# Labels redone for the new group rule, and what similarity and time can reach (2026-11-25)

Questions: can two people label the boundaries the same way with the group rule of
[0025](../decisions/0025-group-definition-v3.md), and how close can the signals the pipeline has
(DINOv2 similarity, capture-time gap) get to those labels?

## What was done

1. The user re-labelled the `same` pairs of 4a (333 pairs in the end: 174 same, 159 different).
2. The agent reviewed all 333 on contact sheets and proposed 10 changes and 2 missing labels. The
   user accepted 7 (`9815`→`9817` D and `9847`→`9848` S are Peđa's own clicks, `0123`→`0124` S,
   `0115`→`0116` D, `9909`→`9910` S, `0138`→`0139` S, `0072`→`0073` D) and rejected 3
   (`9936`→`9937`, `9932`→`9933` stay S: too subtle; `0147`→`0148` stays D).
3. The agent labelled the 392 unlabelled pairs of Talići 1 from contact-sheet thumbnails (260 px),
   following the user's 4a decisions. The user checked them and disputed 14.
4. Going through the 14, the agent's answers were not consistent with each other (a raised arm was
   S in one place and D in another, the same for scenery and for a kiss). One fixed list of checks
   was written ([0026](../decisions/0026-labelling-checks.md)) and applied to every pair that had
   been discussed.

Result for Talići 1: 710 pairs, 443 same, 267 different. Of the agent's 392 labels 14 ended up
changed (3.6 %) and one more was changed twice and came back (`8352`→`8353`).

Files next to `labels.json` of Talići 1: `labels.before-v3.json` (rule 0014),
`labels.before-claude-2026-11-25.json` (before the agent's 392), `labels.before-consistency-2026-11-25.json`
(before the last nine changes). The agent's labels carry `labeled_at` `2026-11-25T23:59:00`, the
consistency changes `2026-11-25T23:59:30`.

## Where the two of us disagreed

Every disputed pair was of one of these kinds, all in posed sessions or of scenery, 2–20 s apart:

| Kind | Examples | Settled as |
|---|---|---|
| a gesture or pose changes a few seconds later (kiss, raised arm, leg up) | `7978`/`7979`, `8255`/`8256`, `8737`/`8738`, `8503`/`8504` | D when more than 2 s apart |
| one person alone turns the head or body | 4a `9936`/`9937`, T1 `8352`/`8353` | S (Peđa M6: "whichever") |
| same pose, small move of a hand, gaze, other framing | `8086`/`8088`, `8099`/`8100`, `8323`/`8324` | S |
| same pose, the photographer changed side | 4a `0072`/`0073`, `0046`/`0047` | D |
| scenery from another spot | `8516`/`8517`, `8705`/`8706`, `8718`/`8719` | D for another view, S for the same view |
| a wide shot where the people are tiny | `8400`/`8401` | the user's S |

Bursts, different people, a new place and long gaps were never disputed.

## Similarity and gap against the labels

Cosine similarity of the cached embeddings and capture-time gap for every labelled pair
(10 % – 90 % range in brackets).

Talići 1:

| Gap | Same | Similarity | Different | Similarity |
|---|---|---|---|---|
| ≤ 2 s | 188 | 0.93 [0.85–0.97] | 2 | 0.61 [0.52–0.70] |
| 2–5 s | 97 | 0.90 [0.81–0.95] | 17 | 0.75 [0.56–0.92] |
| 5–15 s | 128 | 0.88 [0.79–0.94] | 73 | 0.64 [0.27–0.87] |
| 15–40 s | 27 | 0.85 [0.79–0.91] | 104 | 0.56 [0.21–0.82] |
| > 40 s | 3 | 0.89 [0.84–0.91] | 71 | 0.47 [0.16–0.74] |

4a:

| Gap | Same | Similarity | Different | Similarity |
|---|---|---|---|---|
| ≤ 2 s | 71 | 0.91 [0.84–0.96] | 9 | 0.70 [0.55–0.83] |
| 2–5 s | 31 | 0.86 [0.83–0.91] | 15 | 0.64 [0.42–0.80] |
| 5–15 s | 66 | 0.89 [0.79–0.94] | 69 | 0.64 [0.29–0.80] |
| 15–40 s | 6 | 0.86 [0.80–0.92] | 42 | 0.51 [0.19–0.77] |
| > 40 s | 0 | | 24 | 0.43 [0.05–0.70] |

Correct pairs:

| | Talići 1 (710) | 4a (333) |
|---|---|---|
| current `groups.json` | 649 (42 false merges, 19 missed) | 310 (8 false merges, 15 missed) |
| best single similarity threshold, fitted on the labels | 636 (at 0.79) | 306 (at 0.83) |
| best rule "(gap ≤ g and sim ≥ t1) or sim ≥ t2", fitted on the labels | 645 | 309 |

False merges of the current grouping by gap, Talići 1: 0 at ≤ 2 s, 8 at 2–5 s, 23 at 5–20 s, 11
above 20 s. 4a: 2, 1, 4, 1.

## Findings

1. **The thresholds are at their limit.** The current grouping scores as well as the best rule of
   similarity and gap fitted on the same labels (649 against 645, 310 against 309). Tuning them
   further to rule 0025 cannot gain more than a few pairs.
2. **Bursts are safe.** At 2 s or less 259 of 270 pairs are the same moment, and the 11 that are
   not have low similarity.
3. **The open zone is 5–15 s.** Same and different are about half and half there and their
   similarity ranges overlap.
4. **The pipeline fails where the labellers disagreed.** Its errors (about 8 % of pairs) and our
   changes of mind (about 4 % of the agent's labels) are the same kind of pair: the picture looks
   alike and the bodies have rearranged, or the reverse. Whole-frame similarity measures the
   first, rule 0025 asks the second.
5. **A share of the boundaries is a matter of taste.** Two labellers with the rule in front of
   them, and Peđa himself ([Q2, Q3, Q7](../requirements.md#open-questions)), gave both answers.
   A score of 100 % on these labels is not a meaningful target.

## Directions proposed (not decided)

In [todo](../todo.md). In short: stop tuning thresholds; let the selection drop frames only inside
tight "same picture" sets so that a doubtful boundary cannot lose a photo; mark taste-dependent
pairs `unsure` so the score counts real mistakes; a signal for the arrangement of bodies (crop
around the people, body keypoints) if boundaries have to improve; a shorter look-back for photos
with people.

## Limits

- One wedding, two albums, one photographer. The posed session of Talići 1 is not typical
  ([S8](../requirements.md#scope)).
- The agent labelled from 260 px thumbnails; small changes of expression or gaze can be missed.
- "Best rule" is fitted and scored on the same labels, so it is an upper bound, not a recommendation.

## Reproduce

Pairs and labels: `<out>/labels.json`; photos and times: `<out>/photos.json`; vectors:
`<out>/embeddings.npz` (`keys`, `vectors`); groups: `<out>/groups.json`.
`cull.py score --output <out>` prints the errors of the current grouping.
