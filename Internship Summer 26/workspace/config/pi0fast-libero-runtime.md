# π0-FAST LIBERO runtime record

- Policy: `lerobot/pi0fast-libero`
- Exact policy revision: `840f4b503f4c09110421c33c810a85b6684fd658`
- FAST action tokenizer: `jadechoghari/tokenizer-lib-mean`
- Exact action-tokenizer revision: `79ae83e3cbd8786dcb84b628569f8d076ca8151e`
- Text tokenizer requested by the checkpoint: `google/paligemma-3b-pt-224`
- Public mirror used for tokenizer-only files: `leo009/paligemma-3b-pt-224`
- Exact mirror revision: `39996beb6fb17c5d16a50d3ef8f7a96ad9d03986`

The Google PaliGemma repository is gated. Only tokenizer/config files were taken
from the public mirror. They were verified byte-for-byte against Google's Hub
metadata before being linked into the expected cache namespace:

- `tokenizer.json` SHA-256: `ef6773c135b77b834de1d13c75a4c98ab7a3684ffd602d1831e1f1bf5467c563`
- `tokenizer.model` SHA-256: `8986bb4f423f07f8c7f70d0dbe3526fb2316056c17bae71b1ea975e77a168fc6`
- `added_tokens.json` Git blob: `ff9246e420971b10c510b39a0de289132c2bf23f`
- `config.json` Git blob: `b89393ba09b432265173f688b8a41a2c3c9e3e4c`
- `special_tokens_map.json` Git blob: `0c18fdd94629ea652e2ef36ed9a422474ad0a8e8`
- `tokenizer_config.json` Git blob: `960dcec0bccc6e594d865eceb63c8078e164cfb2`

Host compatibility overrides in `scripts/run-lerobot-libero.sh`:

- `--policy.dtype=float32` because RTX 8000/Turing has no native BF16 support.
- `--policy.compile_model=false` to avoid the checkpoint's training-time compile setting.
- The action tokenizer's bundled `bpe_tokenizer` needs a local
  `config.json` containing `{"model_type":"gpt2"}` with current Transformers;
  this selects the generic byte-level fast-tokenizer wrapper and does not alter
  tokenizer vocabulary or merges.

Validated smoke result: 1/1 success on LIBERO-10 task 0, seed 7, in 55.6 s.
Canonical output:
`/home/julnk0207/vla-artifacts/runs/libero-long-screening-10-v1/pi0fast_libero/smoke`
