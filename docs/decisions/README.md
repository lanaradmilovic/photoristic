# Decisions

One file per decision: why we chose this and not the alternatives. Read the relevant ones
**before** changing behaviour, so a rejected idea is not tried again.

Rules:
- New decision → copy [_template.md](_template.md) to the next number, add a row below.
- A decision is never deleted or rewritten. When it changes, write a new one that supersedes it and
  change only the old one's `Status` line.
- Rejected ideas that were measured get their own record (status `rejected`).
- Current threshold values live in `config.yaml`; a decision records why, not the live value.

| # | Decision | Status | Date |
|---|---|---|---|
| [0001](0001-nef-jpg-one-photo.md) | NEF and JPG with the same name are one photo | accepted | 2026-10-16 |
| [0002](0002-embedded-preview-no-raw-decoding.md) | Embedded JPEG preview, never decode RAW | accepted | 2026-10-16 |
| [0003](0003-camera-by-serial-group-per-camera.md) | Camera by EXIF serial; group per camera | accepted | 2026-10-16 |
| [0004](0004-dinov2-small-local.md) | DINOv2-small, local CPU, whole-frame resize | accepted | 2026-10-19 |
| [0005](0005-time-next-to-similarity.md) | Keep capture time next to similarity | accepted | 2026-10-19 |
| [0006](0006-lookback-and-boundary-refinement.md) | Look-back, mean drift guard, best candidate, refinement | accepted | 2026-10-19 |
| [0007](0007-relaxed-rules-without-people.md) | Relaxed rules without people; RT-DETR detector | accepted | 2026-10-19 |
| [0008](0008-no-exposure-normalisation.md) | Exposure normalisation before embedding | **rejected** | 2026-10-21 |
| [0009](0009-no-group-size-split.md) | Do not split groups by size | accepted | 2026-10-21 |
| [0010](0010-face-identities-signal.md) | Face identities as a second grouping signal | accepted | 2026-10-21 |
| [0011](0011-unknown-face-does-not-stand-in.md) | An unknown face does not stand in for a known person | accepted | 2026-11-11 |
| [0012](0012-no-face-size-filter.md) | Face-size filter for identity clustering | **rejected** | 2026-11-11 |
| [0013](0013-group-definition-v1.md) | Group = interchangeable frames, wide vs tight separate | superseded by 0014 | 2026-10-19 |
| [0014](0014-group-definition-v2.md) | Group = same main people, same moment, same place | accepted | 2026-11-11 |
| [0015](0015-labels-per-adjacent-boundary.md) | Labels on adjacent-photo boundaries, keyed by sha256 | accepted | 2026-10-22 |
| [0016](0016-vlm-judge-grey-zone-only.md) | VLM judge only for the 0.80–0.90 grey zone | superseded by 0020 | 2026-10-23 |
| [0017](0017-segments-gap-300s.md) | Day segments at pauses > 300 s | accepted | 2026-11-11 |
| [0018](0018-swappable-vlm-client-own-server.md) | Own vLLM server, swappable client, no framework | accepted | 2026-10-16 |
| [0019](0019-safety-rules-in-code.md) | Safety rules in code, never left to the model | accepted | 2026-10-19 |
| [0020](0020-vlm-judge-parked.md) | VLM judge out of grouping for now; VLM to scoring | accepted | 2026-11-11 |
| [0021](0021-partial-overlap-does-not-split.md) | Partial overlap of face identities splits a group | **rejected** | 2026-11-11 |
