# 0012 — No face-size filter for identity clustering

- Status: rejected
- Date: 2026-11-11
- Decided by: the user, after before/after sheets

## Context
Blurry 24–40 px background faces formed the largest identity on T3/T4 ("garbage identities").

## Options considered
1. **`faces.identity_min_face_size: 48`** (32 and 40 also tried) — smaller faces stay unknown.
2. **No filter.**

## Decision
Option 2. The filter cleaned the identities but regressed grouping: 4a score 319 → 316, T3
9349–9356 split, T4 first dance 2 → 3 groups. The couple's faces in wide shots are 40–48 px and lose
the "same people" relaxation. 32/40 px change almost nothing. Branch deleted, outputs restored.

## Consequences
Do not re-propose a plain size filter: size cannot separate a background guest from a distant
couple. A fix for garbage identities would need another feature (blur, position, co-occurrence).

## Evidence
[research/2026-10-21-faces.md](../research/2026-10-21-faces.md#face-size-filter-experiment-2026-11-11-rejected);
`groups.prefilter.json` in each output.
