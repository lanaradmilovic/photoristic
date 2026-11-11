# 0020 — VLM judge out of grouping for now; the VLM goes to scoring (phase 3)

- Status: accepted (supersedes [0016](0016-vlm-judge-grey-zone-only.md))
- Date: 2026-11-11
- Decided by: the user

## Context
0016 required the judge to be measured against labels before it influences grouping. First real
run on 4a (Qwen3.5-9B 4-bit on a T4): prompt v1 48 of 56 correct (7 pipeline decisions broken, 2
fixed, all errors false merges); a stricter prompt v2 26 of 56 (28 broken, mostly false splits on
background people). The pipeline alone: 52–53 of 56.

## Options considered
1. **Tune the prompt further (v3)** — ~17 min of server time per try; the bias swings with wording.
2. **Try a stronger model** — needs g6 capacity or another host.
3. **Park the judge; use the VLM for picking the best photo in a group (phase 3).**

## Decision
Option 3. The judge does not beat the pipeline, and a false merge is the dangerous error under the
hard rule. Grouping stays DINOv2 + faces + time; the VLM effort moves to phase 3. The judge code
(`cull.py judge`, prompt v1) stays as a measuring tool, so it can be re-run when a stronger model
is available.

## Consequences
- Grouping errors reach phase 3 unchanged; phase 3 must not trust the model to notice a mixed group
  (the same weakness showed here), so the code safety rules ([0019](0019-safety-rules-in-code.md))
  carry that.
- Retry the judge (and a v3 prompt limiting "person added/missing" to posed group photos) when the
  full model on g6 runs.

## Evidence
[research/2026-11-11-judge-first-real-run.md](../research/2026-11-11-judge-first-real-run.md).
