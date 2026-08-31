#!/usr/bin/env bash
set -u

require_model=0
require_policy=0
for argument in "$@"; do
  case "$argument" in
    --require-model) require_model=1 ;;
    --require-policy) require_policy=1 ;;
    *) echo "Usage: $0 [--require-model] [--require-policy]" >&2; exit 2 ;;
  esac
done

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
declare -A overrides=()
for name in \
  VLA_DATA_ROOT OPENPI_DATA_HOME LIBERO_TASK_SUITE LIBERO_IMAGE \
  LIBERO_POLICY_GPU_ID LIBERO_SIM_GPU_ID LIBERO_POLICY_HOST LIBERO_POLICY_PORT \
  LIBERO_CHECKPOINT_ID LIBERO_POLICY_CONFIG; do
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

failures=0
warnings=0
ok() { printf 'OK    %s\n' "$1"; }
warn() { printf 'WARN  %s\n' "$1"; warnings=$((warnings + 1)); }
fail() { printf 'FAIL  %s\n' "$1"; failures=$((failures + 1)); }

command -v docker >/dev/null 2>&1 && ok "Docker CLI is installed" || fail "Docker CLI is missing"
docker info >/dev/null 2>&1 && ok "Docker runtime is reachable" || fail "Docker runtime is not reachable"
docker image inspect "$LIBERO_IMAGE" >/dev/null 2>&1 \
  && ok "LIBERO image is present: $LIBERO_IMAGE" \
  || fail "LIBERO image is missing: $LIBERO_IMAGE"

case "$LIBERO_TASK_SUITE" in
  libero_spatial|libero_object|libero_goal|libero_10|libero_90)
    ok "LIBERO task suite: $LIBERO_TASK_SUITE" ;;
  *) fail "Unsupported LIBERO_TASK_SUITE: $LIBERO_TASK_SUITE" ;;
esac

if [[ -d "$VLA_DATA_ROOT" && -w "$VLA_DATA_ROOT" ]]; then
  available_kib="$(df -Pk "$VLA_DATA_ROOT" | awk 'NR==2 {print $4}')"
  available_gib=$((available_kib / 1024 / 1024))
  if (( available_gib >= 10 )); then
    ok "Artifact root has ${available_gib} GiB free: $VLA_DATA_ROOT"
  else
    fail "Artifact root has less than 10 GiB free: $VLA_DATA_ROOT"
  fi
  if (( available_gib < 50 )); then
    warn "Less than 50 GiB remains; do not download another model checkpoint here"
  fi
else
  fail "Artifact root is not writable: $VLA_DATA_ROOT"
fi

if [[ "$LIBERO_POLICY_GPU_ID" == "$LIBERO_SIM_GPU_ID" ]]; then
  warn "Policy and simulator both select physical GPU $LIBERO_POLICY_GPU_ID"
else
  ok "GPU split: policy=$LIBERO_POLICY_GPU_ID, simulator=$LIBERO_SIM_GPU_ID"
fi

if nvidia-smi --query-gpu=index --format=csv,noheader >/dev/null 2>&1; then
  gpu_ids="$(nvidia-smi --query-gpu=index --format=csv,noheader)"
  grep -qx "$LIBERO_POLICY_GPU_ID" <<<"$gpu_ids" \
    && ok "Policy GPU $LIBERO_POLICY_GPU_ID is visible" \
    || fail "Policy GPU $LIBERO_POLICY_GPU_ID is not visible"
  grep -qx "$LIBERO_SIM_GPU_ID" <<<"$gpu_ids" \
    && ok "Simulator GPU $LIBERO_SIM_GPU_ID is visible" \
    || fail "Simulator GPU $LIBERO_SIM_GPU_ID is not visible"
fi

checkpoint_id="${LIBERO_CHECKPOINT_ID:?LIBERO_CHECKPOINT_ID must be set}"
checkpoint_prefix="gs://openpi-assets/checkpoints/"
if [[ "$checkpoint_id" != "$checkpoint_prefix"* ]]; then
  fail "LIBERO_CHECKPOINT_ID must begin with $checkpoint_prefix: $checkpoint_id"
  checkpoint_dir=""
else
  checkpoint_dir="${OPENPI_DATA_HOME}/openpi-assets/checkpoints/${checkpoint_id#"$checkpoint_prefix"}"
fi
if [[ -d "$checkpoint_dir/params" ]]; then
  ok "Checkpoint is present: $checkpoint_id"
elif (( require_model )); then
  fail "Missing checkpoint: $checkpoint_dir"
else
  warn "Checkpoint is not installed yet: $checkpoint_id"
fi

if (( require_policy )); then
  if [[ -n "$(ss -ltnH "sport = :${LIBERO_POLICY_PORT}" 2>/dev/null)" ]]; then
    ok "Policy port is listening: $LIBERO_POLICY_PORT"
  else
    fail "No policy listener on port $LIBERO_POLICY_PORT"
  fi
fi

printf '\nSummary: %d failure(s), %d warning(s)\n' "$failures" "$warnings"
(( failures == 0 ))
