"""Model-agnostic LIBERO evaluator with structured benchmark records."""

import argparse
import collections
from datetime import datetime
import json
import math
from pathlib import Path
import time
import traceback

import imageio
import numpy as np
from libero.libero import benchmark, get_libero_path
from libero.libero.envs import OffScreenRenderEnv
from openpi_client import image_tools
from openpi_client.websocket_client_policy import WebsocketClientPolicy


DUMMY_ACTION = np.asarray([0.0] * 6 + [-1.0], dtype=np.float32)
ENV_RESOLUTION = 256
MAX_STEPS = {
    "libero_spatial": 220,
    "libero_object": 280,
    "libero_goal": 300,
    "libero_10": 520,
    "libero_90": 400,
}

LIVE_HTML = """<!doctype html>
<meta charset="utf-8">
<title>LIBERO live preview</title>
<style>
body { margin: 0; background: #111; color: #eee; font: 16px system-ui; text-align: center; }
img { max-width: min(96vw, 900px); max-height: 82vh; image-rendering: auto; }
pre { white-space: pre-wrap; }
</style>
<h2>LIBERO live preview</h2>
<img id="frame" src="latest.jpg" alt="Waiting for the first frame">
<pre id="status">Waiting for rollout...</pre>
<script>
async function refresh() {
  const stamp = Date.now();
  document.getElementById('frame').src = 'latest.jpg?t=' + stamp;
  try {
    const response = await fetch('status.json?t=' + stamp);
    document.getElementById('status').textContent = JSON.stringify(await response.json(), null, 2);
  } catch (_) {}
}
setInterval(refresh, 500);
refresh();
</script>
"""


def write_json(path, data):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(path)


def initialize_live_preview(path):
    if path is None:
        return
    path.mkdir(parents=True, exist_ok=True)
    (path / "index.html").write_text(LIVE_HTML)
    write_json(path / "status.json", {"status": "waiting"})


def update_live_preview(path, image, status):
    if path is None:
        return
    temporary = path / ".latest.jpg.tmp"
    imageio.imwrite(temporary, image, format="jpeg", quality=85)
    temporary.replace(path / "latest.jpg")
    write_json(path / "status.json", status)


def summarize_ms(values):
    values = np.asarray(values, dtype=np.float64)
    if not len(values):
        return {"count": 0, "mean": None, "median": None, "p95": None, "max": None}
    return {
        "count": int(len(values)),
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "p95": float(np.percentile(values, 95)),
        "max": float(np.max(values)),
    }


def quat_to_axisangle(quat):
    quat = np.asarray(quat).copy()
    quat[3] = np.clip(quat[3], -1.0, 1.0)
    denominator = np.sqrt(1.0 - quat[3] * quat[3])
    if math.isclose(denominator, 0.0):
        return np.zeros(3)
    return quat[:3] * 2.0 * math.acos(quat[3]) / denominator


def make_environment(task, seed):
    bddl_file = Path(get_libero_path("bddl_files")) / task.problem_folder / task.bddl_file
    env = OffScreenRenderEnv(
        bddl_file_name=str(bddl_file),
        camera_heights=ENV_RESOLUTION,
        camera_widths=ENV_RESOLUTION,
    )
    env.seed(seed)
    return env


def parse_task_ids(value, task_count):
    if value == "all":
        return list(range(task_count))
    task_ids = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not task_ids or len(set(task_ids)) != len(task_ids):
        raise ValueError("--task-ids must contain unique task IDs or 'all'")
    invalid = [task_id for task_id in task_ids if not 0 <= task_id < task_count]
    if invalid:
        raise ValueError("Invalid task IDs: %s" % invalid)
    return task_ids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--suite", choices=tuple(MAX_STEPS), default="libero_10")
    parser.add_argument("--task-ids", default="all")
    parser.add_argument("--trials-per-task", type=int, default=1)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--replan-steps", type=int, default=5)
    parser.add_argument("--wait-steps", type=int, default=10)
    parser.add_argument("--resize-size", type=int, default=224)
    parser.add_argument("--video-mode", choices=("all", "failures", "none"), default="all")
    parser.add_argument("--output-root", type=Path, default=Path("/artifacts/runs/libero-long-v1"))
    parser.add_argument("--benchmark-id", default="libero-long-v1")
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--checkpoint-id", required=True)
    parser.add_argument("--live-preview-dir", type=Path)
    parser.add_argument("--live-preview-every", type=int, default=2)
    args = parser.parse_args()

    if args.trials_per_task < 1:
        raise ValueError("--trials-per-task must be at least 1")
    if args.replan_steps < 1:
        raise ValueError("--replan-steps must be at least 1")
    if args.live_preview_every < 1:
        raise ValueError("--live-preview-every must be at least 1")

    np.random.seed(args.seed)
    suite = benchmark.get_benchmark_dict()[args.suite]()
    task_ids = parse_task_ids(args.task_ids, suite.n_tasks)
    started_at = datetime.now()
    run_id = started_at.strftime("%Y%m%d-%H%M%S")
    run_dir = args.output_root / args.model_id / started_at.strftime("%Y-%m-%d") / started_at.strftime("%H-%M-%S")
    run_dir.mkdir(parents=True, exist_ok=False)
    manifest_path = run_dir / "manifest.json"
    manifest = {
        "benchmark_id": args.benchmark_id,
        "protocol": "openpi-libero-eval-v1",
        "suite": args.suite,
        "model_id": args.model_id,
        "checkpoint_id": args.checkpoint_id,
        "run_id": run_id,
        "started_at": started_at.isoformat(),
        "seed": args.seed,
        "task_ids": task_ids,
        "trials_per_task": args.trials_per_task,
        "expected_episodes": len(task_ids) * args.trials_per_task,
        "max_control_steps": MAX_STEPS[args.suite],
        "wait_steps": args.wait_steps,
        "replan_steps": args.replan_steps,
        "render_resolution": ENV_RESOLUTION,
        "policy_resolution": args.resize_size,
        "video_mode": args.video_mode,
        "policy_endpoint": {"host": args.host, "port": args.port},
        "episodes": [],
        "status": "running",
    }
    write_json(manifest_path, manifest)
    initialize_live_preview(args.live_preview_dir)
    client = WebsocketClientPolicy(args.host, args.port)

    try:
        for task_id in task_ids:
            task = suite.get_task(task_id)
            initial_states = suite.get_task_init_states(task_id)
            if args.trials_per_task > len(initial_states):
                raise ValueError(
                    "Task %d has %d initial states, fewer than %d requested trials"
                    % (task_id, len(initial_states), args.trials_per_task)
                )
            task_dir = run_dir / ("task-%02d" % task_id)
            task_dir.mkdir()
            env = make_environment(task, args.seed)
            try:
                for episode in range(args.trials_per_task):
                    env.reset()
                    observation = env.set_init_state(initial_states[episode])
                    action_plan = collections.deque()
                    frames = []
                    step_rows = []
                    inference_ms = []
                    success = False
                    runtime_error = None
                    episode_started = time.perf_counter()
                    steps_path = task_dir / ("episode-%02d.steps.jsonl" % episode)
                    metrics_path = task_dir / ("episode-%02d.metrics.json" % episode)
                    video_path = task_dir / ("episode-%02d.mp4" % episode)

                    try:
                        for _ in range(args.wait_steps):
                            observation, _, done, _ = env.step(DUMMY_ACTION)
                            if done:
                                break

                        with steps_path.open("w") as steps_file:
                            for step in range(MAX_STEPS[args.suite]):
                                control_started = time.perf_counter()
                                agent_image = np.ascontiguousarray(
                                    observation["agentview_image"][::-1, ::-1]
                                )
                                wrist_image = np.ascontiguousarray(
                                    observation["robot0_eye_in_hand_image"][::-1, ::-1]
                                )
                                policy_image = image_tools.convert_to_uint8(
                                    image_tools.resize_with_pad(
                                        agent_image, args.resize_size, args.resize_size
                                    )
                                )
                                policy_wrist = image_tools.convert_to_uint8(
                                    image_tools.resize_with_pad(
                                        wrist_image, args.resize_size, args.resize_size
                                    )
                                )
                                if args.video_mode != "none":
                                    frames.append(policy_image)
                                if step % args.live_preview_every == 0:
                                    update_live_preview(
                                        args.live_preview_dir,
                                        policy_image,
                                        {
                                            "status": "running",
                                            "run_id": run_id,
                                            "task_id": task_id,
                                            "instruction": str(task.language),
                                            "episode": episode,
                                            "step": step,
                                            "success": False,
                                        },
                                    )

                                requested_policy = not action_plan
                                request_ms = None
                                response_metadata = {}
                                if requested_policy:
                                    request = {
                                        "observation/image": policy_image,
                                        "observation/wrist_image": policy_wrist,
                                        "observation/state": np.concatenate(
                                            (
                                                observation["robot0_eef_pos"],
                                                quat_to_axisangle(observation["robot0_eef_quat"]),
                                                observation["robot0_gripper_qpos"],
                                            )
                                        ),
                                        "prompt": str(task.language),
                                    }
                                    request_started = time.perf_counter()
                                    response = client.infer(request)
                                    request_ms = (time.perf_counter() - request_started) * 1000.0
                                    inference_ms.append(request_ms)
                                    actions = np.asarray(response["actions"])
                                    if len(actions) < args.replan_steps:
                                        raise ValueError(
                                            "Policy returned %d actions; replan_steps=%d"
                                            % (len(actions), args.replan_steps)
                                        )
                                    action_plan.extend(actions[: args.replan_steps])
                                    response_metadata = {
                                        key: value
                                        for key, value in response.items()
                                        if key != "actions" and isinstance(value, (str, int, float, bool, type(None)))
                                    }

                                action = np.asarray(action_plan.popleft(), dtype=np.float32)
                                observation, reward, done, info = env.step(action)
                                success = bool(done)
                                row = {
                                    "task_id": task_id,
                                    "episode": episode,
                                    "initial_state_index": episode,
                                    "step": step,
                                    "requested_policy": requested_policy,
                                    "client_inference_ms": request_ms,
                                    "control_step_ms": (time.perf_counter() - control_started) * 1000.0,
                                    "action": action.tolist(),
                                    "reward": float(reward),
                                    "success": success,
                                    "policy_metadata": response_metadata,
                                }
                                step_rows.append(row)
                                steps_file.write(json.dumps(row) + "\n")
                                if step % 10 == 0:
                                    steps_file.flush()
                                if success:
                                    break
                    except BaseException as exc:
                        runtime_error = {
                            "type": type(exc).__name__,
                            "message": str(exc),
                            "traceback": traceback.format_exc(),
                        }

                    save_video = bool(frames) and (
                        args.video_mode == "all" or (args.video_mode == "failures" and not success)
                    )
                    if save_video:
                        imageio.mimwrite(video_path, frames, fps=10)
                    metrics = {
                        "benchmark_id": args.benchmark_id,
                        "run_id": run_id,
                        "model_id": args.model_id,
                        "checkpoint_id": args.checkpoint_id,
                        "suite": args.suite,
                        "task_id": task_id,
                        "instruction": str(task.language),
                        "episode": episode,
                        "initial_state_index": episode,
                        "seed": args.seed,
                        "success": success,
                        "failure_reason": None if success else ("runtime_error" if runtime_error else "horizon_reached"),
                        "control_steps": len(step_rows),
                        "wall_duration_s": time.perf_counter() - episode_started,
                        "policy_requests": len(inference_ms),
                        "client_inference_ms": summarize_ms(inference_ms),
                        "runtime_error": runtime_error,
                        "video": str(video_path) if save_video else None,
                        "steps_file": str(steps_path),
                    }
                    write_json(metrics_path, metrics)
                    if frames:
                        update_live_preview(
                            args.live_preview_dir,
                            frames[-1],
                            {
                                "status": "episode_complete",
                                "run_id": run_id,
                                "task_id": task_id,
                                "instruction": str(task.language),
                                "episode": episode,
                                "success": success,
                                "control_steps": len(step_rows),
                            },
                        )
                    manifest["episodes"].append(
                        {
                            "task_id": task_id,
                            "instruction": str(task.language),
                            "episode": episode,
                            "initial_state_index": episode,
                            "success": success,
                            "metrics": str(metrics_path),
                            "steps_file": str(steps_path),
                            "video": str(video_path) if save_video else None,
                        }
                    )
                    successes = sum(item["success"] for item in manifest["episodes"])
                    manifest["summary"] = {
                        "episodes": len(manifest["episodes"]),
                        "successes": successes,
                        "failures": len(manifest["episodes"]) - successes,
                        "success_rate": successes / len(manifest["episodes"]),
                    }
                    write_json(manifest_path, manifest)
                    print(
                        "task=%02d episode=%02d success=%s steps=%d"
                        % (task_id, episode, success, len(step_rows)),
                        flush=True,
                    )
                    if runtime_error:
                        raise RuntimeError(runtime_error["message"])
            finally:
                env.close()

        manifest["status"] = "completed"
        manifest["finished_at"] = datetime.now().isoformat()
        write_json(manifest_path, manifest)
        if args.live_preview_dir is not None:
            write_json(
                args.live_preview_dir / "status.json",
                {"status": "completed", "run_id": run_id, "summary": manifest.get("summary")},
            )
        print("manifest=%s" % manifest_path, flush=True)
    except BaseException as exc:
        manifest["status"] = "aborted"
        manifest["finished_at"] = datetime.now().isoformat()
        manifest["abort_reason"] = {"type": type(exc).__name__, "message": str(exc)}
        write_json(manifest_path, manifest)
        raise


if __name__ == "__main__":
    main()
