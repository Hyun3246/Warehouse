#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

declare -A overrides=()
for name in \
  LIBERO_BENCHMARK_ID LIBERO_TASK_SUITE LIBERO_MODEL_ID LIBERO_CHECKPOINT_ID \
  LIBERO_SEED LIBERO_REPLAN_STEPS LIBERO_WAIT_STEPS LIBERO_POLICY_RESOLUTION \
  LIBERO_SMOKE_TRIALS LIBERO_PILOT_TRIALS LIBERO_FULL_TRIALS \
  LIBERO_PILOT_VIDEO_MODE LIBERO_FULL_VIDEO_MODE LIBERO_IMAGE \
  LIBERO_STREAMING LIBERO_STREAM_PORT LIBERO_LIVE_PREVIEW_EVERY \
  LIBERO_POLICY_GPU_ID LIBERO_SIM_GPU_ID LIBERO_POLICY_HOST LIBERO_POLICY_PORT; do
  if [[ -v "$name" ]]; then
    overrides["$name"]="${!name}"
  fi
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

profile="${1:-pilot}"
case "$profile" in
  smoke)
    trials="$LIBERO_SMOKE_TRIALS"
    task_ids=0
    video_mode=all
    ;;
  pilot)
    trials="$LIBERO_PILOT_TRIALS"
    task_ids=all
    video_mode="$LIBERO_PILOT_VIDEO_MODE"
    ;;
  full)
    trials="$LIBERO_FULL_TRIALS"
    task_ids=all
    video_mode="$LIBERO_FULL_VIDEO_MODE"
    ;;
  *) echo "Usage: $0 [smoke|pilot|full]" >&2; exit 2 ;;
esac

"$workspace_dir/scripts/libero-preflight.sh" --require-model --require-policy

output_root="${VLA_DATA_ROOT}/runs/${LIBERO_BENCHMARK_ID}"
live_args=()
if [[ "${LIBERO_STREAMING:-0}" == 1 ]]; then
  live_args=(
    --live-preview-dir "/artifacts/runs/${LIBERO_BENCHMARK_ID}/_live"
    --live-preview-every "${LIBERO_LIVE_PREVIEW_EVERY:-2}"
  )
fi
echo
echo "LIBERO profile: $profile"
echo "Suite: $LIBERO_TASK_SUITE"
echo "Tasks: $task_ids"
echo "Trials per task: $trials"
echo "Video mode: $video_mode"
echo "Simulator GPU: physical GPU ${LIBERO_SIM_GPU_ID}"
echo "Output: $output_root"

exec docker run --rm \
  --network host \
  --device "nvidia.com/gpu=${LIBERO_SIM_GPU_ID}" \
  -e MUJOCO_GL=egl \
  -e MUJOCO_EGL_DEVICE_ID=0 \
  -e PYOPENGL_PLATFORM=egl \
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics \
  -v "${VLA_DATA_ROOT}:/artifacts" \
  "$LIBERO_IMAGE" \
  python /opt/smoke/libero_eval.py \
    --host "$LIBERO_POLICY_HOST" \
    --port "$LIBERO_POLICY_PORT" \
    --suite "$LIBERO_TASK_SUITE" \
    --task-ids "$task_ids" \
    --trials-per-task "$trials" \
    --seed "$LIBERO_SEED" \
    --replan-steps "$LIBERO_REPLAN_STEPS" \
    --wait-steps "$LIBERO_WAIT_STEPS" \
    --resize-size "$LIBERO_POLICY_RESOLUTION" \
    --video-mode "$video_mode" \
    --output-root "/artifacts/runs/${LIBERO_BENCHMARK_ID}" \
    --benchmark-id "$LIBERO_BENCHMARK_ID" \
    --model-id "$LIBERO_MODEL_ID" \
    --checkpoint-id "$LIBERO_CHECKPOINT_ID" \
    "${live_args[@]}"
