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

## Verifying the report UI

The Claude-in-Chrome extension cannot open `127.0.0.1` / `localhost` on this workstation. Use
headless Chrome with a harness HTML that iframes the report and `console.log`s results:
`chrome.exe --headless=new --enable-logging=stderr --v=0 --virtual-time-budget=30000 --screenshot=… <url>`
(add `--allow-file-access-from-files` for file:// mode). `--dump-dom` and `--timeout` do not wait
for async work.
