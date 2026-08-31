#!/usr/bin/env bash
set -euo pipefail

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${1:-openvla}"
profile="${2:-screening}"
requested_gpu_id="${3:-}"

set -a
# shellcheck disable=SC1091
source "$workspace_dir/config/openvla.env"
set +a
gpu_id="${requested_gpu_id:-$OPENVLA_GPU_ID}"

case "$target" in
  openvla)
    repo="$workspace_dir/projects/openvla"
    model_id="$OPENVLA_MODEL_ID"
    model_name="openvla_7b_libero_10"
    extra_args=()
    ;;
  oft)
    repo="$workspace_dir/projects/openvla-oft"
    model_id="$OPENVLA_OFT_MODEL_ID"
    model_name="openvla_oft_libero_10"
    extra_args=(
      --use_l1_regression True
      --use_diffusion False
      --use_film False
      --num_images_in_input 2
      --use_proprio True
      --num_open_loop_steps 8
    )
    ;;
  *) echo "Usage: $0 {openvla|oft} [pilot|screening] [gpu-id]" >&2; exit 2 ;;
esac

case "$profile" in
  pilot) trials="$OPENVLA_PILOT_TRIALS" ;;
  screening) trials="$OPENVLA_SCREENING_TRIALS" ;;
  *) echo "Usage: $0 {openvla|oft} [pilot|screening] [gpu-id]" >&2; exit 2 ;;
esac

"$workspace_dir/scripts/openvla-preflight.sh" "$target" "$gpu_id"
if [[ "$gpu_id" == "1" ]] && tmux has-session -t vla-libero-base-screening 2>/dev/null; then
  echo "π0.5-base screening is still running; refusing to contend for GPU $gpu_id." >&2
  exit 1
fi

session="vla-${target}-libero-${profile}"
tmux has-session -t "$session" 2>/dev/null && { echo "Session already exists: $session" >&2; exit 1; }

output_dir="$OPENVLA_OUTPUT_ROOT/libero-long-screening-10-v1/$model_name"
mkdir -p "$output_dir/logs" "$output_dir/rollouts"
if [[ -e "$repo/rollouts" && ! -L "$repo/rollouts" ]]; then
  echo "Refusing to replace non-symlink rollout directory: $repo/rollouts" >&2
  exit 1
fi
ln -sfn "$output_dir/rollouts" "$repo/rollouts"

command=(
  env
  "CUDA_VISIBLE_DEVICES=$gpu_id"
  "MUJOCO_GL=egl"
  "MUJOCO_EGL_DEVICE_ID=$gpu_id"
  "PYOPENGL_PLATFORM=egl"
  "HF_HOME=$OPENVLA_HF_HOME"
  "LIBERO_CONFIG_PATH=$OPENVLA_LIBERO_CONFIG_PATH"
  "PYTHONPATH=$workspace_dir/projects/openpi/third_party/libero"
  "$repo/.venv/bin/python"
  experiments/robot/libero/run_libero_eval.py
  --pretrained_checkpoint "$model_id"
  --task_suite_name "$OPENVLA_TASK_SUITE"
  --num_trials_per_task "$trials"
  --seed "$OPENVLA_SEED"
  --center_crop "$OPENVLA_CENTER_CROP"
  --local_log_dir "$output_dir/logs"
  --use_wandb False
  "${extra_args[@]}"
)

printf -v quoted_command '%q ' "${command[@]}"
tmux new-session -d -s "$session" -c "$repo" "$quoted_command >$output_dir/console.log 2>&1"
echo "Started $target LIBERO $profile session: $session"
echo "Output: $output_dir"

