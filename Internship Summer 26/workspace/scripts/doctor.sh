#!/usr/bin/env bash
set -u

failures=0
warnings=0

ok() { printf 'OK    %s\n' "$1"; }
warn() { printf 'WARN  %s\n' "$1"; warnings=$((warnings + 1)); }
fail() { printf 'FAIL  %s\n' "$1"; failures=$((failures + 1)); }

workspace_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
host_env="$workspace_dir/config/host.env"

if [[ -r /etc/os-release ]]; then
  . /etc/os-release
  ok "OS: ${PRETTY_NAME:-unknown}"
else
  fail "Cannot read /etc/os-release"
fi

if command -v nvidia-smi >/dev/null 2>&1; then
  driver_version="$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -n1)"
  gpu_count="$(nvidia-smi --query-gpu=name --format=csv,noheader | wc -l)"
  ok "NVIDIA driver $driver_version; $gpu_count GPU(s) visible"
else
  fail "nvidia-smi is unavailable"
fi

if command -v docker >/dev/null 2>&1; then
  ok "$(docker --version)"
  if docker info >/dev/null 2>&1; then
    ok "Docker daemon is accessible"
    if docker info --format '{{json .SecurityOptions}}' | grep -q rootless; then
      ok "Docker is running in rootless mode"
    fi
    if docker info --format '{{json .CDISpecDirs}}' | grep -q '/home/julnk0207/.config/cdi'; then
      ok "User-scoped NVIDIA CDI directory is configured"
    elif docker info --format '{{json .Runtimes}}' | grep -q nvidia; then
      ok "NVIDIA Docker runtime is registered"
    else
      warn "No NVIDIA runtime or user-scoped CDI directory detected"
    fi
    docker_root="$(docker info --format '{{.DockerRootDir}}')"
    [[ "$docker_root" == /home/* ]] && warn "Docker images use root storage: $docker_root"
  else
    fail "Docker daemon is not accessible by user $(id -un)"
  fi
else
  fail "Docker is not installed"
fi

if command -v git-lfs >/dev/null 2>&1; then
  ok "$(git-lfs version)"
else
  fail "Git LFS is not installed"
fi

if command -v uv >/dev/null 2>&1; then
  ok "$(uv --version)"
else
  warn "uv is not installed yet"
fi

if [[ -r "$host_env" ]]; then
  # The file contains paths and simple scalar settings only.
  set -a
  # shellcheck disable=SC1090
  . "$host_env"
  set +a
  if [[ -n "${VLA_DATA_ROOT:-}" && -d "$VLA_DATA_ROOT" && -w "$VLA_DATA_ROOT" ]]; then
    ok "Artifact root is writable: $VLA_DATA_ROOT"
    [[ "$VLA_DATA_ROOT" == /home/* ]] && warn "Artifact root is temporary home storage; do not download large datasets or checkpoints"
  else
    fail "VLA_DATA_ROOT is missing or not writable: ${VLA_DATA_ROOT:-unset}"
  fi
else
  fail "Create config/host.env from config/host.env.example"
fi

root_free_gib="$(df -Pk / | awk 'NR==2 {printf "%d", $4/1024/1024}')"
if (( root_free_gib < 100 )); then
  warn "Root filesystem has only ${root_free_gib} GiB free; keep artifacts on /data"
else
  ok "Root filesystem has ${root_free_gib} GiB free"
fi

printf '\nSummary: %d failure(s), %d warning(s)\n' "$failures" "$warnings"
(( failures == 0 ))
