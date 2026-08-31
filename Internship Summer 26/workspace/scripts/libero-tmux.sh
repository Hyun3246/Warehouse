#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
session="${LIBERO_TMUX_SESSION:-vla-libero}"
command_name="${1:-start}"

declare -A overrides=()
for name in \
  LIBERO_BENCHMARK_ID LIBERO_TASK_SUITE LIBERO_MODEL_ID LIBERO_CHECKPOINT_ID \
  LIBERO_POLICY_CONFIG \
  LIBERO_SEED LIBERO_REPLAN_STEPS LIBERO_WAIT_STEPS LIBERO_POLICY_RESOLUTION \
  LIBERO_SMOKE_TRIALS LIBERO_PILOT_TRIALS LIBERO_FULL_TRIALS \
  LIBERO_PILOT_VIDEO_MODE LIBERO_FULL_VIDEO_MODE LIBERO_IMAGE \
  LIBERO_STREAMING LIBERO_STREAM_PORT LIBERO_LIVE_PREVIEW_EVERY \
  LIBERO_POLICY_GPU_ID LIBERO_SIM_GPU_ID LIBERO_POLICY_HOST LIBERO_POLICY_PORT; do
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

case "$command_name" in
  start)
    profile="${2:-pilot}"
    case "$profile" in smoke|pilot|full) ;; *) echo "Profile must be smoke, pilot, or full" >&2; exit 2 ;; esac
    if tmux has-session -t "$session" 2>/dev/null; then
      echo "tmux session already exists: $session" >&2
      exit 1
    fi
    if [[ -n "$(ss -ltnH "sport = :${LIBERO_POLICY_PORT}" 2>/dev/null)" ]]; then
      echo "Policy port ${LIBERO_POLICY_PORT} is already in use" >&2
      exit 1
    fi
    if [[ "${LIBERO_STREAMING:-0}" == 1 && -n "$(ss -ltnH "sport = :${LIBERO_STREAM_PORT}" 2>/dev/null)" ]]; then
      echo "Live-preview port ${LIBERO_STREAM_PORT} is already in use" >&2
      exit 1
    fi
    "$workspace_dir/scripts/libero-preflight.sh" --require-model

    tmux new-session -d -s "$session" -n bootstrap -c "$workspace_dir"
    tmux set-option -t "$session" remain-on-exit on
    tmux set-environment -t "$session" LIBERO_TMUX_SESSION "$session"
    for name in \
      LIBERO_BENCHMARK_ID LIBERO_TASK_SUITE LIBERO_MODEL_ID LIBERO_CHECKPOINT_ID \
      LIBERO_POLICY_CONFIG \
      LIBERO_SEED LIBERO_REPLAN_STEPS LIBERO_WAIT_STEPS LIBERO_POLICY_RESOLUTION \
      LIBERO_SMOKE_TRIALS LIBERO_PILOT_TRIALS LIBERO_FULL_TRIALS \
      LIBERO_PILOT_VIDEO_MODE LIBERO_FULL_VIDEO_MODE LIBERO_IMAGE \
      LIBERO_STREAMING LIBERO_STREAM_PORT LIBERO_LIVE_PREVIEW_EVERY \
      LIBERO_POLICY_GPU_ID LIBERO_SIM_GPU_ID LIBERO_POLICY_HOST LIBERO_POLICY_PORT; do
      if [[ -v "$name" ]]; then tmux set-environment -t "$session" "$name" "${!name}"; fi
    done
    tmux new-window -d -t "$session:" -n policy -c "$workspace_dir"
    tmux new-window -d -t "$session:" -n benchmark -c "$workspace_dir"
    if [[ "${LIBERO_STREAMING:-0}" == 1 ]]; then
      tmux new-window -d -t "$session:" -n stream -c "$workspace_dir"
      tmux send-keys -t "$session:stream" "$workspace_dir/scripts/run-libero-stream.sh" Enter
    fi
    tmux send-keys -t "$session:policy" "$workspace_dir/scripts/run-pi05-libero-server.sh" Enter
    tmux send-keys -t "$session:benchmark" "$workspace_dir/scripts/libero-wait-and-run.sh $profile" Enter
    tmux select-window -t "$session:benchmark"
    tmux kill-window -t "$session:bootstrap"
    echo "Started detached tmux session: $session"
    echo "Attach benchmark: tmux attach -t $session:benchmark"
    echo "Attach policy:    tmux attach -t $session:policy"
    ;;
  attach) exec tmux attach -t "$session" ;;
  status)
    tmux list-windows -t "$session" -F '#{window_index}:#{window_name} active=#{window_active} panes=#{window_panes}'
    echo
    tmux capture-pane -p -t "$session:benchmark" -S -30 2>/dev/null || true
    ;;
  stop)
    if tmux has-session -t "$session" 2>/dev/null; then
      tmux kill-session -t "$session"
      echo "Stopped tmux session: $session"
    else
      echo "No tmux session named $session"
    fi
    ;;
  *) echo "Usage: $0 {start [smoke|pilot|full]|attach|status|stop}" >&2; exit 2 ;;
esac
