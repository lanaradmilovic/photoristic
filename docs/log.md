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
- AWS setup started by the user, guided step by step ([aws-setup.md](aws-setup.md)): GPU quota
  approved (8 vCPU, Frankfurt), launch fails with "Insufficient capacity" for g6/g5 in all three
  zones. Reliability for the client (stop/start may fail) left open.
- Later the same day: `g4dn.xlarge` (T4) runs 4-bit Qwen3.5-9B via the tunnel on port 8001 (0e84459).

## Session 6 — 2026-11-11
- First real VLM judge run on 4a, two prompts ([research](research/2026-11-11-judge-first-real-run.md)):
  v1 48/56, v2 26/56, pipeline 52–53/56. v2 rejected (kept in the research note), code stays on v1.
- Judge parked, the VLM moves to phase 3 scoring ([0020](decisions/0020-vlm-judge-parked.md),
  supersedes [0016](decisions/0016-vlm-judge-grey-zone-only.md)).
- Partial overlap of face identities as a split: implemented behind `faces_partial_overlap_blocks`,
  measured on 4a + Talici 1 labels (false merges 9 → 6, missed 45 → 77), left off
  ([research](research/2026-11-11-partial-overlap-block.md), [0021](decisions/0021-partial-overlap-does-not-split.md)). 119 tests.

- **2026-11-11 — review and merge.** Code review of `grouping-partial-overlap` and `segments`; fixed
  the label-save race, Esc in the lightbox, judge resume across prompts (prompt hash), tunnel hint
  port, duplicate segment bars, stale `segments.json` / sheets, segment order past S99, and a
  segments failure no longer stops the report. All branches are in `main`; segments spec:
  [spec/segments.md](spec/segments.md). Smaller findings: [todo.md](todo.md).

## Session 7 — 2026-11-11
- Phase 3 implemented on branch `scoring`: `culling/ranking.py`, `cull.py rank`, keep / maybe in
  `report.html`, `tests/test_ranking.py` (166 tests). Code splits groups into variants, the model
  orders one variant, nothing is rejected ([0022](decisions/0022-variants-in-code-model-ranks.md),
  [spec](spec/vlm-scoring.md)).
- Dry-run on all five folders, no server: keeps 72 % at the defaults
  ([research](research/2026-11-11-ranking-variants-dry-run.md)).
- First real `rank` run on 4a (T4, image limit on the server raised from 2 to 8): 53 of 53 valid
  answers in 8.5 min, but a reversed-order check shows position bias, same winner in 15 of 53
  ([research](research/2026-11-12-ranking-first-real-run.md)). Winners not usable; next steps in todo.

## Session 8 — 2026-11-13 / 14
- `g6.xlarge` (L4) set up with the full Qwen3.5-9B; three start fixes in
  [aws-setup.md](aws-setup.md). `config.yaml` now names the full model.
- Full model, same ranking prompt: still position-biased (same winner in both orders 12 of 53).
  Each photo judged alone + ranking in code: order-independent and stable across image sizes,
  but ties in ~55 % of variants ([research](research/2026-11-14-ranking-full-model-and-per-photo.md)).
  Not yet in `ranking.py`; ground truth needed first.
- "Describe each photo, then choose" in both orders: 15 of 53 stable, the bias moved to the last
  photo (same research note).

## Session 9 — 2026-11-15
- Everything up to here committed and pushed on `scoring` (24bd703).
- Four-steps answers analysed: the winner is fixed in step 2 and the criteria are invented per
  answer. New flow tested on the 27B: fixed checks answered `A / B / same` in both orders,
  agreement decided in code. Consistent (identical pairs clean, synthetic blur and exposure found),
  but a winner in only 10 of 53 variants
  ([research](research/2026-11-15-report-prompt-both-orders.md)). `ranking.py` unchanged.

## Session 10 — 2026-11-17
- Plan for a feedback meeting with the agency on the grouping: they correct our groups instead of
  labelling ([0023](decisions/0023-agency-corrects-our-groups.md)).
- New `cull.py meeting` / `meeting-score` and `score --labels` (`culling/meeting.py`,
  [spec](spec/labels.md#agency-meeting-page)); checked in headless Chrome on synthetic photos.
- Draft `data/meeting/meeting.json` from metadata (20 disputed pairs of 5 kinds, 3 excerpts:
  4a S01, Talici 1 S01, Talici 4 S05); the user still has to look at it. Branch `agency-meeting`.
- 2026-11-18: pick page for the meeting: one-click reasons and a note per group, `--sample` (a
  chosen few groups, short rules), `--picks-file` (the agency's own file), `pick-score --compare`
  ([spec](spec/labels.md#best-photo-picks)). Draft `data/meeting/picks_sample.json`: 17 groups of
  4a by kind of decision, from metadata, g0025 included at the user's request.
- 2026-11-19: the sample can ask "would the other photo do?" (`ask` in the sample, `swap_ok` in the
  picks). Asked on the four two-photo groups of 4a where no saved check of the model finds a
  difference (g0020, g0040, g0044, g0139). Added from the saved answers of the model: g0008 (the
  yawn the user picked against the model's `expression`), g0050 and g0075 (the model is sure:
  stable in both orders, three models agree), g0146 (report and per-photo score disagree), g0126
  (every frame "eyes closed", scores 9). g0060 is a contradiction, not a control: `sharpness` is
  `B` in both orders, i.e. always the second photo shown. Sample: 23 groups, 78 photos. Label server sends `Cache-Control: no-store` (a rebuilt page was shown
  from the browser cache).

## Session 11 — 2026-11-20
- Meeting with the agency held on 2026-11-19 (Peđa, Ksenija). Summary from the two transcripts and
  the saved answers: [interview 3](interviews/2026-11-19-pedja-ksenija-grupisanje-i-izbor.md),
  [numbers](research/2026-11-19-agency-meeting-answers.md). Main message: drop the bad and the
  identical, do not pick one best; Peđa kept 59 of 78 photos. Grouping excerpts were not reviewed.
- File-number gaps of Talici: at least 3,050 shot, 2,575 present, all five folders alike
  ([research](research/2026-11-19-file-number-gaps.md)).

## Session 12 — 2026-11-23
- The user listened to the recording of the 2026-11-19 meeting again and dictated Peđa's comment
  for every photo of the two pages. Written down as
  [the photo-by-photo record](interviews/2026-11-19-pedja-slika-po-slika.md) (M1–M20, X1–X13,
  P1–P23), checked against the saved answers and contact sheets of the photos. Her notes are
  the hand-written transcript and the primary source; the automatic transcript only adds
  detail and never overrides them (the differences are listed at the end of the record).
- New [requirements.md](requirements.md): numbered rules for scope, groups, how many frames stay,
  what is a bad frame, which frame to prefer, editing wishes; ten open questions with safe
  defaults. Linked from `CLAUDE.md`.
- Measured: DINOv2 similarity and the number of frames around a pair do not separate "one" from
  "both"; his cuts and confirmed groups overlap in similarity; two of three cuts are look-back
  joins ([research](research/2026-11-23-meeting-choices-vs-signals.md)).
- Question page for Peđa: the meeting page got a third step type, `questions`, where two examples
  that were answered differently stand side by side with what he said then
  ([0024](decisions/0024-contradictions-side-by-side.md), [spec](spec/labels.md#agency-meeting-page)).
  Eight questions in `data/questions/meeting.json`; checked in the Browser pane of the desktop app,
  which opens localhost. `cull.py` now prints UTF-8 also when its output is piped (`meeting-score`
  crashed on "č").
- 2026-11-24: the user resolved three questions from the recording (guests: two stay two, many
  are selected; "few" and "many" count the frames of one moment; all photos are Peđa's, Đole's
  are not in the folders). [requirements.md](requirements.md#resolved) updated, the question page
  is down to five questions.
- How the program sees the two pairs of the "exactly the same" question: equal similarity, and
  the right result for the second pair only by accident. A crop around the couple separates the
  two pairs (patches 0.88 against 0.65) but not "one" from "both" over twenty pairs
  ([research](research/2026-11-24-same-or-not-two-pairs.md)).
- Everything committed and pushed on `agency-meeting` (baaaa95).
- New group rule decided by the user: [0025](decisions/0025-group-definition-v3.md) replaces 0014.
  Labels prepared for re-checking: the `same` labels outside bursts were removed from `labels.json`
  of 4a and Talići 1 (the old files are `labels.before-v3.json`), so the label tool stops only at
  them.
- Decision still to write: the selection step ([todo](todo.md)).

## Session 13 — 2026-11-25

- The user re-labelled 4a for [0025](decisions/0025-group-definition-v3.md); the agent reviewed all
  333 pairs on contact sheets (7 changes accepted, 3 rejected). The agent then labelled the 392
  open pairs of Talići 1 from thumbnails; the user disputed 14.
- The agent's answers on the disputed pairs were not consistent (raised arm, kiss seconds later,
  turned body, scenery). One list of checks was written and applied to every discussed pair:
  [0026](decisions/0026-labelling-checks.md) (proposed).
- Measured: the current grouping scores as well as the best similarity-and-gap rule fitted on the
  new labels (649 of 710, 310 of 333); pairs 2 s apart or less are nearly always the same moment;
  the errors are the kinds of pair the labellers disagreed on
  ([research](research/2026-11-25-labels-v3-and-signal-ceiling.md)).
- Proposed direction, not decided: no more threshold tuning, frames dropped only inside tight
  "same picture" sets, taste-dependent pairs marked `unsure`, shorter look-back for photos with
  people ([todo](todo.md)).
- Question page: four questions added (`nova-poza`, `druga-strana`, `prostor`, `sme-da-izbaci`, each with two photo examples),
  nine in all; [requirements Q11–Q14](requirements.md#open-questions). The definition as it was is
  `data/questions/meeting.before-2026-11-25.json`. The page was validated with the page builder,
  not opened in a browser.
- Found: a second `cull.py label` on port 8765 starts without an error while the first server keeps
  answering, so the browser showed the other album ([spec](spec/labels.md#what-a-label-is)).
- Committed on `agency-meeting`, merged into `main` (fast-forward, 185 tests pass) and pushed (b8adef3).
- Implemented what does not wait for Peđa's answers, on branch `grouping-v3`
  ([0027](decisions/0027-lookback-and-burst-variants.md),
  [research](research/2026-11-25-lookback-and-burst-variants.md)):
  `faces_lookback_similarity_threshold` 0.70 → 0.82 (both look-back joins Peđa cut are gone, the one
  he confirmed stays; labels 310 → 310 and 649 → 648) and the new `ranking.variant_max_gap_seconds`
  2 s (of Peđa's 59 picked photos 11 instead of 20 cannot be `keep`; keeps 79 → 91 % on 4a,
  68 → 83 % on Talići 1). A look-back window for photos with people was tried and dropped.
  4a and Talići 1 were regrouped; the groups as they were are `groups.before-0027.json`.
  `ranking.json` of 4a is from the old variants.

## 2026-11-26 — Glamur: the grouping measured on a four-camera JPG wedding

- New dataset ([datasets](datasets.md#glamur)): 3,432 JPG, four cameras. `prepare` unchanged
  thresholds, 80 min; new `--exclude FOLDER` for `prepare` / `ingest` skips the montage folder
  ([spec](spec/ingest.md)). Branch `glamur-measurement` (from `grouping-v3`).
- The agent labelled 1,904 boundaries in two blind passes (parallel agent passes, protocol in the
  output folder). Score: 1,561 of 1,763 (88.5 %), 91 false merges, 111 missed, 141 unsure
  ([research](research/2026-11-26-glamur-grouping.md)).
- Found: the camera clocks differ by 68 s and 298 s; guest line-ups with the couple at one spot
  are merged (one group of 56 photos holds about eleven line-ups); in-camera crops share the
  capture time of their source; across cameras the same moment has low similarity.
- For the user: review page of 120 pairs (`cull.py meeting --output <out>/review`), contact
  sheets of 60 groups (`group_sheets/`).

## 2026-11-26 — Glamur: what the agency's editor rejects

- The agency gave Glamur before and after the cull (`svadbe/1-glamur/pre`, `posle`). The editor
  works in Photo Mechanic 5 (colour class 1 = reject), camera by camera; 962 of 3,428 rejected.
- Six agent reviewers gave a reason for every reject; whole-image quality does not separate kept
  from rejected, face sharpness picks her frame at chance, and burst-thinning rules drop more of
  her keeps than her rejects ([research](research/2026-11-26-glamur-cull.md)).
- Local report with a gallery and the user's own marks: `<out>/posle-analiza/index.html`.

## 2026-11-27 — One format for the before/after analyses of weddings

- Every wedding the agency gives before and after the cull gets the same analysis, so agents can
  compare them ([0028](decisions/0028-wedding-analysis-format.md), [spec](spec/wedding-analysis.md)):
  `docs/weddings/<id>/` holds `wedding.json` (roles, clocks, parts of the day), `summary.json`
  and `analysis.md` (numbered claims with evidence); `photos.csv` stays in the output folder.
- New `cull.py analysis --output <out> --wedding docs/weddings/<id>`; config section `analysis`.
- [Codebook](weddings/codebook.md) of reason codes with definitions and examples; version 2
  splits `DUP` (`SAME`), hidden faces (`FACE`) and versions (`VERSION`).
- Glamur repacked: [analysis](weddings/glamur/analysis.md), 15 claims; the numbers match the
  research of 2026-11-26. New: by part of the day, the second photographer loses 54 % in the
  first dance (main 22 %); keeping the first frame of a burst is less wrong (51 % of drops) than
  keeping the sharpest face (61 %).

## 2026-11-28 — Faena: the second wedding before and after the agency's cull

- Faena (2026-10-03, four cameras, 3,822 JPG): the editor rejected 1,291 (34 %). Eight agent
  reviewers coded every reject with codebook 2, a blind second reviewer 129 of them: same code in
  60 %, kappa 0.52 ([analysis](weddings/faena/analysis.md), 17 claims).
- Holds on both weddings: rejects are relative to a kept twin (85 %; Glamur 77 %), each camera is
  culled alone, burst thinning drops about as many of her keeps as of her rejects (46 %), lone
  frames lose 24.1 % on both ([comparison](weddings/README.md#claims-across-weddings)).
- Differs: the main photographer loses 45 % and the second 23 % (Glamur 31 % / 35 %); frames
  with the videographer are sometimes kept; both of a near-identical pair stay less often (18 %).
- New: in four posed pairs the editor kept the frame with closed eyes and rejected the clean
  twin, so her cull is not a clean ground truth for "which frame of a pair" (FAE-F09).
- The first run of the reviewers died on a usage limit with two of eight parts written; the
  rerun wrote results after every strip. `wedding.json` got the civil ceremony (17:04) and two
  formals blocks from the reviewers' strip notes.
