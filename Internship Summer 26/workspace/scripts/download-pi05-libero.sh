#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
set -a
# shellcheck disable=SC1091
source "$workspace_dir/config/host.env"
set +a

cd "$workspace_dir"
checkpoint_id="${1:-gs://openpi-assets/checkpoints/pi05_libero}"
case "$checkpoint_id" in
  gs://openpi-assets/checkpoints/pi05_libero|gs://openpi-assets/checkpoints/pi05_base) ;;
  *) echo "Usage: $0 [gs://openpi-assets/checkpoints/pi05_libero|gs://openpi-assets/checkpoints/pi05_base]" >&2; exit 2 ;;
esac
exec env OPENPI_DATA_HOME="$OPENPI_DATA_HOME" \
  projects/openpi/.venv/bin/python -c \
  "from openpi.shared import download; print(download.maybe_download('$checkpoint_id'))"
