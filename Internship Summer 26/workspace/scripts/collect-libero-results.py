#!/usr/bin/env python3
"""Normalize the completed LIBERO-10 screening results into JSON, CSV, and Markdown."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from datetime import datetime
from pathlib import Path


BENCHMARK = "libero-long-screening-10-v1"


def wilson_interval(successes: int, episodes: int) -> tuple[float, float]:
    if episodes == 0:
        return (0.0, 0.0)
    z = 1.959963984540054
    p = successes / episodes
    denominator = 1 + z * z / episodes
    center = (p + z * z / (2 * episodes)) / denominator
    margin = z * math.sqrt(p * (1 - p) / episodes + z * z / (4 * episodes**2)) / denominator
    return (100 * (center - margin), 100 * (center + margin))


def load_openpi(path: Path, label: str, family: str) -> dict:
    data = json.loads(path.read_text())
    task_ids = data["task_ids"]
    per_task = []
    for task_id in task_ids:
        episodes = [item for item in data["episodes"] if item["task_id"] == task_id]
        per_task.append(sum(bool(item["success"]) for item in episodes))
    return make_result(
        label=label,
        family=family,
        checkpoint=data["checkpoint_id"],
        evaluator=data["protocol"],
        successes=per_task,
        trials_per_task=data["trials_per_task"],
        source=path,
        started_at=data.get("started_at"),
        finished_at=data.get("finished_at"),
    )


def load_lerobot(path: Path, label: str, family: str, checkpoint: str) -> dict:
    data = json.loads(path.read_text())
    per_task = [sum(item["metrics"]["successes"]) for item in data["per_task"]]
    trials = [len(item["metrics"]["successes"]) for item in data["per_task"]]
    if len(set(trials)) != 1:
        raise ValueError(f"Non-uniform trials in {path}: {trials}")
    return make_result(
        label=label,
        family=family,
        checkpoint=checkpoint,
        evaluator="LeRobot 0.6.1 libero-eval",
        successes=per_task,
        trials_per_task=trials[0],
        source=path,
    )


def load_openvla(
    rollout_dir: Path,
    timestamp: str,
    label: str,
    family: str,
    checkpoint: str,
    evaluator: str,
) -> dict:
    episode_results: dict[int, bool] = {}
    pattern = re.compile(r"episode=(\d+)--success=(True|False)")
    files = sorted(rollout_dir.glob(f"{timestamp}*.mp4"))
    for path in files:
        match = pattern.search(path.name)
        if not match:
            continue
        episode_results[int(match.group(1))] = match.group(2) == "True"
    if sorted(episode_results) != list(range(1, 101)):
        raise ValueError(f"Expected episodes 1..100 for {label}; found {len(episode_results)}")
    per_task = [
        sum(episode_results[episode] for episode in range(task_id * 10 + 1, task_id * 10 + 11))
        for task_id in range(10)
    ]
    return make_result(
        label=label,
        family=family,
        checkpoint=checkpoint,
        evaluator=evaluator,
        successes=per_task,
        trials_per_task=10,
        source=rollout_dir,
    )


def make_result(
    *,
    label: str,
    family: str,
    checkpoint: str,
    evaluator: str,
    successes: list[int],
    trials_per_task: int,
    source: Path,
    started_at: str | None = None,
    finished_at: str | None = None,
) -> dict:
    episodes = len(successes) * trials_per_task
    total_successes = sum(successes)
    ci_low, ci_high = wilson_interval(total_successes, episodes)
    return {
        "model": label,
        "family": family,
        "checkpoint": checkpoint,
        "evaluator": evaluator,
        "episodes": episodes,
        "successes": total_successes,
        "failures": episodes - total_successes,
        "success_rate_percent": 100 * total_successes / episodes,
        "wilson_95_percent": [round(ci_low, 1), round(ci_high, 1)],
        "trials_per_task": trials_per_task,
        "per_task_successes": successes,
        "source": str(source),
        "started_at": started_at,
        "finished_at": finished_at,
    }


def load_validation_run(path: Path, model: str, stage: str) -> dict:
    data = json.loads(path.read_text())
    if "summary" in data:
        successes = data["summary"]["successes"]
        episodes = data["summary"]["episodes"]
    else:
        successes = sum(sum(item["metrics"]["successes"]) for item in data["per_task"])
        episodes = sum(len(item["metrics"]["successes"]) for item in data["per_task"])
    return {
        "model": model,
        "stage": stage,
        "successes": successes,
        "episodes": episodes,
        "source": str(path),
    }


def relative_sources(data: list[dict], artifact_root: Path) -> None:
    for item in data:
        item["source"] = str(Path(item["source"]).relative_to(artifact_root))


def write_markdown(path: Path, payload: dict) -> None:
    results = payload["screening_results"]
    task_names = payload["task_names"]
    lines = [
        "# LIBERO-10 screening results",
        "",
        f"Collected from `{payload['benchmark_id']}` artifacts. All primary results use 10 tasks and 10 episodes per task.",
        "",
        "## Overall results",
        "",
        "| Rank | Model | Successes | SR | Wilson 95% CI |",
        "|---:|---|---:|---:|---:|",
    ]
    for rank, result in enumerate(results, 1):
        low, high = result["wilson_95_percent"]
        lines.append(
            f"| {rank} | {result['model']} | {result['successes']}/{result['episodes']} "
            f"| {result['success_rate_percent']:.0f}% | {low:.1f}–{high:.1f}% |"
        )
    lines.extend(
        [
            "",
            "## Per-task successes",
            "",
            "Each cell is successes out of 10 episodes.",
            "",
            "| Model | " + " | ".join(f"T{i}" for i in range(10)) + " | Total |",
            "|---|" + "---:|" * 11,
        ]
    )
    for result in results:
        cells = " | ".join(str(value) for value in result["per_task_successes"])
        lines.append(f"| {result['model']} | {cells} | {result['successes']} |")
    lines.extend(["", "## Task index", ""])
    for task_id, task_name in enumerate(task_names):
        lines.append(f"- T{task_id}: {task_name}")
    lines.extend(
        [
            "",
            "## Validation runs",
            "",
            "Smoke and pilot runs validated execution only; their small samples are not primary benchmark scores.",
            "",
            "| Model | Stage | Result |",
            "|---|---|---:|",
        ]
    )
    for run in payload["validation_runs"]:
        lines.append(f"| {run['model']} | {run['stage']} | {run['successes']}/{run['episodes']} |")
    lines.extend(
        [
            "",
            "## Interpretation limits",
            "",
            "- This is the reduced 100-episode screening profile, not the 500-episode, 50-trials-per-task full profile.",
            "- Runs used the same LIBERO-10 task order, seed 7, fixed initial states, hard resets, and 10 trials per task.",
            "- OpenPI, OpenVLA, and LeRobot policies required different evaluator/runtime stacks. Treat comparisons as controlled screening results, not a bit-identical reproduction of every paper's official environment.",
            "- The π0.5-base result uses LIBERO normalization with the general base checkpoint; its 0% is the intended post-training-effect baseline.",
            "",
            "## Provenance",
            "",
        ]
    )
    for result in results:
        lines.append(f"- {result['model']}: `{result['source']}`")
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path, default=Path("/home/julnk0207/vla-artifacts"))
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1] / "results")
    args = parser.parse_args()
    root = args.artifact_root.resolve()
    campaign = root / "runs" / BENCHMARK

    pi05_libero_manifest = root / "runs/pi0.5-libero/pi05_libero/2026-08-19/02-30-22/manifest.json"
    pi05_base_manifest = campaign / "pi05_base/2026-08-19/07-16-39/manifest.json"
    task_names = [item["instruction"] for item in json.loads(pi05_libero_manifest.read_text())["episodes"][::10]]

    results = [
        load_openpi(pi05_libero_manifest, "π0.5-LIBERO", "OpenPI"),
        load_openpi(pi05_base_manifest, "π0.5-base", "OpenPI"),
        load_openvla(
            campaign / "openvla_7b_libero_10/rollouts/2026_08_19",
            "2026_08_19-18_12_10",
            "OpenVLA-7B LIBERO-10",
            "OpenVLA",
            "openvla/openvla-7b-finetuned-libero-10",
            "OpenVLA official LIBERO evaluator",
        ),
        load_openvla(
            campaign / "openvla_oft_libero_10/rollouts/2026_08_19",
            "2026_08_19-17_12_58",
            "OpenVLA-OFT LIBERO-10",
            "OpenVLA-OFT",
            "moojink/openvla-7b-oft-finetuned-libero-10",
            "OpenVLA-OFT official LIBERO evaluator",
        ),
        load_lerobot(
            campaign / "smolvla_libero/screening/eval_info.json",
            "SmolVLA LIBERO",
            "LeRobot",
            "HuggingFaceVLA/smolvla_libero",
        ),
        load_lerobot(
            campaign / "pi0fast_libero/screening/eval_info.json",
            "π0-FAST LIBERO",
            "LeRobot",
            "lerobot/pi0fast-libero",
        ),
        load_lerobot(
            campaign / "vla_jepa_libero/screening/eval_info.json",
            "VLA-JEPA LIBERO",
            "LeRobot",
            "lerobot/VLA-JEPA-LIBERO",
        ),
    ]
    for result in results:
        if result["episodes"] != 100:
            raise ValueError(f"Primary result is not 100 episodes: {result['model']}")
    results.sort(key=lambda item: (-item["successes"], item["model"]))

    validations = [
        load_validation_run(root / "runs/pi0.5-libero-pilot/pi05_libero/2026-08-19/01-48-50/manifest.json", "π0.5-LIBERO", "pilot"),
        load_validation_run(root / "runs/pi0.5-base-pilot/pi05_base/2026-08-19/06-42-41/manifest.json", "π0.5-base", "pilot"),
        load_validation_run(campaign / "smolvla_libero/smoke-task0/eval_info.json", "SmolVLA LIBERO", "smoke"),
        load_validation_run(campaign / "smolvla_libero/pilot/eval_info.json", "SmolVLA LIBERO", "pilot"),
        load_validation_run(campaign / "pi0fast_libero/smoke/eval_info.json", "π0-FAST LIBERO", "smoke"),
        load_validation_run(campaign / "pi0fast_libero/pilot/eval_info.json", "π0-FAST LIBERO", "pilot"),
        load_validation_run(campaign / "vla_jepa_libero/validity check/eval_info.json", "VLA-JEPA LIBERO", "smoke"),
        load_validation_run(campaign / "vla_jepa_libero/pilot/eval_info.json", "VLA-JEPA LIBERO", "pilot"),
    ]
    relative_sources(results, root)
    relative_sources(validations, root)

    payload = {
        "benchmark_id": BENCHMARK,
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "suite": "LIBERO-10 / LIBERO-Long",
        "seed": 7,
        "tasks": 10,
        "trials_per_task": 10,
        "episodes_per_model": 100,
        "task_names": task_names,
        "screening_results": results,
        "validation_runs": validations,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / f"{BENCHMARK}.json"
    csv_path = args.output_dir / f"{BENCHMARK}.csv"
    md_path = args.output_dir / f"{BENCHMARK}.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    with csv_path.open("w", newline="") as handle:
        fieldnames = ["model", "successes", "episodes", "success_rate_percent"] + [f"task_{i}" for i in range(10)]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            row = {key: result[key] for key in fieldnames[:4]}
            row.update({f"task_{i}": value for i, value in enumerate(result["per_task_successes"])})
            writer.writerow(row)
    write_markdown(md_path, payload)
    print(json_path)
    print(csv_path)
    print(md_path)


if __name__ == "__main__":
    main()
