#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
host_env="$workspace_dir/config/host.env"
profile="${1:-pilot}"

case "$profile" in
  pilot|full) ;;
  *) echo "Profile must be pilot or full, got: $profile" >&2; exit 2 ;;
esac

if [[ -r "$host_env" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$host_env"
  set +a
fi

policy_host="${OPENPI_HOST:-localhost}"
policy_port="${OPENPI_PORT:-8001}"
wait_seconds="${TRACK_A_POLICY_WAIT_SECONDS:-180}"
tmux_session="${TRACK_A_TMUX_SESSION:-vla-track-a}"

cleanup_policy() {
  if command -v tmux >/dev/null 2>&1 \
      && tmux has-session -t "$tmux_session" 2>/dev/null; then
    tmux send-keys -t "$tmux_session:policy" C-c 2>/dev/null || true
  fi
}
trap cleanup_policy EXIT INT TERM

echo "Waiting up to ${wait_seconds}s for policy endpoint $policy_host:$policy_port"
deadline=$((SECONDS + wait_seconds))
until timeout 2 bash -c "</dev/tcp/$policy_host/$policy_port" 2>/dev/null; do
  if (( SECONDS >= deadline )); then
    echo "Timed out waiting for policy endpoint $policy_host:$policy_port" >&2
    exit 1
  fi
  sleep 1
done

echo "Policy is ready; starting Track A $profile profile"
set +e
"$workspace_dir/scripts/run-track-a.sh" "$profile"
status=$?
set -e

if (( status == 0 )); then
  echo "Track A $profile profile finished successfully"
else
  echo "Track A $profile profile failed with status $status" >&2
fi
exit "$status"
