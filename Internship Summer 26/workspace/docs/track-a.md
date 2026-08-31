# Track A: zero-shot DROID simulation comparison

Track A evaluates installed DROID-compatible checkpoints without fine-tuning.
Its primary protocol is `droid-sim-12task-v1`, which reproduces the public
DreamZero-versus-pi0.5 `sim-evals` comparison:

- one fixed Isaac Lab scene containing a Rubik's Cube and red bowl;
- 12 frozen language instructions;
- 30 simulated seconds per episode (450 control steps at 15 Hz);
- one pilot trial or three full trials per instruction;
- model-native action horizons and camera inputs;
- qualitative pass/fail review from the saved rollout videos.

Protocol reference:
https://www.alexkoven.com/project/dreamzero_vs_pi0.5/

This is a reproducible simulator protocol. It is not the original DROID
paper's real-robot evaluation and not DreamZero's 40-task real-robot protocol.

## Configuration

- Versioned defaults: `config/track-a.env`
- Host paths, ports, and GPU allocation: `config/host.env`
- Policy GPU: physical GPU 1 by default
- Simulator/renderer GPU: physical GPU 2 by default
- Output: `$VLA_DATA_ROOT/runs/droid-sim-12task-v1/<model>/`

The installed pi0.5-DROID configuration records two model inputs: one external
camera and one wrist camera, each resized to 224 x 224. Its action horizon is 8.

Run the environment check without requiring a policy server:

```bash
cd /home/julnk0207/vla-workspace
./scripts/track-a-preflight.sh
```

## Run in tmux

The launcher creates `vla-track-a:policy` and `vla-track-a:benchmark`, waits for
the policy endpoint, and stops the policy after the benchmark command exits.

The pilot collects one trial for every prompt: 12 rollouts total.

```bash
TRACK_A_STREAMING=1 ./scripts/track-a-tmux.sh start pilot
```

After inspecting the pilot, the published full protocol collects three trials
for every prompt: 36 rollouts total.

```bash
TRACK_A_STREAMING=0 ./scripts/track-a-tmux.sh start full
```

Inspect or attach:

```bash
./scripts/track-a-tmux.sh status
tmux attach -t vla-track-a:benchmark
tmux attach -t vla-track-a:policy
```

Use `Ctrl-b d` to detach. Stop the complete session explicitly with:

```bash
./scripts/track-a-tmux.sh stop
```

## Records and review

All 12 tasks and their trials are saved under one timestamped run directory:

```text
YYYY-MM-DD/HH-MM-SS/
  manifest.json
  task-01/
    episode-0.mp4
    episode-0.steps.jsonl
    episode-0.metrics.json
    episode-0.review.json
  ...
  task-12/
```

`manifest.json` contains the frozen task definitions, expected episode count,
model/checkpoint identity, camera profile, action horizon, paired episode seeds,
and links to every artifact. It is updated after every episode.

Each episode produces at most one MP4 in its task directory. The evaluator does
not create additional `latest-task` or `latest-scene` video links.

Manual-protocol episodes finish with `success: null` and
`review_status: pending`. The old cube-in-bowl detector remains in the step
records only as a reference diagnostic; it never terminates or scores the 12
language tasks.

Review a video and record its verdict with:

```bash
./scripts/score-droid-sim-episode.py \
  /absolute/path/to/YYYY-MM-DD/HH-MM-SS \
  task-01 0 pass \
  --reviewer julnk0207 \
  --notes "Cube was released inside the bowl"
```

Use `fail` instead of `pass` when the behavior does not meaningfully satisfy
the instruction. The command updates the review file, episode metrics, and
aggregate manifest. It refuses to overwrite an existing review unless
`--replace` is provided.

For fair model comparisons, use the same `TRACK_A_RANDOM_SEED` and episode
count. Trial `N` always uses `TRACK_A_RANDOM_SEED + N`, providing a shared
initial-state key across tasks and models.

## Watch from a Mac

Streaming is optional and does not replace MP4 recording. Use the NVIDIA Isaac
Sim WebRTC Streaming Client matching Isaac Sim 5.0. A private-network or VPN
connection must allow TCP 49100 and UDP 47998.

```bash
TRACK_A_STREAMING=1 ./scripts/track-a-tmux.sh start pilot
```

Do not expose private mode directly to the public Internet. For a deliberately
public run, restrict both ports to the Mac source IP and set:

```bash
TRACK_A_STREAMING=1 TRACK_A_STREAMING_MODE=1 PUBLIC_IP=203.0.113.10 \
  ./scripts/track-a-tmux.sh start pilot
```

## Secondary three-scene diagnostic

The previous three-scene automatic benchmark remains available, but it is not
the primary published comparison protocol:

```bash
TRACK_A_PROTOCOL=three_scene \
TRACK_A_BENCHMARK_ID=droid-three-scene-v1 \
TRACK_A_PILOT_EPISODES=1 \
  ./scripts/track-a-tmux.sh start pilot
```

Its automatic relative-pose success rules remain provisional. A full
three-scene run is blocked until `TRACK_A_SCORING_VALIDATED=1` is supplied.

## Current limitations

- Qualitative success labels require human review; latency and trajectory
  diagnostics are automatic.
- `pi05_droid` currently uses the joint-velocity adapter. Other checkpoints
  need model-specific camera/action adapters and must record those settings.
- Do not download additional large checkpoints until writable `/data` storage
  is available.
