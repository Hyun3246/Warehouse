# Headless simulation environment

The `libero-sim` service is a standalone simulation client. Policy frameworks
belong in separate containers and can later communicate with this client over a
small policy-server interface.

## Pinned stack

| Component | Version |
|---|---|
| Base runtime | CUDA 12.2.2 / Ubuntu 22.04 |
| Python | 3.8.20 |
| MuJoCo | 3.2.3 |
| robosuite | 1.4.1 |
| LIBERO | `8f1084e3132a39270c3a13ebe37270a43ece2a01` |
| Torch | 1.11.0 CPU-only (LIBERO metadata/state loading) |
| Renderer | Headless EGL on physical GPU 1 |

The MuJoCo and robosuite pins match the current OpenPI LIBERO client reference.
The simulator does not contain an OpenPI, Octo, or other policy runtime.

## Commands

Build or rebuild:

```bash
cd ~/vla-workspace
docker compose --profile sim build libero-sim
```

Test raw MuJoCo GPU rendering:

```bash
docker compose --profile sim run --rm libero-sim \
  python /opt/smoke/mujoco_smoke.py
```

Reset and step LIBERO Spatial task 0:

```bash
docker compose --profile sim run --rm libero-sim
```

Open an interactive shell:

```bash
docker compose --profile sim run --rm libero-sim bash
```

## Outputs

Smoke-test images are written to:

```text
~/vla-artifacts/runs/sim-smoke/mujoco.png
~/vla-artifacts/runs/sim-smoke/libero-spatial-task-0.png
```

The host artifact directory is mounted at `/artifacts` inside the container.
LIBERO datasets, when provisioned later, belong under
`~/vla-artifacts/datasets/libero` or the future `/data` replacement.

## Expected warnings

LIBERO's pinned stack may print warnings about robosuite private macros and the
deprecated `gym` package. These do not affect the validated reset, camera
rendering, or action-step path. Do not independently upgrade Gym, NumPy,
robosuite, or MuJoCo inside this image; change the pins and rerun both smoke
tests together.

