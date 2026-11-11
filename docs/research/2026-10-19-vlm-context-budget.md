# VLM context budget: Qwen3.5-9B and Claude Haiku 5.5

Date: 2026-10-19. Confirm with one real request and read `usage.prompt_tokens`. Used by
[vlm-scoring.md](../spec/vlm-scoring.md).

## Qwen3.5-9B

Sources: the Hugging Face model card, `config.json`, `preprocessor_config.json`.

- **Architecture:** 32 layers; only 8 are full attention (4 KV heads × head_dim 256), the other 24
  are Gated DeltaNet linear attention with a fixed-size state. Native context 262,144 tokens. BF16
  weights ~19–20 GB (HF lists 10B parameters including the vision encoder).
- **Image tokens:** patch 16 × merge 2 ⇒ **one visual token per 32×32 px**; sides rounded to
  multiples of 32.

  | Preview size | Tokens per image |
  |---|---|
  | 768×512 | ≈ 384 |
  | 1024×683 | ≈ 672 |
  | 1536×1024 | ≈ 1,536 |

  The default processor cap is 16.7 MP per image, so an unresized NEF preview would cost ~16k
  tokens: **always resize client-side** (`vlm.image_long_edge`).
- **KV cache (own estimate):** only the 8 full-attention layers grow: 8 × 2 × 4 × 256 × 2 B ≈
  **32 KB per token** ⇒ 16k ≈ 0.5 GB, 32k ≈ 1 GB, 262k ≈ 8 GB (does not fit next to BF16 weights on
  a 24 GB L4). Linear-attention state adds ~50 MB per sequence.
- **vLLM:** the model card uses `--max-model-len 262144 --reasoning-parser qwen3`. Thinking is off
  per request with `extra_body={"chat_template_kwargs": {"enable_thinking": False}}`.
- **Non-thinking sampling** (model card): temperature 0.7, top_p 0.8, top_k 20, presence_penalty 1.5.

## Claude Haiku 5.5

Sources: the Claude vision docs and the Claude API reference.

- 1M-token context, 128K max output.
- **Image tokens:** ⌈W/28⌉ × ⌈H/28⌉ on the high-resolution tier (max 2576 px long edge / 4784
  tokens per image). 1024×683 ≈ 925 tokens.
- **Limits:** up to 600 images per request; with more than 20 images each must be ≤ 2000 px per
  side; max 5 MB per image (base64) on Bedrock; Bedrock and Google Cloud accept base64 only, with a
  request size below 32 MB.
- **Price on the Claude API:** $0.10 / $0.50 per MTok input / output for prompts ≤ 100K tokens.
  Bedrock pricing still to be checked.
- **Thinking:** on by default at effort `medium`; use `low` for scoring and leave room in `max_tokens`.

## Budget per group

Prompt ~1,000 + N × image (~680 Qwen / ~930 Haiku at 1024 px) + N × ~120 output.

| Qwen `--max-model-len` | Max photos per group (10 % margin) |
|---|---|
| 16,384 | ≈ 17 |
| 32,768 | ≈ 35 |

For Haiku the context is not the limit.
