# 0017 — Day segments at pauses > 300 s; no time rule for the missed cuts

- Status: accepted
- Date: 2026-11-11
- Decided by: the user, after reviewing the 180 s vs 300 s sheets

## Context
Segments (parts of the day) are input for per-segment grouping profiles and VLM classification.
The agent recommended 180 s on 2026-10-22.

## Options considered
1. **180 s** — makes the 4 real cuts that 300 s misses, but also 6 superfluous ones.
2. **300 s.**
3. **600 s** — glues whole parts of the day (one 316-photo segment).

## Decision
300 s. Pause lengths of real and superfluous cuts overlap completely (189–258 s vs 191–266 s), so no
threshold separates them; the 4 missed cuts need content-based splitting (VLM segment classification).

## Consequences
Code merged into `main` 2026-11-11. Tiny segments (< 5 photos) are only flagged.

## Evidence
[research/2026-10-22-segments.md](../research/2026-10-22-segments.md).
