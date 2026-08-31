#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sim_dir="$workspace_dir/projects/sim-evals"
host_env="$workspace_dir/config/host.env"

if [[ -f "$host_env" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$host_env"
  set +a
fi

episodes_per_task="${1:-1}"
max_steps="${2:-450}"
order="${3:-sequential}"
protocol="${DROID_PROTOCOL:-droid_sim_12}"
policy_host="${OPENPI_HOST:-localhost}"
policy_port="${OPENPI_PORT:-8001}"
sim_gpu_id="${DROID_SIM_GPU_ID:-2}"
run_dir="${VLA_DATA_ROOT:-/home/julnk0207/vla-artifacts}/runs/pi05-droid-suite"
random_seed="${DROID_TASK_SEED:-0}"
action_mode="${DROID_ACTION_MODE:-joint_velocity}"
open_loop_horizon="${DROID_OPEN_LOOP_HORIZON:-8}"
benchmark_id="${DROID_BENCHMARK_ID:-droid-sim-ad-hoc}"
model_id="${DROID_MODEL_ID:-pi05_droid}"
checkpoint_id="${DROID_CHECKPOINT_ID:-gs://openpi-assets/checkpoints/pi05_droid}"
scoring_status="${DROID_SCORING_STATUS:-provisional}"
camera_profile="${DROID_CAMERA_PROFILE:-external_cam_plus_wrist_224x224}"
run_id="${DROID_RUN_ID:-$(date +%Y%m%d-%H%M%S)}"
run_dir="${DROID_RUN_DIR:-$run_dir}"

if [[ ! -x "$sim_dir/.venv/bin/python" ]]; then
  echo "Missing simulator environment: $sim_dir/.venv" >&2
  exit 1
fi

case "$protocol" in
  droid_sim_12)
    task_set="droid_sim_12"
    task_description="12 frozen prompts in scene 1"
    ;;
  three_scene)
    case "$order" in
      sequential) task_set="all" ;;
      random) task_set="random" ;;
      *)
        echo "ORDER must be 'sequential' or 'random', got: $order" >&2
        exit 2
        ;;
    esac
    task_description="three-scene secondary suite ($order order)"
    ;;
  *)
    echo "DROID_PROTOCOL must be 'droid_sim_12' or 'three_scene', got: $protocol" >&2
    exit 2
    ;;
esac

headless_args=()
display_mode="headless recording"
if [[ "${DROID_STREAMING:-0}" == "1" ]]; then
  streaming_mode="${DROID_STREAMING_MODE:-2}"
  if [[ "$streaming_mode" != "1" && "$streaming_mode" != "2" ]]; then
    echo "DROID_STREAMING_MODE must be 1 or 2, got: $streaming_mode" >&2
    exit 2
  fi
  if [[ "$streaming_mode" == "1" && -z "${PUBLIC_IP:-}" ]]; then
    echo "Public WebRTC mode requires PUBLIC_IP" >&2
    exit 2
  fi
  export LIVESTREAM="$streaming_mode"
  export ENABLE_CAMERAS=1
  display_mode="WebRTC streaming (mode $streaming_mode; TCP 49100, UDP 47998)"
elif [[ "${DROID_HEADLESS:-1}" == "0" ]]; then
  export LIVESTREAM=0
  headless_args+=(--no-headless)
  display_mode="server desktop window"
else
  export LIVESTREAM=0
fi

cd "$sim_dir"
export CUDA_VISIBLE_DEVICES="$sim_gpu_id"
export OMNI_KIT_ACCEPT_EULA=Y

echo "Starting pi0.5-DROID task suite"
echo "Protocol: $protocol"
echo "Tasks: $task_description"
echo "Episodes per task: $episodes_per_task"
echo "Policy endpoint: $policy_host:$policy_port"
echo "Simulation GPU: physical GPU $sim_gpu_id"
echo "Display mode: $display_mode"
echo "Benchmark ID: $benchmark_id"
echo "Model ID: $model_id"
echo "Action mode: $action_mode"
echo "Open-loop horizon: $open_loop_horizon"
echo "Run ID: $run_id"
echo "Scoring status: $scoring_status"
echo "Camera profile: $camera_profile"

.venv/bin/python run_eval.py \
  --episodes "$episodes_per_task" \
  --scene 1 \
  --task-set "$task_set" \
  --remote-host "$policy_host" \
  --remote-port "$policy_port" \
  --action-mode "$action_mode" \
  --open-loop-horizon "$open_loop_horizon" \
  --max-steps "$max_steps" \
  --output-dir "$run_dir" \
  --random-seed "$random_seed" \
  --benchmark-id "$benchmark_id" \
  --model-id "$model_id" \
  --checkpoint-id "$checkpoint_id" \
  --run-id "$run_id" \
  --scoring-status "$scoring_status" \
  --camera-profile "$camera_profile" \
  "${headless_args[@]}"

echo
echo "Task suite finished. Recordings: $run_dir"
