#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
set -a
# shellcheck disable=SC1091
source "$workspace_dir/config/libero.env"
# shellcheck disable=SC1091
source "$workspace_dir/config/host.env"
set +a

checkpoint_id="${1:-$LIBERO_CHECKPOINT_ID}"
source_id="${LIBERO_NORMALIZATION_CHECKPOINT_ID:?LIBERO_NORMALIZATION_CHECKPOINT_ID must be set}"
prefix="gs://openpi-assets/checkpoints/"
for identifier in "$checkpoint_id" "$source_id"; do
  [[ "$identifier" == "$prefix"* ]] || { echo "Invalid checkpoint ID: $identifier" >&2; exit 2; }
done

target_dir="${OPENPI_DATA_HOME}/openpi-assets/checkpoints/${checkpoint_id#"$prefix"}"
source_dir="${OPENPI_DATA_HOME}/openpi-assets/checkpoints/${source_id#"$prefix"}"
asset="physical-intelligence/libero/norm_stats.json"

[[ -d "$target_dir/params" ]] || { echo "Target checkpoint is missing: $target_dir" >&2; exit 1; }
[[ -f "$source_dir/assets/$asset" ]] || { echo "Source LIBERO stats are missing: $source_dir/assets/$asset" >&2; exit 1; }

mkdir -p "$target_dir/assets/physical-intelligence/libero"
cp -p "$source_dir/assets/$asset" "$target_dir/assets/$asset"
printf 'Provisioned LIBERO normalization from %s into %s\n' "$source_id" "$checkpoint_id"
