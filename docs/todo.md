# Todo

The list a new session reads first. Ordered by priority. When an item is done, remove it here and
write one line in [log.md](log.md). Items that need the user are marked **(user)**.

## Now

- **Requirements are written down: [requirements.md](requirements.md)** (2026-11-23, from Peđa's
  comments photo by photo). Read it before the three items below.
- **Show Peđa the question page (user).** `cull.py meeting --output data\questions`: five
  questions for [Q1–Q3 and Q6](requirements.md#open-questions), the contradicting examples side
  by side ([0024](decisions/0024-contradictions-side-by-side.md)). Look at the wording first; it
  is in `data/questions/meeting.json`. Afterwards `cull.py meeting-score --output data\questions`,
  then write the answers into requirements.md and close the questions. Q7 stays the user's (which
  `both` answers are really a different moment).
- **New group rule (user decides). Replaces 0014.** A group is literally the same moment; a new
  pose or action is a new group; orientation, black-and-white and a flash that did not fire do not
  split ([G1–G8](requirements.md#groups)). Write the decision, redo the 4a and Talići 1 labels
  ([0023](decisions/0023-agency-corrects-our-groups.md)), then measure with `cull.py score`. First
  candidate: the look-back join for photos with people (two of his three cuts, 75–117 s apart);
  a higher similarity threshold alone does not give his groups
  ([research](research/2026-11-23-meeting-choices-vs-signals.md)).
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
- **Group across cameras.** Main photographer and assistant shoot the same moment (wide and tight);
  the agency wants both merged by capture time and chosen between
  ([S5](requirements.md#scope)). Now each camera is grouped alone
  ([0003](decisions/0003-camera-by-serial-group-per-camera.md)). Needs a two-camera wedding to measure.
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

- **Check 4a and Talici 1 labels against the new group rule (user).** They were made 2026-11-10, partly under
  the old "wide vs tight = separate" rule ([0013](decisions/0013-group-definition-v1.md)).
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
