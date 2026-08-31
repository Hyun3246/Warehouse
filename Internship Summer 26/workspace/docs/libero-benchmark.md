# LIBERO benchmark

## Selected protocol

The primary comparison is LIBERO-Long, named `libero_10` by LIBERO. It contains
10 long-horizon tasks. The full profile evaluates the same 50 fixed initial
states for every task, for **500 episodes per model**. This matches the default
rollout count in the pinned OpenPI LIBERO evaluator.

The profiles are deliberately separate:

| Profile | Tasks | Trials per task | Total episodes | Videos |
|---|---:|---:|---:|---|
| `smoke` | task 0 only | 1 | 1 | all |
| `pilot` | all 10 | 1 | 10 | all |
| `full` | all 10 | 50 | 500 | failures only |

`smoke` and `pilot` validate infrastructure. Only `full` is the reported
benchmark result. Task order and initial-state selection are deterministic;
the evaluator uses LIBERO's fixed initial states in index order.

Pinned simulator components:

- image: `vla/libero-sim:2026-08-18`
- LIBERO commit: `8f1084e3132a39270c3a13ebe37270a43ece2a01`
- robosuite 1.4.1, MuJoCo 3.2.3, Python 3.8
- environment render: 256 x 256; policy input: 224 x 224
- 10 no-op settling steps; action replanning every 5 steps
- LIBERO-Long horizon: 520 control steps

The initial model is the official `pi05_libero` checkpoint. Model inference and
simulation share physical GPU 1; the RTX 8000 has sufficient memory for both.
The policy server listens at `147.46.125.211:8002`, which is reachable from the
rootless simulator container. Use this same one-GPU allocation for every model
when comparing inference timing.

## Current prerequisite

The simulator image and harness are installed and the simulator-only smoke test
passes. Storage cleanup left about 60 GiB free, which clears the preflight
threshold for installing the initial `pi05_libero` checkpoint. The checkpoint
has not yet been downloaded. Continue using failure-only or disabled video for
full runs; writable `/data` storage is still required before retaining several
large model checkpoints or extensive video collections.

Check readiness at any time:

```bash
cd ~/vla-workspace
./scripts/libero-preflight.sh
```

The stricter check used by launchers is:

```bash
./scripts/libero-preflight.sh --require-model
```

## Running in tmux

After the checkpoint is installed, start both the policy server and evaluator
from one terminal:

```bash
cd ~/vla-workspace
./scripts/libero-tmux.sh start smoke
./scripts/libero-tmux.sh start pilot
./scripts/libero-tmux.sh start full
```

Run one profile at a time. The command creates a `vla-libero` tmux session with
two persistent windows:

- `policy`: the pi0.5-LIBERO WebSocket policy server
- `benchmark`: waits for the server, then runs the selected profile

Useful controls:

```bash
./scripts/libero-tmux.sh status
tmux attach -t vla-libero:benchmark
tmux attach -t vla-libero:policy
```

Inside tmux, `Ctrl-b d` detaches without stopping the run. Stop both windows
with:

```bash
./scripts/libero-tmux.sh stop
```

For a non-tmux run, start `scripts/run-pi05-libero-server.sh` in one terminal
and `scripts/run-libero.sh smoke` (or `pilot` / `full`) in another.

## Records and videos

Each launch creates a timestamped directory:

```text
$VLA_DATA_ROOT/runs/libero-long-v1/
  pi05_libero/YYYY-MM-DD/HH-MM-SS/
    manifest.json
    task-00/
      episode-00.metrics.json
      episode-00.steps.jsonl
      episode-00.mp4
    task-01/
      ...
```

`manifest.json` is updated atomically after every episode. It records protocol
settings, expected/completed episodes, success count, failure count, success
rate, and run status (`running`, `completed`, or `aborted`). This is the primary
file for monitoring and aggregate analysis.

Each `metrics.json` records the instruction, fixed initial-state index,
success/failure, failure reason, control steps, wall time, number of policy
requests, and client-observed inference latency (mean, median, p95, maximum).
Each `steps.jsonl` contains action-level timing, actions, rewards, and success.

The pilot saves every episode video. The full run saves only failed episodes to
limit storage. To suppress full-run videos entirely:

```bash
LIBERO_FULL_VIDEO_MODE=none ./scripts/libero-tmux.sh start full
```

For an optional live preview, enable streaming when the tmux session is
created. This adds a third `stream` window and updates one JPEG in place, so it
does not accumulate video data:

```bash
LIBERO_STREAMING=1 ./scripts/libero-tmux.sh start pilot

# On the Mac
ssh -L 8090:127.0.0.1:8090 julnk0207@SERVER_HOST
```

Then open `http://127.0.0.1:8090/libero-long-v1/_live/` on the Mac. The preview
server binds only to the server's loopback interface and is reachable through
the SSH tunnel. Streaming is disabled by default; saved MP4s remain available
under the same HTTP server while it is enabled.
