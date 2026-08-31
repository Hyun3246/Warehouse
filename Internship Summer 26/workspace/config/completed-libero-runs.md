# Completed LIBERO benchmark runs

This file records the immutable model identifiers and canonical result artifacts
needed to reproduce completed runs. Cached weights may be removed to reclaim
local storage; benchmark outputs under `vla-artifacts/runs` must be retained.

| Model | Checkpoint / exact revision | Episodes | Successes | Success rate | Canonical result |
|---|---|---:|---:|---:|---|
| π0.5-LIBERO | `gs://openpi-assets/checkpoints/pi05_libero` | 100 | 93 | 93.0% | `/home/julnk0207/vla-artifacts/runs/pi0.5-libero/pi05_libero/2026-08-19/02-30-22/manifest.json` |
| π0.5-base | `gs://openpi-assets/checkpoints/pi05_base` | 100 | 0 | 0.0% | `/home/julnk0207/vla-artifacts/runs/libero-long-screening-10-v1/pi05_base/2026-08-19/07-16-39/manifest.json` |
| OpenVLA-7B LIBERO-10 | `openvla/openvla-7b-finetuned-libero-10@80970322773f81baa2e22fe495d0487b93a05cfa` | 100 | 47 | 47.0% | `/home/julnk0207/vla-artifacts/runs/libero-long-screening-10-v1/openvla_7b_libero_10/logs/EVAL-libero_10-openvla-2026_08_19-18_12_10.txt` |
| OpenVLA-OFT LIBERO-10 | `moojink/openvla-7b-oft-finetuned-libero-10@95220f9a3421a7ff12d4218e73d09ade830fa9a3` | 100 | 96 | 96.0% | `/home/julnk0207/vla-artifacts/runs/libero-long-screening-10-v1/openvla_oft_libero_10/logs/EVAL-libero_10-openvla-2026_08_19-17_12_58.txt` |

## Exclusions

- The OpenVLA-base output stamped `2026_08_19-17_12_58` is an invalid aborted
  60-artifact run and must not be included in aggregate results.
- The OpenVLA-base output stamped `2026_08_19-17_21_04` is a separate 10-episode
  pilot and must not be added to the 100-episode full run.
