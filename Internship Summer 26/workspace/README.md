# VLA Workspace

This repository is the control plane for model, simulator, dataset, and runtime
environments. Large artifacts live outside Git and are mounted into containers.

## Current host snapshot (2026-08-18)

- Ubuntu 22.04.4 LTS, glibc 2.35
- 6 x NVIDIA Quadro RTX 8000 (approximately 48 GB VRAM each)
- NVIDIA driver 535.161.07
- 251 GiB RAM
- Docker Engine 27.3.1 and user-scoped Compose 5.1.4 installed
- NVIDIA Container Toolkit 1.13.5 installed
- Rootless Docker enabled for this account
- User-scoped NVIDIA CDI enabled; CUDA 12.2 smoke test passed on GPU 1
- uv 0.11.32 installed under `~/.local/bin`
- Root NVMe: approximately 60 GB free after experiment cleanup
- `/data`: approximately 1.2 TB free, but not writable by this account

## Remaining infrastructure constraints

1. Ask an administrator to create a writable artifact directory on `/data`.
2. Upgrade the NVIDIA driver before adopting Isaac Sim 6.0. Isaac Sim 6.0 was
   tested with Linux driver 580.95.05; driver upgrades must be coordinated with
   other users because they can interrupt active GPU jobs.

Until `/data` storage is available, `~/vla-artifacts` can hold the initial
pi0.5-LIBERO checkpoint and controlled benchmark outputs. Do not install
multiple large checkpoints or enable all-video recording for a full run, and
keep at least 10 GiB free. Writable `/data` storage remains the proper target
for a multi-model comparison.

## First use

```bash
cd ~/vla-workspace
./scripts/doctor.sh
```

The GPU smoke test uses rootless Docker and NVIDIA CDI, selecting GPU 1:

```bash
docker compose --profile smoke run --rm gpu-smoke
```

The smoke image deliberately uses CUDA 12.2 so it can validate the currently
installed driver. It is not the final runtime for newer model stacks. Rootless
Docker currently stores images under `~/.local/share/docker`; relocate this to
the future `/data` allocation before pulling large images.

## Layout

```text
config/       Host-specific paths and GPU allocation
containers/   One image definition per incompatible software stack
projects/     Source checkouts; weights and datasets do not belong here
adapters/     Model/simulator observation and action boundaries
scripts/      Read-only diagnostics and setup helpers
docs/         Compatibility decisions and operational notes
```

See `docs/rootless-runtime.md` for runtime locations, restart commands, and CDI
regeneration after a driver change.

## Simulation environment

The isolated MuJoCo/LIBERO image is ready. Run its end-to-end smoke test with:

```bash
cd ~/vla-workspace
docker compose --profile sim run --rm libero-sim
```

See `docs/simulation.md` for pins, raw MuJoCo testing, interactive shells, and
output locations.

The primary standardized benchmark is LIBERO-Long (`libero_10`). See
`docs/libero-benchmark.md` for the pinned protocol, episode counts, tmux
commands, result layout, and the remaining checkpoint/storage prerequisite.

The earlier DROID simulation comparison remains available as an exploratory
secondary track in `config/track-a.env`; see `docs/track-a.md`.

Shared artifact storage is organized as:

```text
$VLA_DATA_ROOT/
  datasets/
  checkpoints/
  assets/
  runs/
  cache/huggingface/
  cache/uv/
  cache/jax/
  cache/torch/
  cache/omniverse/
```

Each upstream project keeps its native package manager and lockfile. OpenPI,
Octo, GR00T, MuJoCo/LIBERO, and Isaac are not merged into one Python environment.
