# LIBERO-10 screening results

Collected from `libero-long-screening-10-v1` artifacts. All primary results use 10 tasks and 10 episodes per task.

## Overall results

| Rank | Model | Successes | SR | Wilson 95% CI |
|---:|---|---:|---:|---:|
| 1 | VLA-JEPA LIBERO | 98/100 | 98% | 93.0–99.4% |
| 2 | OpenVLA-OFT LIBERO-10 | 96/100 | 96% | 90.2–98.4% |
| 3 | π0.5-LIBERO | 93/100 | 93% | 86.3–96.6% |
| 4 | π0-FAST LIBERO | 87/100 | 87% | 79.0–92.2% |
| 5 | OpenVLA-7B LIBERO-10 | 47/100 | 47% | 37.5–56.7% |
| 6 | SmolVLA LIBERO | 34/100 | 34% | 25.5–43.7% |
| 7 | π0.5-base | 0/100 | 0% | 0.0–3.7% |

## Per-task successes

Each cell is successes out of 10 episodes.

| Model | T0 | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| VLA-JEPA LIBERO | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 9 | 9 | 98 |
| OpenVLA-OFT LIBERO-10 | 9 | 10 | 10 | 10 | 10 | 10 | 10 | 9 | 8 | 10 | 96 |
| π0.5-LIBERO | 10 | 10 | 10 | 10 | 9 | 10 | 10 | 10 | 5 | 9 | 93 |
| π0-FAST LIBERO | 10 | 10 | 9 | 9 | 7 | 9 | 9 | 10 | 4 | 10 | 87 |
| OpenVLA-7B LIBERO-10 | 7 | 7 | 6 | 5 | 3 | 7 | 5 | 4 | 1 | 2 | 47 |
| SmolVLA LIBERO | 0 | 3 | 2 | 10 | 0 | 6 | 7 | 1 | 0 | 5 | 34 |
| π0.5-base | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Task index

- T0: put both the alphabet soup and the tomato sauce in the basket
- T1: put both the cream cheese box and the butter in the basket
- T2: turn on the stove and put the moka pot on it
- T3: put the black bowl in the bottom drawer of the cabinet and close it
- T4: put the white mug on the left plate and put the yellow and white mug on the right plate
- T5: pick up the book and place it in the back compartment of the caddy
- T6: put the white mug on the plate and put the chocolate pudding to the right of the plate
- T7: put both the alphabet soup and the cream cheese box in the basket
- T8: put both moka pots on the stove
- T9: put the yellow and white mug in the microwave and close it

## Validation runs

Smoke and pilot runs validated execution only; their small samples are not primary benchmark scores.

| Model | Stage | Result |
|---|---|---:|
| π0.5-LIBERO | pilot | 10/10 |
| π0.5-base | pilot | 0/10 |
| SmolVLA LIBERO | smoke | 0/1 |
| SmolVLA LIBERO | pilot | 4/10 |
| π0-FAST LIBERO | smoke | 1/1 |
| π0-FAST LIBERO | pilot | 9/10 |
| VLA-JEPA LIBERO | smoke | 1/1 |
| VLA-JEPA LIBERO | pilot | 9/10 |

## Interpretation limits

- This is the reduced 100-episode screening profile, not the 500-episode, 50-trials-per-task full profile.
- Runs used the same LIBERO-10 task order, seed 7, fixed initial states, hard resets, and 10 trials per task.
- OpenPI, OpenVLA, and LeRobot policies required different evaluator/runtime stacks. Treat comparisons as controlled screening results, not a bit-identical reproduction of every paper's official environment.
- The π0.5-base result uses LIBERO normalization with the general base checkpoint; its 0% is the intended post-training-effect baseline.

## Provenance

- VLA-JEPA LIBERO: `runs/libero-long-screening-10-v1/vla_jepa_libero/screening/eval_info.json`
- OpenVLA-OFT LIBERO-10: `runs/libero-long-screening-10-v1/openvla_oft_libero_10/rollouts/2026_08_19`
- π0.5-LIBERO: `runs/pi0.5-libero/pi05_libero/2026-08-19/02-30-22/manifest.json`
- π0-FAST LIBERO: `runs/libero-long-screening-10-v1/pi0fast_libero/screening/eval_info.json`
- OpenVLA-7B LIBERO-10: `runs/libero-long-screening-10-v1/openvla_7b_libero_10/rollouts/2026_08_19`
- SmolVLA LIBERO: `runs/libero-long-screening-10-v1/smolvla_libero/screening/eval_info.json`
- π0.5-base: `runs/libero-long-screening-10-v1/pi05_base/2026-08-19/07-16-39/manifest.json`
