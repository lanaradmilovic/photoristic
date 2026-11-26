# Codebook: why a photo was rejected

The reason codes reviewers give to every rejected photo of a wedding (`reasons.jsonl`, format in
[spec](../spec/wedding-analysis.md#reasonsjsonl)). A code is the reviewer's reading of the
editor's choice, never the editor's word. Change a code only by a new version: summaries of
older weddings name the version they used.

**Current version: 2.** Glamur was reviewed with version 1 (mapping at the end).

## Rules for the reviewer

- Compare the rejected frame with the kept frames of the same moment, same camera first. Open the
  1536 px preview whenever the thumbnail does not show the reason (eyes, focus, expression
  always need it).
- One `primary` code, optionally one `secondary`. When two apply, the primary is the one that
  would decide it alone.
- A code that compares (SAME, EYES, EXPR, FACE, VERSION) needs `kept_alt`: the kept frame it
  was compared with.
- `note`: what you see, short, in English (e.g. "groom's eyes closed, 3724 same pose eyes
  open"). No names, no description of a guest beyond what the reason needs.
- When the thumbnail looks the same, look again at eyes, mouth, hands and the edges before
  writing SAME. In Glamur 3 of 8 checked `DUP` were a worse twin.

## Codes

| Code | Definition | Use when | Do not use when | Glamur examples (v1) |
|---|---|---|---|---|
| `SAME` | near-identical to a kept frame, no visible difference in quality | burst thinning; you checked eyes, mouth, hands, edges in the preview and found nothing | any difference you can name: use that code | `JAS_3340` (= 3339), `JAS_3601` |
| `EYES` | closed, half-closed or blinking eyes of an important person | the kept twin has the eyes open | a kiss or a laugh where closed eyes are the moment; eyes of a guest at the back | `JAS_3306` (3307 open), `KNEZ4338` |
| `FACE` | an important person's face is hidden or turned away: behind another person, hands, a glass, the cake, back to camera | the kept twin shows the face | the face is visible but the expression is worse (`EXPR`) | `JAS_3269` (bride behind a guest), `JAS_4026` (both backs) |
| `EXPR` | the face is visible, the expression is worse than the kept twin: mid-word, grimace, chewing, looking away, eyes down | the difference is in the face itself | the face is hidden (`FACE`) or the eyes are closed (`EYES`) | `LPZ_3569` (serious vs slight smile) |
| `COMP` | framing: something blocks the scene (a guest's head, an arm, the priest's robe, a waiter, a blurred foreground), subject cut off, tilted | the block is in the frame, not on the key face | the blocker is crew (`CREW`) or hides the key face (`FACE`) | `JAS_4023` (arm blocks a third), `JAS_4247` |
| `CREW` | the videographer, another photographer or their gear is in the frame | anyone of the crew is visible enough to notice | a guest with a phone (`COMP`) | `KNEZ3747`, `KNEZ4189` |
| `FOCUS` | missed focus or motion blur on the subject | the subject is soft | intended motion blur (creative frames are kept) | `JAS_4050` |
| `EXPO` | flash did not fire, too dark or too bright, colour cast or flare on faces | the light hurts the faces | a dark frame that looks intended (often kept) | `KNEZ5385` (purple cast) |
| `VERSION` | another version of a kept frame: in-camera crop, colour vs B/W, horizontal vs vertical, wide vs tight of the same instant | the kept frame is the same instant in another version | a different instant (`SAME` or another code) | `LPZ_4141` (crop of 4137), `JAS_3790` |
| `MOMENT` | in-between instant: nothing happens, the action is over or not yet started, people walking out | a kept frame has the moment itself | the moment is the same and only faces differ | `KNEZ4003` (before the kiss of the cross) |
| `NOCOUPLE` | guests only, low interest, not a key person | the frame has no couple or family and adds nothing | guests at the logo wall or table portraits, where one per guest is the rule: use `SAME`/`VERSION` for the repeat | `LPZ_3748` |
| `DETAIL` | a detail, decor or scenery frame redundant with kept details | enough of the same detail is kept | the only frame of that detail | `KNEZ5217` (cake, = 5218) |
| `UNCLEAR` | no visible reason; looks as good as the kept frames | you looked at the preview and found nothing | – | 24 in Glamur, mostly LPZ |

## loss and conf

- `loss`: would a demanding client miss this photo? `no` (fine to drop), `maybe` (taste),
  `yes` (better than or different from what was kept). Every `yes` is checked against all
  cameras before it is reported as a loss.
- `conf`: `high` (the reason is plain in the preview), `medium`, `low` (a guess).

## Agreement

On every wedding about 10 % of the rejects (at least 50, spread over cameras and parts of the
day) are coded by a second reviewer who does not see the first answer. The analysis reports
the agreement per code. A code with poor agreement gets a clearer definition and a new version,
not a majority vote.

## Versions

| Version | Change | Used by |
|---|---|---|
| 1 | first codes, from the Glamur brief (`posle-analiza/review/BRIEF.md`) | Glamur |
| 2 | `DUP` → `SAME` with a stricter check; face hidden or turned away moved from `EXPR` to new `FACE`; `CROP` widened to `VERSION` (also B/W, orientation, wide/tight) | – |

Version 1 to 2: `CROP` → `VERSION`; `DUP` → `SAME`, `EYES`, `EXPR`, `FACE`, `COMP` or
`VERSION` (not knowable without a second look); `EXPR` → `EXPR` or `FACE`; all other codes are
unchanged. Compare a v1 wedding with a v2 one on the merged groups `SAME+VERSION` (thinning)
and `EYES+EXPR+FACE` (faces), and say so.
