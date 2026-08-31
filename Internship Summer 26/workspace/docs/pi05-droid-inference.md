# pi0.5-DROID inference

The official OpenPI `pi05_droid` checkpoint is installed for inference on GPU
1. The server uses port 8001 because another process already owns port 8000.

## Start the policy server

```bash
cd /home/julnk0207/vla-workspace
./scripts/run-pi05-droid-server.sh
```

Keep that terminal open. Model restoration takes several seconds; the server is
ready when it reports that it is listening on `0.0.0.0:8001`.

## Test without a robot

In a second terminal:

```bash
cd /home/julnk0207/vla-workspace
./scripts/smoke-pi05-droid.sh
```

The smoke client sends random DROID-shaped observations and writes timing data
to `/home/julnk0207/vla-artifacts/runs/pi05-droid-smoke/timing.parquet`.

## Paths and overrides

- Source: `/home/julnk0207/vla-workspace/projects/openpi`
- Environment: `/home/julnk0207/vla-workspace/projects/openpi/.venv`
- Checkpoint cache: `/home/julnk0207/vla-artifacts/cache/openpi`
- Defaults: `/home/julnk0207/vla-workspace/config/host.env`

Override `OPENPI_GPU_ID`, `OPENPI_PORT`, or `OPENPI_HOST` in the environment when
needed. Moving to `/data` later only requires copying the artifact tree and
updating `VLA_DATA_ROOT` and `OPENPI_DATA_HOME` in `config/host.env`.

## Validated result

The synthetic end-to-end test passed on an NVIDIA Quadro RTX 8000. Three timed
requests averaged approximately 0.99 seconds end-to-end and 0.83 seconds inside
the policy. Real control still requires mapping the simulator or robot cameras,
joint state, gripper state, and returned action chunk to the DROID interface.

The downloaded `pi05_droid` checkpoint follows the real DROID joint-velocity
control example. The rollout launcher switches the installed simulator to a
velocity drive, clips arm commands to the real-DROID range, and records the two
policy camera views. This velocity path is experimental; the simulator's
upstream recommended configuration remains the separate
`pi05_droid_jointpos` checkpoint.

## Run a recorded simulator rollout

Start the policy server first, then run this in a second terminal:

```bash
cd /home/julnk0207/vla-workspace
./scripts/run-pi05-droid-rollout.sh 1 1 450
```

The arguments are `EPISODES SCENE MAX_STEPS`. Videos are written below
`/home/julnk0207/vla-artifacts/runs/pi05-droid-rollouts/`.

### Validated rollout

Scene 1 was validated for a complete 450-frame, 30-second rollout. The policy
approached and grasped the cube, moved it over the red bowl, and released it
inside. Recordings are stored as one MP4 per episode in its timestamped run
directory.

## Automatically switch tasks

Keep the policy server running, then execute:

```bash
cd /home/julnk0207/vla-workspace
./scripts/run-pi05-droid-suite.sh 1 450 sequential
```

The arguments are `EPISODES_PER_TASK MAX_STEPS ORDER`. `ORDER` may be
`sequential` or `random`. The launcher automatically starts a clean Isaac Sim
process for each task. This adds a short loading pause between tasks, but avoids
an Isaac Sim 5.0 scene-reload hang. It switches through:

1. Put the cube in the bowl.
2. Put the can in the mug.
3. Put the banana in the bin.

For WebRTC streaming to a client on your laptop, use:

```bash
DROID_STREAMING=1 DROID_TASK_SEED=42 ./scripts/run-pi05-droid-suite.sh 1 450 random
```

This sets Isaac Lab's private-network WebRTC mode (`LIVESTREAM=2`) while keeping
the host headless. Do not add `--no-headless` on a server without an X display;
that causes the `Failed to acquire IWindowing interface` error. To display a
window directly on a server graphical desktop instead, use `DROID_HEADLESS=0`.

Set `DROID_TASK_SEED` to reproduce a random task order. Videos and a JSON
manifest are written under
`/home/julnk0207/vla-artifacts/runs/pi05-droid-suite/`, with one MP4 per
episode. The manifest contains the exact path for each recording.
