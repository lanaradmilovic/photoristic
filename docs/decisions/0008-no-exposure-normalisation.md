# 0008 — No exposure normalisation before embedding

- Status: rejected
- Date: 2026-10-21
- Decided by: agent, from measurement

## Context
On Talici 2 the same cufflinks shot dark vs bright scored 0.61 and split.

## Options considered
1. **Scale each thumbnail to a target mean brightness** (`embedding.exposure_target`, gain clamp 4.0).
2. **Leave thumbnails as they are.**

## Decision
Option 2. With target 0.47 the pair moved only 0.61 → 0.62 and grouping got two more singles. The
code was removed (commit 93ed377) instead of being kept off by default.

## Consequences
Exposure jumps still break DINOv2 similarity; do not re-propose a global brightness fix.

## Evidence
Commits 19932c0, 93ed377.
