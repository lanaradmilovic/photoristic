# Look-back for the same people and variants limited to a burst (2026-11-25)

Questions: which look-back setting removes the joins Peđa cut without hurting the labels, and how
far are the variants of [0022](../decisions/0022-variants-in-code-model-ranks.md) from what he
picked? Decision: [0027](../decisions/0027-lookback-and-burst-variants.md).

Method: both labelled albums were regrouped from the caches (embeddings, people, identities) with
one setting changed, and scored against `labels.json` (adjacent pairs only). Five pairs of Peđa
were checked separately, because look-back joins have no label: his cuts 8020|8029 and 8028|8032
(Talići 1), his cut 9815|9817, his join 9847+9848 and the look-back group he called good,
9789 → 9796 (4a). "Peđa" below counts how many of the five the grouping gets right.

## Look-back

| Setting | Talići 1 correct (of 710) | 4a correct (of 333) | Look-back joins T1 / 4a | Peđa (of 5) |
|---|---|---|---|---|
| before | 649 | 310 | 31 / 17 | 1 |
| people look-back window 90 s | 649 | 310 | 29 / 14 | 2 |
| people look-back window 70 s | 649 | 309 | 27 / 13 | 3 |
| people look-back window 60 s | 649 | 307 | 26 / 11 | 3 |
| people look-back window 30 s | 650 | 306 | 16 / 9 | 2 |
| no look-back for people | 650 | 305 | 0 / 3 | 2 |
| same-people look-back 0.75 | 649 | 310 | 29 / 15 | 2 |
| same-people look-back 0.80 | 650 | 310 | 22 / 15 | 2 |
| **same-people look-back 0.82** | **648** | **310** | **16 / 15** | **3** |
| same-people look-back 0.85 | 648 | 308 | 14 / 13 | 3 |
| same-people look-back 0.90 (off) | 645 | 305 | 10 / 12 | 3 |

The two pairs of the five that no setting fixes are neighbours, not look-back: 9815|9817 (0.82 at
2 s, joined) and 9847+9848 (0.65, split).

Neighbour rules for the same people, for comparison: `faces_similarity_threshold` 0.75–0.80 and
`faces_gap_seconds` 20–30 move Talići 1 between 649 and 651 and leave 4a at 310.

- The label score barely moves with any look-back setting: the labels are adjacent pairs.
- A shorter window makes 4a worse because a photo that may no longer return joins its neighbour
  instead. In the one case looked at (0057) both placements are wrong: before it was with 0043
  (standing apart against holding hands), after with 0055 (the other side).
- 0.82 separates Peđa's cuts (0.73 and 0.78) from the return he confirmed (0.86).
- The window was implemented for the measurement (`people_lookback_seconds`) and removed again.

## Variants against Peđa's picks

His 23 groups of 4a: 78 photos, 59 picked. A variant keeps one photo, so "cannot all be kept" is
the number of picked photos beyond one per variant, and "kept, not picked" the variants without a
picked photo. No model is involved. Keeps are variants per photo over the whole album.

| Variants | Keeps Talići 1 | Keeps 4a | Picked, cannot all be kept | Kept, not picked |
|---|---|---|---|---|
| before (0.90, any gap) | 68 % | 79 % | 20 | 4 |
| within 5 s | 76 % | 90 % | 12 | 13 |
| within 3 s | 79 % | 90 % | 12 | 13 |
| **within 2 s** | **83 %** | **91 %** | **11** | **13** |
| within 1 s | 90 % | 94 % | 9 | 15 |
| within 2 s, similarity 0.85 | 78 % | 88 % | 14 | 11 |
| within 2 s, similarity 0.93 | 88 % | 96 % | 5 | 16 |
| similarity 0.95, any gap | 90 % | 96 % | 4 | 16 |
| every photo its own variant | 100 % | 100 % | 0 | 19 |

- A third of what he picked could not be `keep` with the old variants.
- The burst limit halves that. What remains are bursts where he keeps every frame.
- He dropped 19 of 78 in these groups; a rule that keeps everything is wrong by those 19.

## After the change

`cull.py score --groups groups.before-0027.json groups.json`: 4a 310 → 310 (no pair differs),
Talići 1 649 → 648 (2 fixed, 3 broken). Groups: 4a 150 → 152, Talići 1 221 → 235.

## Limits

- Five pairs of one person decide the look-back value; the labels cannot.
- The picks are from one album and were made on groups of the old grouping.
- "Cannot all be kept" assumes the model would pick his photo first; real results can only be worse.
