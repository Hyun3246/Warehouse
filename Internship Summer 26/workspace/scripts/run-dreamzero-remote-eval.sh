#!/usr/bin/env bash
set -euo pipefail

if (( $# < 1 || $# > 4 )); then
  echo "Usage: $0 API_HOST [API_PORT] [EPISODES] [SCENE]" >&2
  exit 2
fi

api_host="$1"
api_port="${2:-6000}"
episodes="${3:-1}"
scene="${4:-1}"

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sim_dir="$workspace_dir/projects/sim-evals"
dreamzero_eval="$workspace_dir/projects/dreamzero/eval_utils/run_sim_eval.py"

if [[ ! -x "$sim_dir/.venv/bin/python" ]]; then
  echo "Missing simulator environment: $sim_dir/.venv" >&2
  exit 1
fi

if [[ ! -f "$dreamzero_eval" ]]; then
  echo "Missing DreamZero evaluation script: $dreamzero_eval" >&2
  exit 1
fi

cd "$sim_dir"
export OMNI_KIT_ACCEPT_EULA=Y
exec .venv/bin/python "$dreamzero_eval" \
  --host "$api_host" \
  --port "$api_port" \
  --episodes "$episodes" \
  --scene "$scene" \
  --headless
