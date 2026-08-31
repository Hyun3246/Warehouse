# OpenVLA LIBERO-10 next steps

## Order

1. Finish the active π0.5-base 100-episode screening.
2. Build and test `openvla` first.
3. Run a 10-episode pilot. If inference and motion are healthy, run the
   100-episode screening (10 tasks x 10 initial states).
4. Treat `oft` as optional. Build and run it only after the OpenVLA result is
   secured and storage is rechecked.

## Models and protocol

- OpenVLA: `openvla/openvla-7b-finetuned-libero-10` (15.1 GB).
- OpenVLA-OFT: `moojink/openvla-7b-oft-finetuned-libero-10` (15.9 GB).
- Suite: `libero_10`; seed: 7; center crop: enabled.
- Pilot: one initial state per task (10 episodes).
- Screening: ten initial states per task (100 episodes).
- OFT uses its published L1 action head, third-person and wrist images,
  proprioception, and 8-action open-loop chunks.

Each repository has a separate environment because OFT requires a custom
Transformers fork. Both environments share the already validated LIBERO checkout.

## Commands (after the current benchmark finishes)

```bash
scripts/setup-openvla-env.sh openvla
scripts/run-openvla-libero.sh openvla pilot
scripts/run-openvla-libero.sh openvla screening

# Optional second model
scripts/setup-openvla-env.sh oft
scripts/run-openvla-libero.sh oft pilot
scripts/run-openvla-libero.sh oft screening
```

Do not start either evaluation while `vla-libero-base-screening` exists. Model
downloads occur on the first evaluation, so recheck free space immediately before
launch. Avoid downloading the optional RLDS datasets; pretrained evaluation does
not need them and they consume roughly another 10 GB.
