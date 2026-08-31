#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
declare -A overrides=()
for name in VLA_DATA_ROOT LIBERO_STREAM_PORT; do
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

mkdir -p "$VLA_DATA_ROOT/runs"
echo "Serving LIBERO live preview on 127.0.0.1:${LIBERO_STREAM_PORT}"
echo "Use an SSH tunnel; the server is not exposed on the LAN."
exec python3 -m http.server "$LIBERO_STREAM_PORT" \
  --bind 127.0.0.1 \
  --directory "$VLA_DATA_ROOT/runs"
