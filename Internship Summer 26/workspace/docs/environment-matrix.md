# Environment matrix

| Stack | Runtime family | Python | Accelerator baseline | Status |
|---|---|---:|---|---|
| Host diagnostics | Host | system | driver 535.161.07 | Ready |
| GPU smoke test | Rootless Docker + CDI | n/a | CUDA 12.2 image | Passed on GPU 1 |
| OpenPI pi0.5-DROID | Native upstream environment | 3.11.15 | JAX 0.5.3 / Torch 2.7.1+cu126 on GPU 1 | Ready; synthetic DROID inference passed |
| Octo 1.5 | Separate legacy JAX environment | 3.10 upstream | JAX 0.4.20/CUDA 11 upstream pin | Planned |
| LIBERO/MuJoCo | Rootless Docker | 3.8.20 | EGL on GPU 1 | Ready; reset/render/step passed |
| GR00T N1.7 | Separate upstream environment/container | 3.12 upstream | CUDA 12.8 upstream | Blocked by driver decision |
| Isaac Sim 6.0 | NVIDIA container | 3.12 | tested Linux driver 580.95.05 | Blocked by driver upgrade |

## Policy

- Exact versions come from upstream lockfiles or container tags.
- Every image is built and tested independently.
- Every source checkout records its commit SHA.
- Containers receive only the GPUs assigned to their workload.
- Downloaded artifacts and caches are stored under `VLA_DATA_ROOT`.
- No project may silently install packages into the host Python environment.

## Deployment order

1. Obtain writable `/data` storage before downloading large artifacts.
2. Decide and schedule the host driver upgrade.
3. Create the OpenPI and MuJoCo/LIBERO environments.
4. Add GR00T and Isaac after the driver upgrade.
5. Add Octo as a separately pinned legacy comparison environment.
