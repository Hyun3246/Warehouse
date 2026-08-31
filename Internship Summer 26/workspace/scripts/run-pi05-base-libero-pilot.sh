#!/usr/bin/env bash
set -euo pipefail

# Runs the matched 10-episode (one initial state per LIBERO-10 task) base-model
# comparison. It never changes the π0.5-LIBERO checkpoint or its prior runs.
workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
checkpoint_id="gs://openpi-assets/checkpoints/pi05_base"

"$workspace_dir/scripts/provision-libero-normalization.sh" "$checkpoint_id"

exec env \
  LIBERO_BENCHMARK_ID="libero-long-base-pilot-10-v1" \
  LIBERO_MODEL_ID="pi05_base" \
  LIBERO_CHECKPOINT_ID="$checkpoint_id" \
  LIBERO_POLICY_CONFIG="pi05_libero" \
  LIBERO_PILOT_TRIALS=1 \
  LIBERO_PILOT_VIDEO_MODE=all \
  LIBERO_TMUX_SESSION="vla-libero-base-pilot" \
  "$workspace_dir/scripts/libero-tmux.sh" start pilot
