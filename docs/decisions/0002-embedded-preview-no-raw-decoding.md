# 0002 — Use the embedded JPEG preview, never decode RAW

- Status: accepted
- Date: 2026-10-16
- Decided by: agent, approved by the user

## Context
~2,500 NEF per wedding on a CPU-only workstation. The VLM and embeddings need at most 1536 px.

## Options considered
1. **RAW decode** (`rawpy.postprocess`) — accurate, slow.
2. **Embedded preview** (`rawpy.extract_thumb`) — Nikon embeds a full-size JPEG.

## Decision
Option 2: fast and good enough for judging. Orientation comes from the **NEF's** IFD0, because
Nikon's embedded preview is stored unrotated. JPGs use their own EXIF orientation.

## Consequences
A body that embeds only a small preview would show up in `original_preview_w/h`; the fallback
(RAW decode at half size) is not implemented.

## Evidence
talici 4a: every NEF had a 5568×3712 preview ([spec/ingest.md](../spec/ingest.md)).
