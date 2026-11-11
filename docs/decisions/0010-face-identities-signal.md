# 0010 — Face identities as a second grouping signal

- Status: accepted
- Date: 2026-10-21 (kept with current settings after the user's review 2026-11-11)
- Decided by: the user, after review

## Context
DINOv2 cannot separate "same couple, new pose" (wanted, 0.72–0.90) from "different guest, same
spot" (forbidden, 0.88). Threshold tuning cannot fix feature overlap.

## Options considered
1. **More threshold tuning / a bigger embedding** — measured not to help ([0004](0004-dinov2-small-local.md)).
2. **Face identities** (SCRFD + AuraFace, ONNX on CPU, Apache 2.0, local): same known people →
   relaxed thresholds; no identity in common → no extended/look-back/no-people join; bursts never blocked.
3. **VLM on every pair** — too slow and needs the server.

## Decision
Option 2. The user rated 39 of 47 face-driven changes on Talici 2–4 good, 4 bad. Settings stay:
`identity_threshold` 0.40, `identity_merge_threshold` 0.45, `min_identity_faces` 10,
`faces_lookback_similarity_threshold` 0.70. The agent's earlier proposal to tighten look-back to
≥ 0.85 and `min_identity_faces` to 15 was dropped: it was based on the old group rule.

## Consequences
Garbage identities (blurry background faces) exist. A partial overlap ({A,B,C} vs {A,B,C,D}) does
not block a join yet ([todo](../todo.md)). `faces.enabled: false` reproduces the old output exactly.

## Evidence
[research/2026-10-21-faces.md](../research/2026-10-21-faces.md); commit b8235da.
