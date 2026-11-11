# VLM judge: first real run on talici 4a (two prompts)

Date: 2026-11-11. Spec: [vlm-judge.md](../spec/vlm-judge.md). Dry-run before it:
[2026-10-23](2026-10-23-judge-dry-run.md). Outcome: [0020](../decisions/0020-vlm-judge-parked.md).

## Setup

- Server: AWS `g4dn.xlarge` (T4 16 GB), vLLM, `Intel/Qwen3.5-9B-int4-AutoRound` (4-bit, float16),
  `--enforce-eager --max-num-seqs 4`, thinking off, temperature 0 ([aws-setup](../aws-setup.md)).
  Not the planned full Qwen3.5-9B on g6 (no capacity in Frankfurt).
- 115 pairs of 4a (59 look-back, 56 neighbour), default config, faces-decided pairs excluded.
  All 56 neighbour pairs have a label.
- No request failed or needed a retry in either run.

## Results against labels.json (56 neighbour pairs)

| | correct | wrong | breaks pipeline | fixes pipeline | same_group precision / recall | `same_group` of 115 |
|---|---|---|---|---|---|---|
| pipeline | 53 (52 in run 2) | 3 (4) | – | – | 0.978 / 0.957 | – |
| judge, prompt v1 | 48 | 8 | 7 | 2 | 0.855 / 1.000 | 109 |
| judge, prompt v2 | 26 | 30 | 28 | 2 | 0.875 / 0.438 | 41 |

`labels.json` was edited by the user at 22:41, between the two runs; this explains the pipeline's
53 → 52. Verdicts: `data/out-4a/judge_verdicts.json` (v1, the current prompt) and
`judge_verdicts.v2.json`.

Speed and tokens:

| | prompt tokens | completion tokens | s / pair | 115 pairs |
|---|---|---|---|---|
| v1 | ~1150 (estimate 1114–1314, first pair 1049) | ~65 | 5.5 (first call 13.6, warm-up) | 10.5 min |
| v2 | ~1200 | ~118 | 8.9 | 16.5 min |

Decoding dominates: ~15 tokens/s on the T4, so every output word costs time; prompt length almost
does not.

## Prompt v1 (the one in `culling/judge.py`): biased to "same"

109 of 115 answers are `same_group`, almost all with confidence 0.95–0.99 (confidence carries no
information). All 8 errors are false merges, with near-identical reasons: "same couple, same
setting, different framing and pose but same moment". The model recognises the people but does not
see a change of action. Example: _KAD9800 (couple standing at the altar) → _KAD9802 (couple walking,
70 s later), label different.

Part of the 8 may be label issues: labels were made 2026-11-10 partly under the old rule
([0013](../decisions/0013-group-definition-v1.md)); e.g. _KAD0136 → _KAD0137 (two poses, 1.7 s) is
probably "same" under [0014](../decisions/0014-group-definition-v2.md).

## Prompt v2 (tried, rejected): biased to "different"

Changes: the model first describes what the main people do in each photo and who differs (schema
order makes it generate these before the verdict); "same moment" defined by the action; doubt →
`different_group`. Exact text, kept for reference:

```
These are two wedding photos by the same photographer, labelled 1 (left) and 2 (right), taken
{gap} seconds apart. Decide whether they belong to the same group: the photographer would keep
only the best one of a group.

Answer with JSON, filling the fields in this order:
- photo1_action: what the main people in photo 1 are doing (fewer than 12 words).
- photo2_action: what the main people in photo 2 are doing (fewer than 12 words).
- people_difference: which main person is added, missing or replaced in photo 2 compared with
  photo 1, or "none" (fewer than 12 words).
- same_people: "yes" if the main people are the same, "no" if a main person is added, missing or
  replaced (for example hugging another guest, one person more or fewer in a group), "unsure" if
  you cannot tell.
- same_moment: "yes" only if the main people do the same action at the same place. A different
  action is "no": standing versus walking, before versus after the rings, petals or a kiss,
  posing versus moving on. Within the same action a new pose, expression, framing (wider or
  tighter) or orientation is still "yes". "unsure" if you cannot tell.
- verdict: "same_group" only if same_people and same_moment are both "yes"; otherwise
  "different_group". If anything is unclear, answer "different_group".
- confidence: a number from 0 to 1.
- reason: fewer than 20 words.
```

Schema fields in that order: `photo1_action`, `photo2_action`, `people_difference` (strings),
`same_people`, `same_moment` (yes/no/unsure), `verdict`, `confidence`, `reason`.

**Why it is worse.** 28 of 30 errors are false splits, and in ~23 of them the reason is a person
"added / missing" who is a background guest or someone walking into the frame:
_KAD0020 → _KAD0021 (0.7 s apart) "a main person (woman in purple) is missing";
_KAD0101 → _KAD0102 "a new person (officiant) is added"; _KAD9810 → _KAD9811 (1.2 s) "different
groom appears" (invented). The 0014 rule "a person added or missing = another group" is meant for a
posed group photo; the model applies it to anyone in the frame, and the separate
`people_difference` field plus "doubt → different" amplified it. The action rule helped on a few
pairs (_KAD9800 → _KAD9802 now correct) and also over-fired (_KAD0117 → _KAD0118, 1 s, "embrace vs
kiss"). Still 3 false merges (_KAD0055/0057, _KAD0068/0069, _KAD0155/0156).

## Conclusion

With this model (9B, 4-bit) the wording moves the bias from one end to the other; neither prompt
beats the pipeline (52–53 of 56). The weak point is telling the main people from the background
and noticing a change of action. Not tried: a v3 that limits "person added/missing" to a posed
group photo; a stronger model (full Qwen3.5-9B on g6, or larger).

Review page used for this note: a one-off script (not in the repo) wrote
`data/out-4a/judge_review.html` with each pair image, label, pipeline, both verdicts, the v2
descriptions and the reasons.
