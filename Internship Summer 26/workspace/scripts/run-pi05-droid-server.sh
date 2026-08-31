#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
openpi_dir="$workspace_dir/projects/openpi"
host_env="$workspace_dir/config/host.env"

if [[ -f "$host_env" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$host_env"
  set +a
fi

openpi_data_home="${OPENPI_DATA_HOME:-/home/julnk0207/vla-artifacts/cache/openpi}"
checkpoint_dir="$openpi_data_home/openpi-assets/checkpoints/pi05_droid"
gpu_id="${OPENPI_GPU_ID:-1}"
port="${OPENPI_PORT:-8001}"

if [[ ! -x "$openpi_dir/.venv/bin/python" ]]; then
  echo "Missing OpenPI environment: $openpi_dir/.venv" >&2
  exit 1
fi

if [[ ! -d "$checkpoint_dir/params" ]]; then
  echo "Missing pi0.5-DROID checkpoint: $checkpoint_dir" >&2
  exit 1
fi

cd "$openpi_dir"
export CUDA_VISIBLE_DEVICES="$gpu_id"
export OPENPI_DATA_HOME="$openpi_data_home"
export XLA_PYTHON_CLIENT_PREALLOCATE=false

echo "Starting pi0.5-DROID on physical GPU $gpu_id, port $port"
exec .venv/bin/python scripts/serve_policy.py \
  --port "$port" \
  policy:checkpoint \
  --policy.config=pi05_droid \
  --policy.dir="$checkpoint_dir"
