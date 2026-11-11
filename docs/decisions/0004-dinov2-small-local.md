# 0004 — DINOv2-small embeddings, local on CPU, whole-frame resize

- Status: accepted
- Date: 2026-10-16 (model choice re-checked 2026-10-19)
- Decided by: agent, approved by the user

## Context
Near-duplicate detection needs a visual-layout embedding; photos must not leave the machine.

## Options considered
1. **CLIP B/32** — captures semantic meaning rather than composition.
2. **DINOv2-small CLS** — composition/layout, small enough for CPU.
3. **DINOv2-base**, **DINOv2-small mean-of-patches** — compared 2026-10-19.

## Decision
DINOv2-small CLS from the 320 px thumbnail resized to 224×224 **without center crop** (shots that
differ only at the edges must still differ). On the user's 12 missed pairs none of the alternatives
was clearly better; mean-of-patches helped 4 neighbour cases but shifts the whole similarity scale.

## Consequences
DINOv2 does not tell people apart (different guest, same spot ≈ 0.88). That limit is addressed by
face identities ([0010](0010-face-identities-signal.md)) and the VLM judge
([0016](0016-vlm-judge-grey-zone-only.md)), not by another embedding.

## Evidence
[research/2026-10-19-grouping-tuning-4a.md](../research/2026-10-19-grouping-tuning-4a.md#round-2--look-back-2026-10-19).
