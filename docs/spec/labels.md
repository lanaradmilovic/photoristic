# Ground-truth labels and scoring

Status: implemented (`culling/labels.py`, `culling/labelserver.py`, label mode in
`culling/report.py`). Decision: [0015](../decisions/0015-labels-per-adjacent-boundary.md).

Labels turn "look at the contact sheets" into a number: label the test weddings once, then every
re-grouping gets precision / recall / F1.

## What a label is

The boundary between two *time-adjacent photos of the same camera*: `same` (one group),
`different`, or `unsure`. Stored per pair of sha256 (not per group id), so labels survive
re-grouping, re-ingesting and renamed output folders. A "same" run of three photos is two labels.

`labels.json`: `[{a_sha, b_sha, a_name, b_name, label: same|different|unsure, labeled_at}, …]`.

Known limitation: look-back joins (a photo returning to an earlier, non-adjacent group) cannot be
labelled and are not scored.

## Labelling

```bash
.venv\Scripts\python cull.py label --output data\out-4a
```

Rebuilds `report.html`, serves the folder on `http://127.0.0.1:8765/` and opens the browser in
*Label mode*. Every change is POSTed and written to `labels.json` at once; Ctrl-C stops the server.
The strip shows the photos in capture order with one widget between each pair:

- the connector shows the pipeline's decision (green = same group, red dashed = different), with
  the DINOv2 similarity and the time gap;
- a **dotted** button is only the pipeline's suggestion, *not* saved until confirmed;
- a **filled** button is a label (green S, red D, amber U); a red left edge marks a label that
  disagrees with the pipeline;
- the counter shows labelled / total and counts per label.

| Key | Action |
|---|---|
| `←` `→` (or `↑` `↓`) | previous / next boundary |
| `S` / `D` / `U` | same / different / unsure, then next boundary |
| `Enter` | accept the pipeline's suggestion |
| `N` | next unlabelled boundary |
| `Backspace` / `Delete` | remove the label |
| `Esc` | leave label mode |
| click a thumbnail | preview (←/→, Esc) |

Opened as a plain file (no server), labels stay in the browser's localStorage per wedding; use
**Export labels.json** / **Import**. *Clear labels* needs two clicks.

## Scoring

```bash
.venv\Scripts\python cull.py score --output data\out-4a
.venv\Scripts\python cull.py score --output data\out-4a --groups groups.json groups.nofaces.json
```

For every labelled boundary (unsure skipped) the pipeline says "same" when both photos are in one
group. Printed: number of labels, correct, **false merges** (joined, label different: the error
that could lose a photo), **missed merges** (split, label same: costs review time), precision /
recall / F1 for "same", and every error with names, similarity and gap. Errors go to `errors.jpg`.
With two files the metrics are side by side, plus which boundaries one gets right and the other
wrong. Any saved `groups*.json` can be scored, so a change is measured before and after.

## Best-photo picks

Status: implemented (`culling/picks.py`, `cull.py pick`, `cull.py pick-score`). Ground truth for
the ranking ([vlm-scoring](vlm-scoring.md)).

```bash
.venv\Scripts\python cull.py pick --output data\out-4a        # opens picks.html
.venv\Scripts\python cull.py pick-score --output data\out-4a  # ranking.json vs picks.json
```

`picks.html` shows one multi-photo group per screen (previews, capture order, numbered). It does
not show the program's choice. The rules are on the page (in Serbian): mark every photo the agency
would deliver, usually one; more only for a different framing, moment or people; between two
near-identical frames pick one and press **T** (toss-up, excluded from "did the model pick right");
**N** when no photo is deliverable. Keys: click or `1`–`9` toggle, `Z` + number or 🔍 full screen
(`Space` toggles there), `Enter` next unfinished group, `←` `→`. Every change is POSTed at once.

Below the photos, once a photo is picked, one click says **why it won**: `eyes`, `focus`,
`expression`, `framing`, `moment` (several allowed), and there is a free note. Both are optional.

`picks.json`: `{updated, groups: {key: {picked: [sha256], none, tossup, names, at, reasons, note}}}`;
`key` is the group's photo sha256 values, sorted and joined with `|`. Matching is per photo, so
picks survive re-grouping and re-ranking.

**A sample for a meeting** (asked for by the user on 2026-11-18: the agency should show how they
choose on a few groups, not on all 79):

```bash
.venv\Scripts\python cull.py pick --output data\out-4a --sample data\meeting\picks_sample.json --picks-file picks.agency.json --port 8766
.venv\Scripts\python cull.py pick-score --output data\out-4a --picks-file picks.agency.json --compare picks.json
```

`--sample FILE` shows only the listed groups, in the file's order, with short rules addressed to
the agency and closed from the start. The file is `[{"photo": "<file name>", "kind": "..."}]`: a
group is named by any of its photos, `kind` is the author's note on why it was chosen and is never
shown. `"ask": true` on an entry (two-photo groups only; for the pairs the model could not decide)
adds one question after the pick: "would it matter if the program had kept the other photo?" The
answer is `swap_ok` in the picks file (`true` = it would not, which also sets `tossup`).
`--picks-file NAME` keeps another person's picks in their own file in the output folder.
`pick-score` also prints how often each reason was given, how many photos were picked per group
and the notes; `--compare NAME` adds how often two people chose the same in the groups both did.

**Review mode** (`cull.py pick --output <out> --review-model`, asked for by the user on
2026-11-14: blind picking is tiring and she wants to see how the model decides). One screen per
multi-frame variant that `ranking.json` has an answer for, photos in the order and with the numbers
the model saw. The model's winner has a dashed blue frame and `MODEL ★`; every caption has the
model's place and the flaw it named; below the photos are its reason and, when
`ranking_reversed.json` exists in the output folder (rows `{photo_ids, winner_reversed,
reason_reversed}` of a check that asked the same variant in reversed order), whether the reversed
question gave the same winner. **A** picks the model's winner, a click picks another photo, **T**
without a pick takes the model's winner as a toss-up. These picks are stored in the same
`picks.json` under the variant's key, with `seen_model: true`: they measure agreement with a
choice the user saw, not an independent ground truth.

`pick-score` prints, for the groups done: picked photos that the ranking keeps (anything else is
only `maybe`), kept photos that were not picked (review time), and how often the model's winner
of a variant was picked (toss-ups and "none" excluded).

## Agency meeting page

Status: implemented (`culling/meeting.py`, `cull.py meeting`, `cull.py meeting-score`). Decision:
[0023](../decisions/0023-agency-corrects-our-groups.md).

```bash
.venv\Scripts\python cull.py meeting --output data\meeting         # builds and opens meeting.html
.venv\Scripts\python cull.py meeting-score --output data\meeting   # what the agency answered
.venv\Scripts\python cull.py score --output data\out-4a --labels data\meeting\meeting_answers.json
.venv\Scripts\python cull.py meeting --output data\questions       # the follow-up questions of 2026-11-23
```

One page in Serbian that leads through a feedback meeting, without numbers or the program's
reasons. What it shows is written by hand in `meeting.json` in the meeting folder; every part is
optional, one of them must be there:

```json
{"title":     "Pitanja posle sastanka",
 "cases":     [{"out": "data/out-4a", "a": "_KAD0141.NEF", "b": "_KAD0142.NEF", "kind": "siri-uzi"}],
 "excerpts":  [{"out": "data/out-4a", "title": "Crkva", "first": "_KAD9796.NEF", "last": "_KAD9900.NEF"}],
 "questions": [{"id": "siri-uzi", "title": "Širi i uži kadar iste poze", "text": "…",
                "ask": "Šta program treba da zadrži?",
                "sides": [{"out": "data/out-4a", "photos": ["_KAD9930.NEF", "_KAD9931.NEF"],
                           "label": "Mladenci kod stolova", "said": "obe", "tone": "keep", "why": "…"}],
                "options": [{"id": "obe", "text": "Uvek obe"}, {"id": "jedna", "text": "Uvek jednu"}]}]}
```

`out` is a pipeline output folder (absolute, or relative to the working directory). The previews in
use are copied to `<meeting folder>/previews/`, so one page can show several weddings. Unknown
keys, unknown file names and a pair shown twice are errors.

1. **Disputed pairs** (`cases`), one per screen, the program's decision not shown: "would you
   deliver one of these two or both?" with three answers, because a group and a variant are not
   the same thing ([0022](../decisions/0022-variants-in-code-model-ranks.md)): `one` (the same
   picture) and `both` (same moment, both delivered) are the label `same`; `different` (another
   moment or other people) is `different`. `kind` is the author's name for what the pair tests; it
   is never shown.
2. **Excerpts**: every group whose first photo was taken between `first` and `last`, as framed
   boxes. A click on ✂ between two photos of a group is a cut (`different`); a click on *spoji*
   between two boxes is a join (`same`, for the last photo of one group and the first of the next).
   "Ostalo je u redu, dalje" writes every untouched pair of the excerpt as `confirmed` with the
   program's decision, so a pair without an entry was not looked at.
3. **Questions** (`questions`), one per screen
   ([0024](../decisions/0024-contradictions-side-by-side.md)): a title, an optional introduction
   (`text`), the examples the question is about (`sides`), the question (`ask`) and the written
   answers (`options`) as a list of buttons. The page adds the answer "Drugačije" (`other`) to
   every question; choosing it puts the cursor in the note.
   - A side is a card with one or more photos, a `label`, what was said about it earlier (`said`,
     shown as "Rekli ste:" with a tag, green for `tone: keep`, orange for `cut`) and the reason
     given then (`why`). Two sides stand next to each other as A and B; that is how answers that
     contradict each other are asked again.
   - A question without sides is just the question and its answers.
   - The last screen lists every question with the chosen answer and the note; a click goes back
     to it.

Keys: `1` `2` `3` answer a disputed pair, `1`–`9` a question, `Enter` confirms an excerpt, `←` `→`
move, a click on a photo opens it full screen. Every screen has an optional note.

`meeting_answers.json`: `{updated, pairs: […], notes: {…}, choices: {…}}`. A pair has the fields of
a label (`a_sha, b_sha, a_name, b_name, label, labeled_at`) plus `source` (`click` / `confirmed` /
`case`), `part` (`case` or the excerpt's title) and, for a case, `answer` and `kind`. `choices` is
`{question id: {option, text, question, at}}`: the wording is stored with the answer, because
`meeting.json` may be rewritten later. Notes are keyed `case:<a_sha>|<b_sha>`, `excerpt:<title>`
and `question:<id>`. Pairs need not be time-adjacent, so groups with look-back photos work.

`meeting-score` prints the answer for every disputed pair, per excerpt the pairs looked at with the
cuts and joins, the answer and note for every question, and the pairs where the agency and
`labels.json` of the same output folder disagree. `score --labels` measures any grouping against the agency's pairs; pairs of other
weddings count as "missing in groups (skipped)". `confirmed` pairs were answered with the
program's grouping on the screen, so they lean towards it.

## Verifying the report UI

The Claude-in-Chrome extension cannot open `127.0.0.1` / `localhost` on this workstation. Use
headless Chrome with a harness HTML that iframes the report and `console.log`s results:
`chrome.exe --headless=new --enable-logging=stderr --v=0 --virtual-time-budget=30000 --screenshot=… <url>`
(add `--allow-file-access-from-files` for file:// mode). `--dump-dom` and `--timeout` do not wait
for async work.

The Browser pane of the Claude desktop app does open `localhost`: start the page with
`--no-browser` through an entry in `.claude/launch.json` and `preview_start`, then read the page,
press keys and take screenshots there (used for the question page on 2026-11-23). Delete the test
answers afterwards.
