#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
host_env="$workspace_dir/config/host.env"
track_env="$workspace_dir/config/track-a.env"

# Load versioned defaults first so shell variables can override them.
declare -A shell_overrides=()
for name in \
  TRACK_A_PROTOCOL TRACK_A_MODEL_ID TRACK_A_BENCHMARK_ID TRACK_A_CHECKPOINT_ID \
  TRACK_A_CAMERA_PROFILE \
  TRACK_A_ACTION_MODE TRACK_A_OPEN_LOOP_HORIZON TRACK_A_PILOT_EPISODES \
  TRACK_A_FULL_EPISODES TRACK_A_MAX_STEPS TRACK_A_ORDER \
  TRACK_A_RANDOM_SEED TRACK_A_SCORING_VALIDATED TRACK_A_STREAMING \
  TRACK_A_STREAMING_MODE PUBLIC_IP; do
  if [[ -v "$name" ]]; then
    shell_overrides["$name"]="${!name}"
  fi
done

set -a
# shellcheck disable=SC1090
source "$track_env"
if [[ -r "$host_env" ]]; then
  # shellcheck disable=SC1090
  source "$host_env"
fi
set +a

for name in "${!shell_overrides[@]}"; do
  printf -v "$name" '%s' "${shell_overrides[$name]}"
  export "$name"
done

profile="${1:-pilot}"
case "$profile" in
  pilot) episodes="$TRACK_A_PILOT_EPISODES" ;;
  full) episodes="$TRACK_A_FULL_EPISODES" ;;
  *) echo "Usage: $0 [pilot|full]" >&2; exit 2 ;;
esac

if [[ "$profile" == "full" && "${TRACK_A_PROTOCOL:-droid_sim_12}" == "three_scene" \
    && "${TRACK_A_SCORING_VALIDATED:-0}" != "1" ]]; then
  echo "Full runs are blocked until TRACK_A_SCORING_VALIDATED=1." >&2
  echo "Validate the provisional success rules on pilot videos first." >&2
  exit 1
fi

case "$TRACK_A_MODEL_ID" in
  pi05_droid) ;;
  *)
    echo "Track A model is not installed yet: $TRACK_A_MODEL_ID" >&2
    exit 2
    ;;
esac

export DROID_BENCHMARK_ID="$TRACK_A_BENCHMARK_ID"
export DROID_PROTOCOL="$TRACK_A_PROTOCOL"
export DROID_MODEL_ID="$TRACK_A_MODEL_ID"
export DROID_CHECKPOINT_ID="$TRACK_A_CHECKPOINT_ID"
export DROID_CAMERA_PROFILE="$TRACK_A_CAMERA_PROFILE"
export DROID_ACTION_MODE="$TRACK_A_ACTION_MODE"
export DROID_OPEN_LOOP_HORIZON="$TRACK_A_OPEN_LOOP_HORIZON"
export DROID_TASK_SEED="$TRACK_A_RANDOM_SEED"
if [[ "$TRACK_A_PROTOCOL" == "droid_sim_12" ]]; then
  export DROID_SCORING_STATUS=pending_manual_review
elif [[ "${TRACK_A_SCORING_VALIDATED:-0}" == "1" ]]; then
  export DROID_SCORING_STATUS=validated
else
  export DROID_SCORING_STATUS=provisional
fi
export DROID_STREAMING="$TRACK_A_STREAMING"
export DROID_STREAMING_MODE="$TRACK_A_STREAMING_MODE"
export DROID_RUN_DIR="${VLA_DATA_ROOT:-/home/julnk0207/vla-artifacts}/runs/$TRACK_A_BENCHMARK_ID/$TRACK_A_MODEL_ID"

"$workspace_dir/scripts/track-a-preflight.sh" --require-policy

echo
echo "Track A profile: $profile"
echo "Protocol: $TRACK_A_PROTOCOL"
echo "Benchmark: $TRACK_A_BENCHMARK_ID"
echo "Model: $TRACK_A_MODEL_ID"
echo "Episodes per task: $episodes"
if [[ "$TRACK_A_PROTOCOL" == "droid_sim_12" ]]; then
  echo "Expected rollouts: $((12 * episodes))"
fi
echo "Streaming: $TRACK_A_STREAMING"

exec "$workspace_dir/scripts/run-pi05-droid-suite.sh" \
  "$episodes" "$TRACK_A_MAX_STEPS" "$TRACK_A_ORDER"
