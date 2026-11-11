# Day segments

Status: implemented (`culling/segments.py`, header strips in `culling/report.py`). Decision: [0017](../decisions/0017-segments-gap-300s.md). Measurements: [research](../research/2026-10-22-segments.md).

A wedding day is shot in parts with very different rhythms: preparations, family formals,
the church, the couple session, speeches, the first dance, the party. `culling/segments.py`
finds those parts without any model: per camera, photos are sorted by capture time and a new
segment starts wherever the pause between two neighbours is longer than `segments.gap_seconds`.
Photos without a capture time (or that failed ingest) go to one segment `unknown`.
Segments with fewer than `segments.min_photos` photos get the flag `tiny` but are never merged.
`prepare` and `group` run it after grouping; on its own:

```bash
.venv\Scripts\python cull.py segments --output D:\cull\2024-06-15 --sheets
```

This writes `segments.json`, prints one table row per segment and, with `--sheets`, one contact
sheet per segment in `segments_sheets/<segment_id>.jpg` (up to `sheet_max_thumbs` thumbnails
sampled evenly in time, each with the file number and clock time). The report shows a header
strip before the first group of every segment (id, time span, photos, groups, share without
people, main identities, link to the sheet). The segments are the input for later per-segment
grouping profiles and for a VLM that names the part of the day.

**`segments.json`:** `{created, gap_seconds, min_photos, n_segments, n_tiny, n_unknown_photos,
groups_crossing, segments: [segment…]}`.

| Segment field | Meaning |
|---|---|
| `segment_id` | `S01`, `S02`, … in camera order then time order; `unknown` for the undated photos |
| `camera_id`, `start`, `end`, `duration_seconds` | Camera and time span (`null` for `unknown`) |
| `n_photos`, `photo_ids` | Photos in capture order; `unknown` also has `reasons` (`no_timestamp` / `ingest_error`) per photo |
| `group_ids` | Groups from `groups.json` whose first photo lies in the segment |
| `flags` | `tiny` (fewer than `min_photos`), `unknown` |
| `stats.median_gap_s`, `stats.p90_gap_s`, `stats.burst_share` | Rhythm: median and 90th percentile of the gaps between neighbours, share of gaps under 2 s (`null` with one photo) |
| `stats.no_people_share` | Share of photos without a person (`people.json`; `null` without it) |
| `stats.median_faces`, `stats.identities` | Median faces per photo and the known identities with their photo counts, top 10 (`identities.json`; `null` / `[]` without it) |
| `stats.portrait_share` | Share of portrait-orientation frames |
| `stats.n_groups`, `stats.n_groups_crossing` | Groups entirely inside the segment, and groups with photos on both sides of a boundary (should be 0; the top-level `groups_crossing` lists them) |
