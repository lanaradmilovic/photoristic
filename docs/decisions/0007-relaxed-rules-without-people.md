# 0007 — Relaxed grouping for photos without people; RT-DETR as person detector

- Status: accepted
- Date: 2026-10-19 (detector replaced 2026-10-21)
- Decided by: the user

## Context
Decor, food and detail shots are over-split by the strict people thresholds, but the dangerous
DINOv2 failure ("different person, same spot") cannot happen without people.

## Options considered
1. **One rule set for all photos.**
2. **A person gate + `nopeople_*` thresholds** (45 s / 0.80, look-back 0.86).

Detector: YOLOS-tiny first, RT-DETR v2 r18vd now.

## Decision
Option 2. YOLOS-tiny was replaced by RT-DETR: it hallucinated a person on the lemonade jars (9883)
and missed the dip-kiss couple (0131). Score threshold 0.6 separates real people in odd poses
(≥ 0.60) from hallucinations on blurry close-ups (≤ 0.59) on 4a; boxes < 2 % of the frame are ignored.

## Consequences
No-people look-back stays at 0.86: good and bad merges both sit at 0.853.

## Evidence
`config.yaml` comments under `people`;
[research/2026-10-19-grouping-tuning-4a.md](../research/2026-10-19-grouping-tuning-4a.md#measured-limits-for-people-photos-2026-10-19-review).
