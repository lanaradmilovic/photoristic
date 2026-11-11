# VLM judge (step 2c)

Status: implemented (`culling/vlm.py`, `culling/judge.py`) and **parked**: the first real run on
4a did not beat the pipeline, so grouping does not use it ([0020](../decisions/0020-vlm-judge-parked.md)).
It stays as a measuring tool for a stronger model. Real run: [research](../research/2026-11-11-judge-first-real-run.md);
dry-run numbers: [research](../research/2026-10-23-judge-dry-run.md).

DINOv2 similarity between **0.80 and 0.90** is a grey zone: it holds "the same couple in a new
pose" (one group) as well as "another guest at the same spot" (must stay apart). Face identities
decide part of it; the rest (profiles, backs, small faces) needs a model that sees both frames.
`cull.py judge` sends such pairs to a VLM as one side-by-side image and records its verdict. The
verdicts are **not used by grouping yet**: this step measures how well the model decides the grey
zone before anything depends on it.

## Which pairs

`judge.sim_low <= similarity < judge.sim_high`, per camera, in capture order:

- *neighbour*: two time-adjacent photos, whether the pipeline joined them or not;
- *look-back*: a photo and its best-matching earlier photo of another group whose latest photo is
  at most `grouping.lookback_seconds` old (the pipeline kept them apart). As in grouping, a group
  whose best photo shows different identified people is skipped, and the most similar remaining
  group is the candidate; the gap shown is to that best-matching photo. A match at or above the
  band that the pipeline still did not join is only counted. Also: a photo that joined its own
  group by look-back (`joined_by`) with a best match in the band — a possible false merge through
  the relaxed `faces_*` / `nopeople_*` rules; kept whatever decided them.

Excluded, each counted in the dry-run: pairs whose face identities already say *same* or
*different* (`--include-faces-decided` sends them too), pairs where both photos show no people,
and everything past `--max-pairs`.

## The question

The pair image shows photo 1 (left) and photo 2 (right), each scaled to
`judge.pair_image_long_edge` (768 px). The prompt gives the time gap and asks for `same_people`
(yes / no / unsure), `interchangeable` (yes / no / unsure, defined by the
[group rule](grouping.md#what-a-group-is)), `verdict` (`same_group` / `different_group` /
`unsure`), `confidence` (0–1) and a short `reason`. The answer is forced into that JSON schema
(vLLM structured outputs), temperature 0, thinking off. The prompt never mentions the similarity
or the pipeline's decision.

## Running

```bash
.venv\Scripts\python cull.py judge --output data\out-4a --dry-run    # select pairs, write images, send nothing
.venv\Scripts\python cull.py ping-vlm                                # does the server answer and serve the model?
.venv\Scripts\python cull.py judge --output data\out-4a --max-pairs 5
.venv\Scripts\python cull.py judge --output data\out-4a              # all; safe to interrupt and rerun
```

The dry-run prints pairs per kind (and how many the pipeline joined), exclusions, a token estimate
(Qwen3.5: one visual token per 32×32 px of the pair image plus ~330 text tokens) and a duration
estimate from `judge.seconds_per_call`.

A real run needs the vLLM server ([plan, constraints](../plan.md#fixed-constraints)): start the
instance, open the tunnel, set `VLM_API_KEY` when the server checks a key, run `ping-vlm` first.
**Port 8000 on the workstation is held by DashClientService**, so tunnel with
`ssh -L 8001:localhost:8000 <host>` and set `vlm.base_url: http://localhost:8001/v1`. Compare
`usage.prompt_tokens` of the first answers with the estimate.

The run writes `judge_verdicts.json` after every pair; a dropped connection stops it and the next
run asks only for missing pairs (verdicts `error` — no valid answer after `vlm.max_retries` — are
asked again). When `labels.json` exists, labelled neighbour pairs are compared with the labels:
correct / wrong / abstained for the judge, correct / wrong for the pipeline on the same pairs,
precision and recall for `same_group`, and every wrong pair with the model's reason. Stored under
`labels` in `judge_verdicts.json`.

## Files

- `judge_pairs.json`: `{created, sim_low, sim_high, lookback_seconds, stats, pairs: [{a_id, b_id,
  a_name, b_name, camera_id, a_time, b_time, kind, similarity, gap_seconds, pipeline_same_group,
  faces_relation, image, image_size}]}`, rewritten on every run.
- `judge_pairs.jpg`: contact sheet in the same order (green frame = pipeline joined, red = split).
- `judge_pairs/<a>_<b>.jpg`: exactly what is sent.
- `judge_verdicts.json`: `{created, updated, model, base_url, sim_low, sim_high, verdicts:
  {"<a_id>|<b_id>": {a_id, b_id, a_name, b_name, kind, same_people, interchangeable, verdict,
  confidence, reason, attempts, elapsed_s, prompt_tokens, judged_at}}, labels}`.

Privacy: pair images go only to `vlm.base_url`; `--dry-run` sends nothing; the log carries only
verdict and confidence per pair.
