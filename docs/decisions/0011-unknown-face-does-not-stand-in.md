# 0011 — An unknown face does not stand in for a missing known person

- Status: accepted
- Date: 2026-11-11
- Decided by: the user

## Context
In Talici 1 8026–8030 the bride in profile is unidentified, so `{A,B}` vs `{B}` + unknown does
not count as "same people" and the session splits.

## Options considered
1. **`faces_same_allows_unknown: true`** — merges 8026–8030, but on 4a also joins the couple
   walking in (two unknown guests) with the altar sequence, and vows close-ups with unrelated frames.
2. **`false`** — keeps the split.

## Decision
Option 2. An unknown face may be the next guest in a hug line; a wrong merge risks a photo, a
missed merge only costs review time.

## Evidence
[research/2026-10-21-faces.md](../research/2026-10-21-faces.md#trade-offs-seen).
