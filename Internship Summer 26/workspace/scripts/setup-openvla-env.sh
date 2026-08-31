#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${1:-openvla}"
case "$target" in
  openvla) repo="$workspace_dir/projects/openvla" ;;
  oft) repo="$workspace_dir/projects/openvla-oft" ;;
  *) echo "Usage: $0 {openvla|oft}" >&2; exit 2 ;;
esac

set -a
# shellcheck disable=SC1091
source "$workspace_dir/config/openvla.env"
set +a

[[ -d "$repo/.git" ]] || { echo "Missing repository: $repo" >&2; exit 1; }
available_kib="$(df -Pk "$workspace_dir" | awk 'NR==2 {print $4}')"
(( available_kib >= 25 * 1024 * 1024 )) || {
  echo "At least 25 GiB free is required to build an OpenVLA environment." >&2
  exit 1
}

export UV_CACHE_DIR="$OPENVLA_UV_CACHE_DIR"
if [[ ! -x "$repo/.venv/bin/python" ]]; then
  uv venv --python 3.10 "$repo/.venv"
fi
uv pip install --python "$repo/.venv/bin/python" -e "$repo"
uv pip install --python "$repo/.venv/bin/python" \
  -r "$repo/experiments/robot/libero/libero_requirements.txt" \
  -e "$workspace_dir/projects/openpi/third_party/libero"
uv pip install --python "$repo/.venv/bin/python" "mujoco==2.3.7"
uv pip install --python "$repo/.venv/bin/python" "tensorflow-metadata==1.15.0"
uv pip install --python "$repo/.venv/bin/python" "wandb==0.16.6"
uv pip install --python "$repo/.venv/bin/python" packaging ninja

# FlashAttention-2 requires Ampere or newer GPUs. RTX 8000 is Turing (SM 7.5),
# so the evaluation utilities use eager attention and FP16 on this host.
compute_capability="$(nvidia-smi --query-gpu=compute_cap --format=csv,noheader 2>/dev/null | head -n 1 || true)"
if [[ "$compute_capability" =~ ^(8|9|10|12)\. ]]; then
  uv pip install --python "$repo/.venv/bin/python" "flash-attn==2.5.5" --no-build-isolation
else
  echo "Skipping FlashAttention-2 for compute capability ${compute_capability:-unknown}."
fi

echo "Prepared $target environment: $repo/.venv"

