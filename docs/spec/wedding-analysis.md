# Wedding analysis: one wedding before and after the agency's cull

Every wedding the agency gives us twice (as handed over, and after their editor's cull) gets the
same analysis in the same shape, so that Claude agents can compare weddings and test claims
across them. Why this shape: practice for error analysis (open notes, then a fixed taxonomy, then
counts), for qualitative codebooks (definition, when to use, when not, examples, agreement
between coders) and for documents read by agents (small summary first, details on demand,
YAML front matter, the evidence of every claim marked). The folder is
[docs/weddings/](../weddings/README.md).

## Files

| File | Where | Written by | What |
|---|---|---|---|
| `wedding.json` | `docs/weddings/<id>/` | hand / agent | facts the code cannot know: camera roles, clock offsets, parts of the day, the couple's face identities |
| `<out>/analysis/reasons.jsonl` | output folder (OneDrive) | reviewers | one line per rejected photo: reason code, loss, confidence, note |
| `<out>/analysis/photos.csv` | output folder (OneDrive) | `cull.py analysis` | one row per photo, same columns for every wedding |
| `summary.json` | `docs/weddings/<id>/` | `cull.py analysis` | the numbers, same keys for every wedding |
| `analysis.md` | `docs/weddings/<id>/` | agent + user | the findings as numbered claims, from the template below |
| report HTML | output folder | anything | the user's view; generated, never the source |

`photos.csv` and `reasons.jsonl` stay with the photos (they name guests' frames and describe
them). `summary.json` and `analysis.md` hold only file names and numbers and go into git.

Run, after `cull.py agency --after <posle>` has written `agency_cull.json`:

```
.venv\Scripts\python cull.py analysis --output "<out>" --wedding docs\weddings\<id>
```

## wedding.json

```json
{
 "wedding": "glamur", "date": "2026-11-08", "editor": "Ksenija", "program": "Photo Mechanic 5",
 "reference_camera": "KNEZ",
 "cameras": [{"prefix": "LPZ_", "role": "second", "clock_offset_s": -298, "clock_checked": true}],
 "couple_identities": ["B", "C"], "couple_checked": false,
 "day_parts": [{"part": "couple", "start": "15:37", "end": "16:33", "cameras": ["KNEZ"]},
               {"part": "arrival", "start": "15:37", "end": "17:35"}]
}
```

- `prefix`: start of the file name (longest match wins). `clock_offset_s` is added to the
  camera's time to get the reference camera's time.
- `role`: `main` (follows the couple), `second`, `decor`, `guests`, `other`.
- `day_parts`: on the reference clock, `HH:MM`, start inclusive, end exclusive, `24:00` allowed.
  The first entry that matches the time and names this camera (or no camera) wins, so entries
  limited to cameras go first. Parts: `prep` (homes, until the church), `church`, `civil`,
  `formals` (posed family groups), `couple` (couple session), `arrival` (guests arriving, logo
  wall, table portraits), `reception_line` (congratulations), `first_dance`, `cake`, `party`,
  `other`.
- Any other key (`note`, `data`, `before`, `after`) is free text for the reader.

## reasons.jsonl

```json
{"file": "LPZ_3569.JPG", "primary": "EXPR", "secondary": "", "kept_alt": "LPZ_3570.JPG",
 "loss": "no", "conf": "high", "reviewer": "agent-part1", "codebook": 1,
 "note": "groom profile, serious; 3570 same pose with slight smile"}
```

Codes, `loss` and `conf` are defined in [codebook.md](../weddings/codebook.md); `codebook` is its
version. A photo judged twice keeps its first line. Notes describe what is seen, never who a
guest is.

## photos.csv

| Column | Meaning |
|---|---|
| `file`, `photo_id` | file name; id from `photos.json` |
| `camera`, `role` | prefix from wedding.json; its role (`other` when no prefix matches) |
| `time_camera`, `time_ref` | capture time on the camera's clock; on the reference clock |
| `day_part` | from wedding.json |
| `decision` | `kept`, `rejected`, `both` (in a kept folder and in the rejected one), `missing`, `ambiguous`, `unknown` |
| `group_id`, `group_size`, `segment_id` | the pipeline's group and segment |
| `has_people`, `n_faces` | person detection; faces found |
| `couple` | how many of the couple's identities are in the frame (0–2); empty without `couple_identities` |
| `prev_gap_s`, `prev_sim` | gap (s) and DINOv2 similarity to the previous frame of the same camera |
| `burst_id`, `burst_size`, `burst_pos` | chain of neighbours within `analysis.burst_gap_seconds` and at least `analysis.burst_similarity` (config.yaml); a lone frame is a burst of 1 |
| `reason` … `note` | from reasons.jsonl, empty for kept photos |

## summary.json

Rates count only `kept` and `rejected` photos. `{photos, rejected, rate}` is the unit of every
breakdown.

| Key | What |
|---|---|
| `schema`, `wedding`, `created`, `cull_source`, `params` | format version, the analysis parameters used |
| `counts`, `reject_rate` | photos per decision |
| `by_role`, `by_day_part`, `by_role_day_part` | rejection rate per role, part of the day, `role/part` |
| `near_identical_pairs` | adjacent frames of one burst: both kept, one rejected, both rejected |
| `bursts_by_size` | bursts of 2, 3–4, 5+: share kept, bursts with nothing kept |
| `lone_frames` | rejection rate of frames that are in no burst (not thinning) |
| `rules` | standard thinning rules against the agency: `drops`, `drops_agency_kept` (false rejects, the failure), `agency_rejects_caught` |
| `couple_in_frame` | rejection rate by number of the couple's identities in the frame |
| `cross_camera` | per non-main role: rejection rate when the main camera shot within `analysis.cross_camera_seconds`, and when not |
| `reasons` | `by_code`, `by_code_role`, `loss`, `conf`, `loss_yes` (file names), codebook versions |

Rules: `burst_keep_first` keeps the first frame of every burst; `burst_keep_half` keeps every
other frame from the first. A new rule is added in `culling/analysis.py` and every summary is
regenerated, so all weddings carry it.

## analysis.md template

```markdown
---
wedding: glamur
date: 2026-11-08
analysed: 2026-11-26
editor: Ksenija
program: Photo Mechanic 5
cameras: 4
photos_before: 3432
rejected: 962
codebook: 1
reviewed_by: six agent reviewers, spot check of 16 by the main agent
status: draft | checked by user | confirmed by agency
---
# <Wedding>: what the agency rejects

## Context        (the packages, cameras and roles, how the editor works, anything unusual)
## Numbers        (from summary.json; link it, quote only what the claims need)
## Reasons        (table of codes; how much to trust them)
## Findings       (the claims, see below)
## Losses         (rejects that a client might miss, checked against all cameras)
## Questions for the agency
## Limits
## Reproduce
```

Every finding is one claim with an id and its evidence:

```markdown
- **GLA-F03** The editor culls each camera alone, not "the better of two photographers".
  evidence: measured · `summary.json` cross_camera.second: 0.329 with main within 3 s, 0.364 without
  bears on: S5 · holds elsewhere: –
```

- id: three letters of the wedding, `F` and a number; never reused.
- evidence: `file` (read from the files, e.g. XMP), `measured` (a number in summary.json or
  photos.csv), `judged` (reviewers' or the user's eye), `said` (the agency said it, with the
  interview linked). Write the strongest one that applies.
- bears on: requirement ids from [requirements.md](../requirements.md) (S, C, G, K, B, N, W, R, Q).
- holds elsewhere: filled in by the comparison, e.g. `TAL-F02 yes`, `XYZ-F05 no`.
- An answer of the agency is added under the claim (`said: … [interview](…)`), the claim is
  not rewritten.

## Comparing weddings

[docs/weddings/README.md](../weddings/README.md) says how an agent compares them and keeps the
index of weddings and of claims that hold across them.
