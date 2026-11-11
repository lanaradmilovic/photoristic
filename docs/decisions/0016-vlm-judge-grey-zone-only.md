# 0016 — VLM judge only for the 0.80–0.90 grey zone, measured before it is used

- Status: accepted
- Date: 2026-10-21 (implemented 2026-10-23)
- Decided by: the user

## Context
After faces, the remaining ambiguous pairs (profiles, backs, small faces) need a model that sees
both frames. A VLM call on every pair is slow, and the server runs only during work sessions.

## Options considered
1. **VLM on every adjacent pair.**
2. **VLM only on pairs with similarity in [0.80, 0.90) that faces do not decide**, sent as one
   side-by-side image with a strict JSON schema.
3. **Per-segment grouping profiles** — still a direction; needs segments first ([0017](0017-segments-gap-300s.md)).

## Decision
Option 2, and its verdicts are **not used by grouping** until they are compared with labels.

## Consequences
~690 calls across the five folders, ~40 % redundant (joined bursts, repeated look-back anchors).
The first real run needs the user's server/model choice.

## Evidence
[research/2026-10-23-judge-dry-run.md](../research/2026-10-23-judge-dry-run.md), [spec/vlm-judge.md](../spec/vlm-judge.md).
