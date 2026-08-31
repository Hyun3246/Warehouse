#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
set -a
# shellcheck disable=SC1091
source "$workspace_dir/config/libero.env"
# shellcheck disable=SC1091
source "$workspace_dir/config/host.env"
set +a

exec docker run --rm \
  --device "nvidia.com/gpu=${LIBERO_SIM_GPU_ID:-2}" \
  -e MUJOCO_GL=egl \
  -e MUJOCO_EGL_DEVICE_ID=0 \
  -e PYOPENGL_PLATFORM=egl \
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics \
  -v "${VLA_DATA_ROOT}:/artifacts" \
  "$LIBERO_IMAGE" \
  python /opt/smoke/libero_smoke.py
