# Session log

Append-only. One entry per session: date, what changed, what was decided, test count, what is
still open. Measurements go into [research/](research/), decisions into [decisions/](decisions/);
link them here instead of copying.

## Session 1 — 2026-10-16
- Phases 0–2 implemented (ingest, DINOv2 embeddings, grouping, report); 22 tests.
- First real run on talici 4a (334 NEF, one camera): NEF ingest works; AppleDouble `._` files now
  skipped; thresholds retuned (round 1, [research](research/2026-10-19-grouping-tuning-4a.md)).
- Decisions [0001](decisions/0001-nef-jpg-one-photo.md)–[0003](decisions/0003-camera-by-serial-group-per-camera.md), [0018](decisions/0018-swappable-vlm-client-own-server.md).

## Session 2 — 2026-10-19
- Diagnosed the user's 12 missed pairs, compared 4 embedding models, added look-back; then
  A+B+C+D (rounds 2–3, [research](research/2026-10-19-grouping-tuning-4a.md)). Person detection and
  `nopeople_*` rules. 27 tests.
- VLM context budget researched ([research](research/2026-10-19-vlm-context-budget.md)).
- Decisions [0004](decisions/0004-dinov2-small-local.md)–[0007](decisions/0007-relaxed-rules-without-people.md), [0013](decisions/0013-group-definition-v1.md), [0019](decisions/0019-safety-rules-in-code.md).

## Session 3 — 2026-10-21
- Ran all five talici folders ([datasets](datasets.md)). Exposure normalisation tried and removed
  ([0008](decisions/0008-no-exposure-normalisation.md)); size split turned off ([0009](decisions/0009-no-group-size-split.md)).
- Face identities as a grouping signal, commit b8235da ([research](research/2026-10-21-faces.md),
  [0010](decisions/0010-face-identities-signal.md)). 54 tests.

## Session 3b — 2026-10-22 / 23 (agents, separate branches)
- Faces analysis on Talici 2–4 (no code). Labelling tool + `score` on branch `labels` (7e3ffde,
  [0015](decisions/0015-labels-per-adjacent-boundary.md)). Day segments on branch `segments`
  ([research](research/2026-10-22-segments.md)). VLM judge dry-run on branch `judge` (7253579,
  [research](research/2026-10-23-judge-dry-run.md), [0016](decisions/0016-vlm-judge-grey-zone-only.md)); 118 tests.

## Session 4 — 2026-11-10 / 11
- The user labelled 4a (333 pairs): 319 correct, 4 false merges, 10 missed (F1 0.959).
- Group rule changed ([0014](decisions/0014-group-definition-v2.md) supersedes [0013](decisions/0013-group-definition-v1.md)); VLM prompt aligned (f4fec57).
- Faces review: 39/47 good, settings kept ([0010](decisions/0010-face-identities-signal.md), [0011](decisions/0011-unknown-face-does-not-stand-in.md)); face-size filter rejected ([0012](decisions/0012-no-face-size-filter.md)).
- Segments: 300 s kept ([0017](decisions/0017-segments-gap-300s.md)).
- Market research on complaints about existing culling tools ([research](research/2026-11-10-culling-complaints.md), in Serbian).

## Session 5 — 2026-11-11
- Documentation restructured on branch `docs`: short `CLAUDE.md`, `docs/` with plan, todo, log,
  decisions (ADRs), spec, research, datasets; `PLAN.md` removed, `README.md` shortened. No code changes.
