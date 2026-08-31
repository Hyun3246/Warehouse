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

episodes="${1:-1}"
scene="${2:-1}"
max_steps="${3:-450}"
policy_host="${OPENPI_HOST:-localhost}"
policy_port="${OPENPI_PORT:-8001}"
sim_gpu_id="${DROID_SIM_GPU_ID:-2}"
run_dir="${VLA_DATA_ROOT:-/home/julnk0207/vla-artifacts}/runs/pi05-droid-rollouts"

if [[ ! -x "$sim_dir/.venv/bin/python" ]]; then
  echo "Missing simulator environment: $sim_dir/.venv" >&2
  exit 1
fi

cd "$sim_dir"
export CUDA_VISIBLE_DEVICES="$sim_gpu_id"
export OMNI_KIT_ACCEPT_EULA=Y

echo "Starting velocity rollout on physical GPU $sim_gpu_id"
echo "Policy endpoint: $policy_host:$policy_port"
exec .venv/bin/python run_eval.py \
  --episodes "$episodes" \
  --scene "$scene" \
  --remote-host "$policy_host" \
  --remote-port "$policy_port" \
  --action-mode joint_velocity \
  --max-steps "$max_steps" \
  --output-dir "$run_dir"
