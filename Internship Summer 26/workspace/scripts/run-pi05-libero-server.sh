#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
openpi_dir="$workspace_dir/projects/openpi"

declare -A overrides=()
for name in OPENPI_DATA_HOME LIBERO_POLICY_GPU_ID LIBERO_POLICY_PORT \
  LIBERO_CHECKPOINT_ID LIBERO_POLICY_CONFIG; do
  if [[ -v "$name" ]]; then overrides["$name"]="${!name}"; fi
done
set -a
# shellcheck disable=SC1091
source "$workspace_dir/config/libero.env"
# shellcheck disable=SC1091
source "$workspace_dir/config/host.env"
set +a
for name in "${!overrides[@]}"; do
  printf -v "$name" '%s' "${overrides[$name]}"
  export "$name"
done

checkpoint_id="${LIBERO_CHECKPOINT_ID:?LIBERO_CHECKPOINT_ID must be set}"
checkpoint_prefix="gs://openpi-assets/checkpoints/"
if [[ "$checkpoint_id" != "$checkpoint_prefix"* ]]; then
  echo "LIBERO_CHECKPOINT_ID must begin with $checkpoint_prefix: $checkpoint_id" >&2
  exit 1
fi
checkpoint_dir="${OPENPI_DATA_HOME}/openpi-assets/checkpoints/${checkpoint_id#"$checkpoint_prefix"}"
policy_config="${LIBERO_POLICY_CONFIG:-pi05_libero}"
gpu_id="${LIBERO_POLICY_GPU_ID:-1}"
port="${LIBERO_POLICY_PORT:-8002}"

if [[ ! -x "$openpi_dir/.venv/bin/python" ]]; then
  echo "Missing OpenPI environment: $openpi_dir/.venv" >&2
  exit 1
fi
if [[ ! -d "$checkpoint_dir/params" ]]; then
  echo "Missing checkpoint: $checkpoint_dir" >&2
  echo "Checkpoint download is deferred until writable artifact storage is available." >&2
  exit 1
fi

cd "$openpi_dir"
export CUDA_VISIBLE_DEVICES="$gpu_id"
export OPENPI_DATA_HOME
export XLA_PYTHON_CLIENT_PREALLOCATE=false

echo "Starting $policy_config from $checkpoint_id on physical GPU $gpu_id, port $port"
exec .venv/bin/python scripts/serve_policy.py \
  --port "$port" \
  policy:checkpoint \
  --policy.config="$policy_config" \
  --policy.dir="$checkpoint_dir"
