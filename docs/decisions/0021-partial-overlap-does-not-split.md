# 0021 — A partial overlap of face identities does not split a group

- Status: rejected (the split; the flag stays, off)
- Date: 2026-11-11
- Decided by: the user, after review

## Context
Rule [0014](0014-group-definition-v2.md): a person added to or missing from a group photo is
another group. The pipeline let DINOv2 decide such pairs, because a partial overlap of face
identities ({A,B,C} vs {A,B,C,D}) was "no opinion".

## Options considered
1. **Partial overlap = different people** (`faces_partial_overlap_blocks: true`) — measured on the
   4a and Talici 1 labels: false merges 9 → 6, missed merges 45 → 77, about 3–4 % more groups.
2. **Narrow it by face size or face count** — checked on the changed pairs; neither separates a real
   change from a face that was not recognised.
3. **Keep partial overlap as "no opinion"** (today's behaviour).

## Decision
Option 3. Most of the new splits are the bride or groom not recognised in one frame (head turned)
or a background person walking in, which the labels count as one group; the gain is 3 false merges
out of 1043 labelled pairs. The flag stays in the code, off, so it can be re-measured when face
recognition or the labels change.

## Consequences
- Pairs like Talici 1's group of 3 men vs 4 men still merge when DINOv2 says so; the rule of 0014
  for added/missing people is not enforced by the pipeline.
- Phase 3 must keep this in mind: a group may mix two group photos that differ by one person, and
  the safety rules ([0019](0019-safety-rules-in-code.md)) have to protect them.

## Evidence
[research/2026-11-11-partial-overlap-block.md](../research/2026-11-11-partial-overlap-block.md).
