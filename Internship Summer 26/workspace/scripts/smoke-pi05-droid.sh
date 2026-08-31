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

host="${OPENPI_HOST:-localhost}"
port="${OPENPI_PORT:-8001}"
steps="${1:-3}"
run_dir="${VLA_DATA_ROOT:-/home/julnk0207/vla-artifacts}/runs/pi05-droid-smoke"

mkdir -p "$run_dir"
cd "$openpi_dir"
exec .venv/bin/python examples/simple_client/main.py \
  --env DROID \
  --host "$host" \
  --port "$port" \
  --num-steps "$steps" \
  --timing-file "$run_dir/timing.parquet"
