#!/usr/bin/env bash
set -u

failures=0
warnings=0
require_policy=0

if [[ "${1:-}" == "--require-policy" ]]; then
  require_policy=1
elif [[ $# -gt 0 ]]; then
  echo "Usage: $0 [--require-policy]" >&2
  exit 2
fi

ok() { printf 'OK    %s\n' "$1"; }
warn() { printf 'WARN  %s\n' "$1"; warnings=$((warnings + 1)); }
fail() { printf 'FAIL  %s\n' "$1"; failures=$((failures + 1)); }

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
host_env="$workspace_dir/config/host.env"
track_env="$workspace_dir/config/track-a.env"

# Preserve explicit one-command overrides such as TRACK_A_STREAMING=1.
declare -A shell_overrides=()
for name in TRACK_A_STREAMING TRACK_A_STREAMING_MODE PUBLIC_IP; do
  if [[ -v "$name" ]]; then
    shell_overrides["$name"]="${!name}"
  fi
done

for env_file in "$track_env" "$host_env"; do
  if [[ -r "$env_file" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$env_file"
    set +a
    ok "Loaded $env_file"
  else
    fail "Missing configuration: $env_file"
  fi
done

for name in "${!shell_overrides[@]}"; do
  printf -v "$name" '%s' "${shell_overrides[$name]}"
  export "$name"
done

openpi_dir="$workspace_dir/projects/openpi"
sim_dir="$workspace_dir/projects/sim-evals"
artifact_root="${VLA_DATA_ROOT:-/home/julnk0207/vla-artifacts}"
openpi_data_home="${OPENPI_DATA_HOME:-$artifact_root/cache/openpi}"
checkpoint_dir="$openpi_data_home/openpi-assets/checkpoints/pi05_droid"
policy_host="${OPENPI_HOST:-localhost}"
policy_port="${OPENPI_PORT:-8001}"
policy_gpu="${OPENPI_GPU_ID:-1}"
sim_gpu="${DROID_SIM_GPU_ID:-2}"
streaming="${TRACK_A_STREAMING:-0}"
streaming_mode="${TRACK_A_STREAMING_MODE:-2}"

[[ -x "$openpi_dir/.venv/bin/python" ]] \
  && ok "OpenPI environment is present" \
  || fail "Missing OpenPI environment: $openpi_dir/.venv"
[[ -x "$sim_dir/.venv/bin/python" ]] \
  && ok "Isaac Sim environment is present" \
  || fail "Missing simulator environment: $sim_dir/.venv"
[[ -d "$checkpoint_dir/params" ]] \
  && ok "pi0.5-DROID checkpoint is present" \
  || fail "Missing pi0.5-DROID checkpoint: $checkpoint_dir"

for asset in scene1.usd scene2.usd scene3.usd franka_robotiq_2f_85_flattened.usd; do
  [[ -s "$sim_dir/assets/$asset" ]] \
    && ok "Simulator asset: $asset" \
    || fail "Missing simulator asset: $sim_dir/assets/$asset"
done

if [[ -d "$artifact_root" && -w "$artifact_root" ]]; then
  available_kib="$(df -Pk "$artifact_root" | awk 'NR==2 {print $4}')"
  available_gib=$((available_kib / 1024 / 1024))
  if (( available_gib >= 5 )); then
    ok "Artifact root has ${available_gib} GiB free: $artifact_root"
  else
    fail "Artifact root has less than 5 GiB free: $artifact_root"
  fi
else
  fail "Artifact root is not writable: $artifact_root"
fi

if [[ "$policy_gpu" == "$sim_gpu" ]]; then
  warn "Policy and simulator both select physical GPU $policy_gpu"
else
  ok "GPU split: policy=$policy_gpu, simulator=$sim_gpu"
fi

if nvidia-smi --query-gpu=index --format=csv,noheader >/dev/null 2>&1; then
  visible_gpu_ids="$(nvidia-smi --query-gpu=index --format=csv,noheader)"
  grep -qx "$policy_gpu" <<<"$visible_gpu_ids" \
    && ok "Policy GPU $policy_gpu is visible" \
    || fail "Policy GPU $policy_gpu is not visible"
  grep -qx "$sim_gpu" <<<"$visible_gpu_ids" \
    && ok "Simulator GPU $sim_gpu is visible" \
    || fail "Simulator GPU $sim_gpu is not visible"
else
  warn "nvidia-smi cannot query GPUs in this shell; verify at launch time"
fi

if (( require_policy )); then
  if timeout 2 bash -c "</dev/tcp/$policy_host/$policy_port" 2>/dev/null; then
    ok "Policy endpoint is reachable: $policy_host:$policy_port"
  else
    fail "Policy endpoint is not reachable: $policy_host:$policy_port"
  fi
fi

case "$streaming" in
  0) ok "WebRTC streaming is disabled" ;;
  1)
    case "$streaming_mode" in
      1)
        if [[ -n "${PUBLIC_IP:-}" ]]; then
          ok "WebRTC public endpoint is configured: $PUBLIC_IP"
        else
          fail "TRACK_A_STREAMING_MODE=1 requires PUBLIC_IP"
        fi
        warn "Public streaming endpoints have no built-in authentication; restrict them to the Mac client IP"
        ;;
      2)
        host_addresses="$(hostname -I 2>/dev/null || true)"
        ok "Private-network WebRTC enabled; server address(es): ${host_addresses:-unknown}"
        ;;
      *) fail "TRACK_A_STREAMING_MODE must be 1 or 2, got: $streaming_mode" ;;
    esac
    ok "Mac client requires TCP 49100 and UDP 47998 to reach this host"
    if command -v ss >/dev/null 2>&1; then
      if [[ -n "$(ss -ltnH 'sport = :49100' 2>/dev/null)" ]]; then
        fail "TCP 49100 is already in use"
      else
        ok "TCP 49100 is available"
      fi
      if [[ -n "$(ss -lunH 'sport = :47998' 2>/dev/null)" ]]; then
        fail "UDP 47998 is already in use"
      else
        ok "UDP 47998 is available"
      fi
    else
      warn "ss is unavailable; WebRTC port conflicts were not checked"
    fi
    ;;
  *) fail "TRACK_A_STREAMING must be 0 or 1, got: $streaming" ;;
esac

printf '\nSummary: %d failure(s), %d warning(s)\n' "$failures" "$warnings"
(( failures == 0 ))
