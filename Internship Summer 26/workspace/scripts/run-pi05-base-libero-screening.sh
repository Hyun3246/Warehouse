#!/usr/bin/env bash
set -euo pipefail

# Runs the π0.5-base comparator on the exact π0.5-LIBERO screening protocol:
# LIBERO-10, ten initial states per task, seed 7, and failure videos.
workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
checkpoint_id="gs://openpi-assets/checkpoints/pi05_base"

"$workspace_dir/scripts/provision-libero-normalization.sh" "$checkpoint_id"

exec env \
  LIBERO_BENCHMARK_ID="libero-long-screening-10-v1" \
  LIBERO_MODEL_ID="pi05_base" \
  LIBERO_CHECKPOINT_ID="$checkpoint_id" \
  LIBERO_POLICY_CONFIG="pi05_libero" \
  LIBERO_PILOT_TRIALS=10 \
  LIBERO_PILOT_VIDEO_MODE=failures \
  LIBERO_TMUX_SESSION="vla-libero-base-screening" \
  "$workspace_dir/scripts/libero-tmux.sh" start pilot
