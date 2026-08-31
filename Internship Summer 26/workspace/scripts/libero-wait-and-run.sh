#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
profile="${1:-pilot}"

declare -A overrides=()
for name in \
  LIBERO_BENCHMARK_ID LIBERO_TASK_SUITE LIBERO_MODEL_ID LIBERO_CHECKPOINT_ID \
  LIBERO_SEED LIBERO_REPLAN_STEPS LIBERO_WAIT_STEPS LIBERO_POLICY_RESOLUTION \
  LIBERO_SMOKE_TRIALS LIBERO_PILOT_TRIALS LIBERO_FULL_TRIALS \
  LIBERO_PILOT_VIDEO_MODE LIBERO_FULL_VIDEO_MODE LIBERO_IMAGE \
  LIBERO_STREAMING LIBERO_STREAM_PORT LIBERO_LIVE_PREVIEW_EVERY \
  LIBERO_POLICY_GPU_ID LIBERO_SIM_GPU_ID LIBERO_POLICY_HOST LIBERO_POLICY_PORT \
  LIBERO_POLICY_WAIT_SECONDS LIBERO_TMUX_SESSION; do
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

session="${LIBERO_TMUX_SESSION:-vla-libero}"
wait_seconds="${LIBERO_POLICY_WAIT_SECONDS:-180}"

cleanup_policy() {
  if tmux has-session -t "$session" 2>/dev/null; then
    tmux send-keys -t "$session:policy" C-c 2>/dev/null || true
  fi
}
trap cleanup_policy EXIT INT TERM

echo "Waiting up to ${wait_seconds}s for policy port ${LIBERO_POLICY_PORT}"
deadline=$((SECONDS + wait_seconds))
until [[ -n "$(ss -ltnH "sport = :${LIBERO_POLICY_PORT}" 2>/dev/null)" ]]; do
  if (( SECONDS >= deadline )); then
    echo "Timed out waiting for policy port ${LIBERO_POLICY_PORT}" >&2
    exit 1
  fi
  sleep 1
done

echo "Policy is ready; starting LIBERO $profile profile"
"$workspace_dir/scripts/run-libero.sh" "$profile"
