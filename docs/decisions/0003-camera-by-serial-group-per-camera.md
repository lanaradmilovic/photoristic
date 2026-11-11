# 0003 — Identify the camera by EXIF serial and group per camera

- Status: accepted
- Date: 2026-10-16
- Decided by: agent, approved by the user

## Context
Every wedding has two photographers. Folder layouts vary between weddings, and the two cameras'
clocks are not synchronized.

## Options considered
1. **Camera by folder** — breaks on arbitrary layouts.
2. **Camera by EXIF serial** (`BodySerialNumber`, then `MakerNote SerialNumber`, then make+model with a warning).
3. **Merge both cameras on one timeline** — impossible without clock sync.

## Decision
Option 2, and grouping runs per camera, because timestamps of different cameras cannot be compared.

## Consequences
The same moment shot by both photographers lands in two groups (costs review time, never a photo).
Cross-camera matching would need clock-offset estimation; not planned.

## Evidence
[spec/ingest.md](../spec/ingest.md), [spec/grouping.md](../spec/grouping.md).
