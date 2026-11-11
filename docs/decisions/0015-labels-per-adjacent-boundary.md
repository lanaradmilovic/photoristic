# 0015 — Ground truth as labels on adjacent-photo boundaries, keyed by sha256

- Status: accepted
- Date: 2026-10-22
- Decided by: the user (agreed plan of 2026-10-22)

## Context
Every grouping change was judged by eye on contact sheets; changes need a number.

## Options considered
1. **Label whole groups** — breaks when group ids change on re-grouping.
2. **Label each boundary between time-adjacent photos of one camera**, keyed by the two sha256.

## Decision
Option 2: survives re-grouping, re-ingesting and renamed outputs, and maps directly onto false
merges (dangerous) vs missed merges (review time). `cull.py score` prints P/R/F1 and `errors.jpg`.

## Consequences
Look-back joins ("photo 5 belongs with photo 2") cannot be labelled or scored.

## Evidence
[spec/labels.md](../spec/labels.md). 4a: 333 labels; score 319 correct, 4 false, 10 missed (F1 0.959).
