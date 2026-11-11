# Grouping (step 2)

Status: implemented (`culling/embed.py`, `culling/people.py`, `culling/faces.py`,
`culling/grouping.py`, `culling/report.py`). All thresholds are in `config.yaml` under
`grouping`, `people` and `faces`; the current values live there, not here.

## What a group is

The rule every threshold, label and VLM answer is measured against
([decision 0014](../decisions/0014-group-definition-v2.md)):

- One group = the same main people in the same moment at the same place; the photographer keeps
  the best frame of it. A wider or tighter framing, a new pose or expression, or a vertical versus
  a horizontal frame stays in the same group.
- Different people = a different group: a hug with another guest in the congratulation line, and
  also **a person added to or missing from a group photo** (bride with her parents vs. bride with
  her parents and grandmother). Both frames are kept; a photo with one person fewer is not a
  substitute for the full one.
- A new activity or a new place = a different group.
- Photos without people (decor, food, details) may group more loosely.

Merging too much is worse than splitting too much: the VLM ranks *within* a group, so a wrongly
merged moment risks losing its best frame to a different scene. When in doubt, split.

## Signals

- **Embeddings:** DINOv2-small CLS vectors on CPU, from the 320 px thumbnail resized to 224×224
  with no crop ([0004](../decisions/0004-dinov2-small-local.md)). Cached in `embeddings.npz` by
  sha256; changing `embedding.model_name` invalidates the cache.
- **Person detection:** RT-DETR v2 (`people.model_name`), a photo "has people" when a box scores ≥
  `people.score_threshold` and covers ≥ `min_box_area_fraction` of the frame. Photos without
  people use the relaxed `nopeople_*` rules ([0007](../decisions/0007-relaxed-rules-without-people.md)).
- **Face identities:** see [Face identities](#face-identities) below.
- **Capture time:** kept next to similarity on purpose ([0005](../decisions/0005-time-next-to-similarity.md)).

## Algorithm

Per camera ([0003](../decisions/0003-camera-by-serial-group-per-camera.md)), photos are sorted by
capture time (with sub-seconds when present, then by filename). Walking in order, each photo
collects **candidate groups** and joins the one it is most similar to; with no candidate it
starts a new group ([0006](../decisions/0006-lookback-and-boundary-refinement.md)).

**Candidate 1: the previous photo's group** (`should_join`). It qualifies when either holds:
- **(a)** gap to the previous photo ≤ `time_gap_seconds` **and** cosine similarity ≥ `similarity_threshold` (a burst), or
- **(b)** gap ≤ `extended_gap_seconds` **and** similarity ≥ `high_similarity_threshold` (the same frame taken again a few seconds later),
- **(c)** both photos without people: gap ≤ `nopeople_gap_seconds` and similarity ≥ `nopeople_similarity_threshold`.

**Drift guard.** The photo's *average* similarity to all photos of the group must also be ≥
`min_mean_similarity_to_group`. This stops a slowly changing scene from chaining on; because the
average is used, a burst where the subject moves is not cut in the middle.

**Candidate 2: look-back** (`find_lookback_group`). The photo may be a *return* to an earlier
scene. An earlier group of the same camera is a candidate when all of these hold:
- the group's last photo is at most `lookback_seconds` old;
- the photo's best match in that group has similarity ≥ `lookback_similarity_threshold`
  (`nopeople_lookback_similarity_threshold` without people);
- the photo passes the drift guard;
- the group would not span more than `max_group_span_seconds`.

The look-back threshold is high on purpose: a different guest at the same spot and pose scores
0.85–0.88. Look-back photos are marked ↩ in the report and the group gets the flag `lookback`.
`lookback_seconds: 0` turns it off.

**Boundary refinement** (`refine_boundaries`). Afterwards, for every two consecutive groups at
most `extended_gap_seconds` apart, the last photo of the first group (or the first photo of the
second) moves to the other group when its average similarity there is higher by more than
`refine_margin`. Moved photos are marked ⇄, flag `moved`. Off with `refine_boundaries: false`.

**No size split.** `max_group_size: 0` (default): groups are never cut by size
([0009](../decisions/0009-no-group-size-split.md)). A positive value re-enables cutting at the
weakest consecutive similarity, linked through `split_from` / `split_part`.

**Invariant:** every photo is in exactly one group (`check_every_photo_once`, tests). Failed or
undated photos become single-photo groups with a flag and appear under *Problems* in the report.

## Face identities

[Decision 0010](../decisions/0010-face-identities-signal.md). Every preview is run through SCRFD-10G
(5 keypoints); each face is aligned to the ArcFace template and embedded with AuraFace (ArcFace
ResNet100, 512-d), ONNX on CPU. Per wedding, faces are clustered into identities: Chinese Whispers
at cosine similarity ≥ `identity_threshold`, then clusters whose centroids are ≥
`identity_merge_threshold` are merged (bride with and without sunglasses). Labels `A`, `B`, … by
number of faces. Only identities with ≥ `min_identity_faces` faces are *known*; rarer faces are
unknown and never speak for or against a merge.

Each photo's signature is its set of known identities and its number of faces. When two photos are
compared (neighbour, look-back, boundary refinement):

- **same people** (identical sets, same face count): the relaxed `faces_*` rules apply as well —
  gap ≤ `faces_gap_seconds` and similarity ≥ `faces_similarity_threshold`, look-back at
  `faces_lookback_similarity_threshold`, drift guard at `faces_min_mean_similarity_to_group`.
- **different people** (both have known identities, none in common): no join by the extended-gap,
  look-back or no-people rules. A burst (within `time_gap_seconds`) is never blocked: a face hidden
  in one frame is not a change of people.
- `faces_same_allows_unknown: true` lets an unknown face stand in for a missing known person
  (off, [0011](../decisions/0011-unknown-face-does-not-stand-in.md)).
- anything else (no identified face on one side, partial overlap): the usual rules. A partial
  overlap ({A,B,C} vs {A,B,C,D}) therefore does not block a join, although the group rule says a
  person added or missing is another group. `faces_partial_overlap_blocks: true` would treat it as
  *different people*; it is off because most such pairs are a face not recognised in one frame
  ([0021](../decisions/0021-partial-overlap-does-not-split.md)).

The report shows faces and identities under each photo (`👤2 A,B`) and the badges *joined: same
people* / *kept apart: different people*. `cull.py faces --output … --sheets` writes one contact
sheet per identity to `faces_sheets/`. `faces.enabled: false` restores the face-free behaviour
exactly (tested).

## Report

- **Top:** totals, group-size histogram, photos per camera, thresholds used.
- **Body:** one row per group, by camera and in time order. Under each thumbnail: the time gap and
  similarity to the previous photo (for a group's first photo: the cut). Low similarities are
  highlighted. Click a thumbnail for the preview (←/→, Esc). Filters: hide singles, only flagged
  groups, one camera.
- **End:** *Problems* lists failed and undated files.
- *Label mode*: see [labels.md](labels.md).

## Tuning loop

Edit `config.yaml` → `cull.py group --output <out>` (re-groups from caches in seconds) →
`cull.py score --output <out>` against `labels.json` → look at `errors.jpg` and `report.html`.
Every change is checked on Talici 1 (over-splitting) **and** 4a (wrong merges) at least; see
[datasets](../datasets.md). Measurement history: [research](../research/).
