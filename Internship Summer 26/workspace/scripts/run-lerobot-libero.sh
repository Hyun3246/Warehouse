#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo="$workspace_dir/projects/lerobot"
target="${1:-smolvla}"
profile="${2:-pilot}"
gpu_id="${3:-3}"

case "$target" in
  smolvla)
    model_id="HuggingFaceVLA/smolvla_libero"
    model_name="smolvla_libero"
    extra_args=(--policy.n_action_steps=1)
    ;;
  vla_jepa)
    model_id="lerobot/VLA-JEPA-LIBERO"
    model_name="vla_jepa_libero"
    extra_args=(--policy.enable_world_model=false --policy.torch_dtype=float16)
    ;;
  pi0fast)
    model_id="lerobot/pi0fast-libero"
    model_name="pi0fast_libero"
    # RTX 8000 (Turing) has no native BF16 support. Override the Hub BF16 and compile settings.
    extra_args=(--policy.max_action_tokens=256 --policy.n_action_steps=10 --policy.dtype=float32 --policy.compile_model=false)
    ;;
  *)
    echo "Usage: $0 {smolvla|vla_jepa|pi0fast} {smoke|pilot|screening} [gpu-id]" >&2
    exit 2
    ;;
esac

case "$profile" in
  smoke)
    episodes=1
    task_args=(--env.task_ids=[0])
    ;;
  pilot)
    episodes=1
    task_args=()
    ;;
  screening)
    episodes=10
    task_args=()
    ;;
  *)
    echo "Usage: $0 {smolvla|vla_jepa|pi0fast} {smoke|pilot|screening} [gpu-id]" >&2
    exit 2
    ;;
esac

session="vla-${target}-libero-${profile}"
if tmux has-session -t "$session" 2>/dev/null; then
  echo "Session already exists: $session" >&2
  exit 1
fi

output_dir="/home/julnk0207/vla-artifacts/runs/libero-long-screening-10-v1/$model_name/$profile"
mkdir -p "$output_dir"

command=(
  env
  "CUDA_VISIBLE_DEVICES=$gpu_id"
  MUJOCO_GL=egl
  "MUJOCO_EGL_DEVICE_ID=$gpu_id"
  PYOPENGL_PLATFORM=egl
  HF_HOME=/home/julnk0207/vla-artifacts/cache/huggingface
  HF_HUB_OFFLINE=1
  TRANSFORMERS_OFFLINE=1
  "$repo/.venv/bin/lerobot-eval"
  "--policy.path=$model_id"
  --env.type=libero
  --env.task=libero_10
  "${task_args[@]}"
  --env.max_parallel_tasks=1
  --env.init_states=true
  --env.hard_reset=true
  --env.control_mode=relative
  "--eval.n_episodes=$episodes"
  --eval.batch_size=1
  --seed=7
  "--output_dir=$output_dir"
  "${extra_args[@]}"
)

printf -v quoted_command '%q ' "${command[@]}"
tmux new-session -d -s "$session" -c "$repo" "$quoted_command >$output_dir/console.log 2>&1"

echo "Started $target LIBERO-10 $profile on GPU $gpu_id: $session"
echo "Output: $output_dir"
