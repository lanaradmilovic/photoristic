# Todo

The list a new session reads first. Ordered by priority. When an item is done, remove it here and
write one line in [log.md](log.md). Items that need the user are marked **(user)**.

## Now

- **Requirements are written down: [requirements.md](requirements.md)** (2026-11-23, from Peđa's
  comments photo by photo). Read it before the three items below.
- **Show Peđa the question page (user).** `cull.py meeting --output data\questions`: twelve
  questions, revised 2026-11-26 for the selection step and shortened in Peđa's words: for
  Ksenija (Glamur after culling, deleted frames, where dropped frames go, her program, how many
  stay), then rules to confirm (important moments, photo session, important moment with nearly
  identical frames, closed eyes, wide and tight, marking dark frames, camera clocks). What was
  dropped and why: [open questions](requirements.md#open-questions). Wording in
  `data/questions/meeting.json`.
  Q11–Q13 (where a moment ends) are the user's to decide for the labels. Afterwards `cull.py meeting-score --output data\questions`,
  then write the answers into requirements.md and close the questions. Q7 stays the user's (which
  `both` answers are really a different moment).
- **Grouping after the new labels: decide the direction (user).** The labels of 4a and Talići 1
  follow [0025](decisions/0025-group-definition-v3.md) and the checks of
  [0026](decisions/0026-labelling-checks.md). Measured 2026-11-25: the current grouping is as good
  as the best rule of similarity and gap fitted on these labels (649 of 710, 310 of 333), and its
  errors are the pairs the labellers disagreed on
  ([research](research/2026-11-25-labels-v3-and-signal-ceiling.md)). Proposed, in this order:
  1. Do not tune the similarity and gap thresholds further; keep the labels as a regression check.
  2. Two levels: tight "same picture" sets, the only place where the selection may prefer one
     frame ([K2](requirements.md#how-many-frames-of-a-group-stay)), inside looser "moment" groups
     used for the review page and for counting few or many (K7). The first half is done: the
     variants of [0022](decisions/0022-variants-in-code-model-ranks.md) were already such sets
     and are now limited to one burst (0027). Waiting for Peđa's answer to `sme-da-izbaci`:
     whether the program also chooses among similar frames when there are many (K7), and what to
     do in important moments, where he keeps every frame of a burst (K3).
  3. Mark the taste-dependent pairs `unsure` in both label files so `cull.py score` counts real
     mistakes (kinds of pairs: research, "Where the two of us disagreed").
  4. Done 2026-11-25 on branch `grouping-v3`: same people return to an earlier group only at
     0.82, and a variant is one burst of 2 s
     ([0027](decisions/0027-lookback-and-burst-variants.md)). Still open from it: review and
     merge the branch; run `cull.py rank` on 4a again (`ranking.json` is from the old variants);
     look-back joins inside the ceremony still glue different steps (`0043` with `0057`) and no
     label sees them (see "Labelling tool: look-back joins" below).
  5. Only if boundaries still have to improve: a signal for the arrangement of bodies (similarity
     of a crop around the people, body keypoints), local on CPU.
- **Check the agent's labels of Talići 1 to the end (user).** 392 pairs were labelled by the agent
  from thumbnails; the user checked them once and disputed 14. Pairs worth a second look are
  listed in the research file. Refresh the label page (Ctrl-F5) before clicking: it saves its own
  copy of all labels.
- **Decide what the selection step does (user). Blocks phase 3.** Input is now
  [K1–K12, B1–B6](requirements.md#how-many-frames-of-a-group-stay): bad frames out, exactly-same
  frames reduced to one, the rest kept; fewer only for ordinary moments with many frames. One
  winner per variant ([0022](decisions/0022-variants-in-code-model-ranks.md)) is stricter than
  that (Peđa kept 59 of 78, [numbers](research/2026-11-19-agency-meeting-answers.md)). Missing
  signals: who is in the frame (couple, family, guests) and how important the moment is. A kiss
  must not count as closed eyes, a recoverable dark frame must not be marked down. Candidate signal
  for "exactly the same" (K2): similarity of a crop around the main people, which separates the two
  example pairs but not "one" from "both" in general
  ([research](research/2026-11-24-same-or-not-two-pairs.md)). Write the decision record.
- **Promised to the agency: an improvement by 2026-11-26.** Peđa is there on Thursdays for two or
  three more weeks, then away for about two months (WhatsApp / video call possible).
- **Data from the agency (user).** They give one wedding as an unedited and an edited package. Still
  to ask: how many photos stay of 5–6 thousand, which program Ksenija culls in, whether Peđa deleted
  frames before handing over Talici ([gaps](research/2026-11-19-file-number-gaps.md): 475 of at
  least 3,050 are missing, so the pipeline has never seen plainly bad frames), and a wedding with
  the photos of both photographers: the Talići folders hold one camera only, so Đole's frames of
  that day are missing ([resolved Q10](requirements.md#resolved)).
- **Glamur before/after the agency's cull: talk it through (user).** The editor rejected 962 of
  3,428 in Photo Mechanic; reasons are differences between twins (faces, occlusion, crew, flash),
  every burst-thinning rule drops more of her keeps than her rejects
  ([research](research/2026-11-26-glamur-cull.md)). Report with a gallery of all rejects and your
  own marks: `<out>\posle-analiza\index.html` (open from disk). Next, if agreed: a score of
  suggestions against her decisions; questions for Ksenija are at the end of the report.
  The same in the fixed format for comparing weddings: [weddings/glamur](weddings/glamur/analysis.md)
  (15 claims, status draft until you check them).
- **Next before/after wedding: use the fixed format ([weddings](weddings/README.md#adding-a-wedding)).**
  Codebook version 2, a second reviewer on about 10 % of the rejects, then `cull.py analysis`
  and `analysis.md`; then the first comparison fills "holds elsewhere" of the Glamur claims.
  Glamur's `DUP` (475) could be recoded with v2 to make the two comparable on faces.
- **Check the agent's labels of Glamur (user, 120 pairs).**
  `cull.py meeting --output "<OneDrive>\...\output\2026-11-26-glamur\review"`, then
  `cull.py meeting-score` on the same folder: its last block lists where your answer differs from
  `labels.json`. Shown: 21 of 91 false merges, 26 of 111 missed merges, 33 of 141 unsure (random,
  the rest is in `review/not_shown.txt` and `errors.jpg`) and 40 random pairs where labels and
  pipeline agree ([research](research/2026-11-26-glamur-grouping.md)).
- **Guest line-ups are merged (found on Glamur).** Other guests with the couple at the same spot
  10–36 s apart join one group (40 false merges; `g0318` is 56 photos of about eleven line-ups,
  partly through look-back). Not tuned. Ask the agency first whether these printed photos go
  through the tool at all ([S2](requirements.md#scope)); if they do, the selection must not pick
  one frame from such a group. Also to decide: a tight frame (or in-camera crop) of some people of
  a posed photo, same group or not (the checks of 0026 do not say; labelled `unsure`).
- **Group across cameras.** Measured on Glamur: the clocks differ (LPZ +298 s, JAS -68 s against
  KNEZ, VAL not measurable), so a clock offset per camera comes first; with corrected clocks 36 %
  of photos have a partner within 2 s, about six in ten such pairs are the same moment, and the
  one-camera similarity rule finds a third of those
  ([research](research/2026-11-26-glamur-grouping.md#across-cameras)). Background: main photographer and assistant shoot the same moment (wide and tight);
  the agency wants both merged by capture time and chosen between
  ([S5](requirements.md#scope)). Now each camera is grouped alone
  ([0003](decisions/0003-camera-by-serial-group-per-camera.md)). Next: a decision record for offset estimation and pairing of groups.
- **Grouping was reviewed only in part at the meeting** (3 cuts, 1 join, about ten groups
  commented, Deo 3 not opened). The page stays ready: `cull.py meeting --output data\meeting`
  ([spec](spec/labels.md#agency-meeting-page)). Do not score a grouping against
  `meeting_answers.json` before [Q7](requirements.md#open-questions) is resolved.

- **Phase 3: switch `ranking.py` to judging each photo alone.** Comparing frames in one request
  is position-biased with both the 4-bit and the full model (same winner in both orders 15 and 12
  of 53). Judging each photo alone and ranking in code is stable (eyes/focus/expression agree in
  95–98 % between 1024 and 1280 px), but ties at the top in ~55 % of variants
  ([research](research/2026-11-14-ranking-full-model-and-per-photo.md)). To do: per-photo request
  and schema in `ranking.py` (prompt and penalties from the experiment), cache per photo sha256,
  ties at the top all `keep` (safe) or broken by a pairwise question asked in both orders.
  Decide after the ground truth below shows whether the per-photo winners are right.
- **Pairwise report prompt (2026-11-15): consistent, not selective.** Fixed checks, `A / B / same`,
  both orders, agreement in code: 0 invented differences on identical pairs, 3 of 576 answers
  depend on the order, but only 10 of 53 variants get one winner (85 % of photos kept)
  ([research](research/2026-11-15-report-prompt-both-orders.md)). Not in `ranking.py`. Decide
  (user): accept "tie = keep all" with this keep rate, or add a taste step for ties. To try:
  face crops for the eyes check, log-probabilities instead of the three answers.
- **Ground truth for "best photo" (user, ~20 min on 4a).** Wait for the decision above: the picks
  should record what the agency would deliver (often several photos), not one winner. Tool:
  `cull.py pick --output data\out-4a` (79 groups); the agency's 23 groups are in
  `picks.agency.json` (`pick-score --picks-file picks.agency.json --compare picks.json`).

## Next

- **Day segments: 4 missed cuts.** At 300 s four real part-of-day changes are not cut; pauses cannot
  separate them ([0017](decisions/0017-segments-gap-300s.md)). Needs content (VLM segment
  classification), not another threshold.

- **Open review findings (2026-11-11), smaller ones not fixed at merge:** label server checks no
  Origin; failed save falls back to localStorage that server mode never reads; thresholds copied in
  `judge.py` docstring and report JS; double VLM ping; duplicated helpers (`_write_json`, `_ratio`,
  `_time`, `_clock`); `partial_blocks` treats an unrecognised face as a different person (measure
  with `cull.py score` first); segments: `load_people` skips the model check, stale
  `identities.json` used when faces are off, filters hide segment bars only by camera, burst
  cutoff and sheet sizes not in config.

## Later / ideas

- **Labelling tool: look-back joins.** Only adjacent pairs can be labelled; "photo 5 belongs with
  photo 2" cannot be recorded. Add such a label if the user sees it often.
- **Ranking: oversized variants.** A variant longer than `ranking.max_images` is cut into parts
  with one keep each; a play-off between the part winners would save keeps if such variants are common.
- **VLM judge again with a stronger model.** Parked ([0020](decisions/0020-vlm-judge-parked.md)).
  When the full Qwen3.5-9B (g6) or a larger model runs, re-run `cull.py judge` on 4a (~10 min) and
  try a v3 prompt that limits "person added/missing" to posed group photos.
- **Garbage face identities.** A size filter was rejected ([0012](decisions/0012-no-face-size-filter.md));
  another feature (blur, position, co-occurrence) might work.
- Phase 1 checks on a two-camera wedding ([plan](plan.md#phase-1--ingest)).
