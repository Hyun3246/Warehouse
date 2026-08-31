#!/usr/bin/env bash
set -u

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${1:-openvla}"
requested_gpu_id="${2:-}"
case "$target" in
  openvla) repo="$workspace_dir/projects/openvla"; required_gib=22 ;;
  oft) repo="$workspace_dir/projects/openvla-oft"; required_gib=23 ;;
  *) echo "Usage: $0 {openvla|oft}" >&2; exit 2 ;;
esac

set -a
# shellcheck disable=SC1091
source "$workspace_dir/config/openvla.env"
set +a
gpu_id="${requested_gpu_id:-$OPENVLA_GPU_ID}"

failures=0
ok() { printf 'OK    %s\n' "$1"; }
fail() { printf 'FAIL  %s\n' "$1"; failures=$((failures + 1)); }
warn() { printf 'WARN  %s\n' "$1"; }

[[ -d "$repo/.git" ]] && ok "Repository is present: $repo" || fail "Missing repository: $repo"
[[ -x "$repo/.venv/bin/python" ]] && ok "Python environment is present" || fail "Run scripts/setup-openvla-env.sh $target"
[[ -f "$OPENVLA_LIBERO_CONFIG_PATH/config.yaml" ]] && ok "LIBERO path config is present" || fail "Missing LIBERO path config"

available_kib="$(df -Pk "$workspace_dir" | awk 'NR==2 {print $4}')"
available_gib=$((available_kib / 1024 / 1024))
(( available_gib >= required_gib )) && ok "${available_gib} GiB free" || fail "Need ${required_gib} GiB free; only ${available_gib} GiB remains"

if nvidia-smi --query-gpu=index --format=csv,noheader 2>/dev/null | grep -qx "$gpu_id"; then
  ok "GPU $gpu_id is visible"
else
  fail "GPU $gpu_id is not visible"
fi

if [[ "$gpu_id" == "1" ]] && tmux has-session -t vla-libero-base-screening 2>/dev/null; then
  warn "π0.5-base screening is still using the benchmark GPU; do not start OpenVLA yet"
fi

printf '\nSummary: %d failure(s)\n' "$failures"
(( failures == 0 ))

