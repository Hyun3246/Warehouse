#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
session="${TRACK_A_TMUX_SESSION:-vla-track-a}"
command_name="${1:-start}"

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux is not installed" >&2
  exit 1
fi

if [[ ! "$session" =~ ^[A-Za-z0-9_-]+$ ]]; then
  echo "Invalid TRACK_A_TMUX_SESSION: $session" >&2
  exit 2
fi

case "$command_name" in
  start)
    profile="${2:-pilot}"
    case "$profile" in
      pilot|full) ;;
      *) echo "Profile must be pilot or full, got: $profile" >&2; exit 2 ;;
    esac

    if tmux has-session -t "$session" 2>/dev/null; then
      echo "tmux session already exists: $session" >&2
      echo "Attach with: $0 attach" >&2
      exit 1
    fi
    if [[ -n "$(ss -ltnH 'sport = :8001' 2>/dev/null)" ]]; then
      echo "Policy port 8001 is already in use; refusing to start a second server" >&2
      exit 1
    fi

    # Build the session and its environment before starting either workload.
    # Both workload windows keep an interactive shell as their top-level
    # process, so a failed command leaves its output available for inspection.
    tmux new-session -d -s "$session" -n bootstrap -c "$workspace_dir"
    tmux set-option -t "$session" remain-on-exit on
    tmux set-environment -t "$session" TRACK_A_TMUX_SESSION "$session"

    for name in \
      TRACK_A_PROTOCOL TRACK_A_MODEL_ID TRACK_A_BENCHMARK_ID TRACK_A_CHECKPOINT_ID \
      TRACK_A_CAMERA_PROFILE \
      TRACK_A_ACTION_MODE TRACK_A_OPEN_LOOP_HORIZON TRACK_A_PILOT_EPISODES \
      TRACK_A_FULL_EPISODES TRACK_A_MAX_STEPS TRACK_A_ORDER \
      TRACK_A_RANDOM_SEED TRACK_A_SCORING_VALIDATED TRACK_A_STREAMING TRACK_A_STREAMING_MODE \
      TRACK_A_POLICY_WAIT_SECONDS PUBLIC_IP; do
      if [[ -v "$name" ]]; then
        tmux set-environment -t "$session" "$name" "${!name}"
      fi
    done

    if ! tmux new-window -d -t "$session:" -n policy -c "$workspace_dir"; then
      tmux kill-session -t "$session"
      exit 1
    fi
    if ! tmux new-window -d -t "$session:" -n benchmark -c "$workspace_dir"; then
      tmux kill-session -t "$session"
      exit 1
    fi

    tmux send-keys -t "$session:policy" \
      "$workspace_dir/scripts/run-pi05-droid-server.sh" Enter
    tmux send-keys -t "$session:benchmark" \
      "$workspace_dir/scripts/track-a-wait-and-run.sh $profile" Enter
    tmux select-window -t "$session:benchmark"
    tmux kill-window -t "$session:bootstrap"

    echo "Started detached tmux session: $session"
    echo "Attach: $0 attach"
    echo "Status: $0 status"
    echo "Stop:   $0 stop"
    ;;
  attach)
    exec tmux attach-session -t "$session"
    ;;
  status)
    if tmux has-session -t "$session" 2>/dev/null; then
      tmux list-windows -t "$session" \
        -F '#{window_index}:#{window_name} active=#{window_active} panes=#{window_panes}'
      echo
      echo "Recent benchmark output:"
      tmux capture-pane -p -t "$session:benchmark" -S -20 2>/dev/null || true
    else
      echo "No tmux session named $session"
      exit 1
    fi
    ;;
  stop)
    if tmux has-session -t "$session" 2>/dev/null; then
      tmux kill-session -t "$session"
      echo "Stopped tmux session: $session"
    else
      echo "No tmux session named $session"
    fi
    ;;
  *)
    echo "Usage: $0 {start [pilot|full]|attach|status|stop}" >&2
    exit 2
    ;;
esac
