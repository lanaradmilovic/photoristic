# Requirements — what the agency needs from the culling

The source of truth for what the pipeline has to do. Every later change of grouping or selection
is checked against this file.

Derived from what Peđa said, photo by photo, on the two pages shown at the meeting of 2026-11-19.
The evidence is in [interviews/2026-11-19-pedja-slika-po-slika.md](interviews/2026-11-19-pedja-slika-po-slika.md)
(Serbian): `M1–M20` disputed pairs, `X1–X13` group overview, `P1–P23` best-photo groups. The
numbers behind it are in [research/2026-11-23-meeting-choices-vs-signals.md](research/2026-11-23-meeting-choices-vs-signals.md).

The primary source is the user's own notes: she wrote them by hand while listening to the
recording. The automatic transcript only adds detail; where the two differ, her notes win
([list of differences](interviews/2026-11-19-pedja-slika-po-slika.md#gde-automatski-transkript-kaže-drugačije)).
Never correct a requirement from the automatic transcript; it decides only where a note
contradicts itself. What is in neither source was not said and is not a requirement.

How to use this file:

- A change of behaviour names the requirement it serves (`G2`, `K3`, …). IDs are stable.
- A requirement changes only when the agency says something new. Edit it here, add the date and the
  evidence; do not keep an old and a new version side by side.
- Every line says how sure it is: **said** (Peđa stated it as a rule), **shown** (it follows from
  what he chose on the photos), **ours** (our reading or proposal, not confirmed by the agency).
- Where his answers contradict each other, the line points to an [open question](#open-questions).
  Until it is answered, the **safe default** written there applies.
- The hard rule stays above everything here: never lose a good photo
  ([plan](plan.md#goal-and-the-hard-rule)).

How far this can be trusted:

- One person (Peđa) on one wedding (Talići), which he calls untypical (`S8`). Ksenija, who does the
  culling, said little.
- 20 pairs, 23 groups and about a dozen comments on the group overview. He answered quickly; a few
  clicks contradict the rule he stated in the same sentence (`Q8`, `Q9`).
- The meaning of the page answers is not reliable for grouping (`Q7`).

## Scope

| ID | | Requirement | Evidence |
|---|---|---|---|
| S1 | said | The tool is for culling **after** the wedding: the photos that go to the couple digitally. | general |
| S2 | said | Not for the photos printed and sold during the wedding (guests, guests with the couple, tables). There is no time; nothing is filtered, everything is printed. | general |
| S3 | said | It serves the main photographer and the assistants who follow the couple, not the secondary photographers who shoot guests. | general |
| S4 | said | Input is RAW (Peđa, Đole, Danilo) and JPG (everyone else). Both must work. Peđa's own weddings will not go through the tool. | general |
| S5 | said | The photos of both photographers of the day are put together, ordered by capture time, and the better frame is chosen across both. | X13 |
| S6 | said | There is no fixed number of photos to deliver. | M3 |
| S7 | said | No setup per wedding: the photographer will not mark the important people at the start (about 30 packages arrive after a weekend). Recognising the couple automatically was our proposal; he did not object (automatic transcript). | X4 |
| S8 | said | Talići is not typical: fully digital, no printing, two days, 70 guests, cocktail, spontaneous guest photos, a lot of time with the couple. A typical wedding gives 10–15 minutes with the couple, so a moment has fewer frames and more of them are kept. | X9, general |

## Principle

| ID | | Requirement | Evidence |
|---|---|---|---|
| C1 | said | The system removes what is bad. Everything good may go to the couple; they choose by their own taste. | general |
| C2 | said | Very similar good photos may be delivered. That is not an error; the couple choose among them. | general |
| C3 | said | A missing photo is worse than an extra one ("better than them chasing me later because something is gone"). Their clients like to get more photos. | P21, P19 |

## Groups

A group is the set of frames the selection rules (`K`) are applied to.

| ID | | Requirement | Evidence |
|---|---|---|---|
| G1 | said | A group is **literally the same moment**: the same people in the same pose or action, seconds apart. Not "a similar moment". Grouping must be stricter than now, as it was earlier. | general, X11 |
| G2 | shown | A new pose or a new action is a new group, also with the same people at the same place a moment later. | X6, X11, X12, M12, M16, M17 |
| G3 | said | Orientation is not a criterion. A horizontal and a vertical frame of exactly the same moment are the same picture; the question is "the same moment?", never "the same orientation?". | X6, M15, M20 |
| G4 | said | Black-and-white and colour are the same picture (the RAW is always colour). | M9 |
| G5 | shown | One continuous action stays one group: a walk (10 frames in 28 s), a kiss with the look before and the smile after (5 frames in 3 s), the couple standing at the altar (4 frames, one a minute later). | X2, X5, X8 |
| G6 | shown | Details of the same object are one group even when the framing differs a lot (the table in the church: wide, tighter, vertical). | X7 |
| G7 | shown | A frame that is darker or lighter because the flash fired or not is still the same moment. | X10, M13, M14 |
| G8 | said | The same picture with three people and then a fourth person joining: both frames are kept. | M10 |

`G1`/`G2` and `G3`/`G4`/`G6` pull in opposite directions for an algorithm that compares whole
frames: see [What this changes](#what-this-changes-in-the-pipeline).

## How many frames of a group stay

Applied in this order.

| ID | | Requirement | Evidence |
|---|---|---|---|
| K1 | said | Bad frames go out first (`B1–B6`). | general |
| K2 | said | Frames that are **exactly the same** ("baš iste"): one is enough and it does not matter which. This holds for the couple too ("if they are exactly the same I drop one"). See `Q2`. | P1, P8, P12, P16, P23, M6, M13, M18 |
| K3 | said | Important moments: every good frame stays, discard as little as possible. Named: the bride led in by her brother or father, the groom's entrance, the first meeting of the couple, the wedding ceremony, entering and leaving the church, the kiss, the first dance. | M2, M11, P3, P10, P13, P17, P21, X9 |
| K4 | said | The couple: every frame where they look good stays; only frames where they look bad go. | M2, M8, P9 |
| K5 | said | The closest family (mother, brother): all good frames stay. The photographer cannot know which one they will like. | M10, P18 |
| K6 | said | Guests and everybody else: few frames of a moment, all good ones stay (two stay two); many, a few are selected. Confirmed by the user from the recording, 2026-11-24. | M1, M2, P18, P19 |
| K7 | said | Few frames of a moment (two or three), all good: all stay. Many: select. "Few" and "many" count the frames of that one moment, as in the walk through the church: ten frames of one moment, a few are enough (the user from the recording, 2026-11-24). His numbers: 2–3 of 5; 2–3 or 3–4 of 10; 5 of 12; 2–3 of 15 photos of tables; 2 of 3–4 large group photos. | M1, M3, P6, P7, P15, P22, X5, X8, X9 |
| K8 | shown | When he selects from many, he keeps one frame per distinct look: before the kiss, the kiss, the smile (P2); full-length and cropped (P20). In a walk any two or three with a good step (P6). | P2, P6, P20 |
| K9 | said | Decor, food, interiors, tables, details: the same or a similar angle → one; different angles → two or three. Which one does not matter. | P5, P12, P16, P23, M18, X7 |
| K10 | said | A wide and a tight framing of a similar pose: both stay. See `Q1`. | M5, M10, P11, P13, P20 |
| K11 | said | When the system cannot know who a person is (mother or guest), keeping one of two near-identical frames is acceptable. | P18 |
| K12 | said, as a proposal | The system should notice that a moment has few frames and, when all are good, keep them; when there are too many, about 12, keep 5. | P7 |

## What makes a frame bad

| ID | | Requirement | Evidence |
|---|---|---|---|
| B1 | said | Closed eyes, unless they are intended (a "dreamy" pose) or natural (a kiss). Aftershoot cannot tell them apart and Peđa doubts a program can. | general, X12 |
| B2 | said | Blur that is a fault, not an artistic one. Slight blur can be recovered (Topaz), strong blur cannot. | general |
| B3 | said | Exposure that **cannot be recovered**. Highlights at 250–255 and blacks at 0–5 are lost; a strong flash can burn a white dress already at 230. Everything else can be pulled back: a lot from RAW, a little from JPG. **A frame that can be recovered is never rejected.** | M7, M14, X10 |
| B4 | said | A bad face or expression of the main people: mouth open, a yawning child, the groom not looking, "a critical face". | M3, M4, P4, P11 |
| B5 | shown | An unflattering body: a foot or hands in an odd position, legs. | M9, M20 |
| B6 | said | A frame too dark to judge is neither delivered as it is nor thrown away. It is fixed first and judged afterwards. See `Q6`. | M7, X10 |

Not a reason to reject:

| ID | | Requirement | Evidence |
|---|---|---|---|
| N1 | said | Shadows of other people (videographers) on the subject, a head or a hand at the edge of the frame, people standing behind a table. He wants them retouched (`R6`). | P7, P10, P11, P17, P22 |
| N2 | said | Some guest with closed eyes in a large group photo in harsh sun. | M3 |
| N3 | shown | Eyes closed in a kiss; smoke covering part of the frame in the smoke-bomb kiss. | P2, P21 |
| N4 | shown | A dark preview. The darker frame without flash can be the better one (M14). | M14, X10 |

## Which frame, when one is enough

| ID | | Requirement | Evidence |
|---|---|---|---|
| W1 | said | In a group photo look at the couple first. The clients care most that everybody is visible. | M3 |
| W2 | shown | Reasons he gave for one frame over another: the expression of the main person (M4, P4), a straight and level framing and a better pose (M14), a brighter face (M13), the wider framing when the frames are the same (M15), the lighter frame (P22). | as listed |
| W3 | said | Between exactly-same frames it does not matter: "would the other one do?" was answered yes five times of five. | P1, P8, P12, P18, P23 |

## Editing wishes (after culling, not part of the current work)

| ID | | Requirement |
|---|---|---|
| R1 | said | Editing comes after culling. The last step is one basic filter with slightly lower contrast. |
| R2 | said | Correct exposure and lift shadows; bring back overexposed frames (limits in `B3`). Harsh sun needs a filter that lowers highlights and lifts shadows instead of his usual presets. |
| R3 | said | Recovery is done on the RAW: "it can be pulled out of the RAW, and when it goes to JPG you get a DNG (digital negative file)". |
| R4 | said | Denoise for the church and the first dance (ISO 1200–1600); he uses 50 %, more looks plastic. |
| R5 | said | Straighten the frame, correct perspective, extend a cut-off dress with AI (M12). |
| R6 | said | Remove shadows of other people, remove a head that entered the frame (P7, P10, P17). A strong wish. |
| R7 | said | One edit applied to all similar frames (Lightroom's sync does this). |
| R8 | said | Slightly blurred frames can be sharpened (Topaz AI). |

## What the system cannot know

To be kept in mind when a rule above needs it:

- who is family and which guest matters to the couple (`S7`, `K11`);
- whether closed eyes were intended (`B1`);
- what happened at a particular wedding (automatic transcript only, said in reply to `K12`).

## Open questions

Contradictions in the answers. "Ask" says who can resolve it.

Q1–Q3 and Q6 are ready to be asked on one page (five questions): `cull.py meeting --output data\questions`
([spec](spec/labels.md#agency-meeting-page), [0024](decisions/0024-contradictions-side-by-side.md)).
Q2 is asked as two questions there: pairs that are exactly the same, and long series of one moment.
Q11–Q14 were added to the same page on 2026-11-25 (four more questions).

**Q1 — A wider and a tighter (or a horizontal and a vertical) frame of the same pose: one or both?**
- Both: M5 (couple at the tables; the wide one shows the table), M10 (family), M14 (groom, with and
  without flash), P20 (guests: one full-length, one cropped), P11, P13.
- One: M15 (couple on the pier: "they are the same", the wider one), M20 (mother giving a speech:
  the tighter one), M9 (groom on the boat).
- The stated rules collide: `K10` says keep both, `G3` says a horizontal and a vertical of the
  same moment are the same picture.
- Safe default: keep both.
- Ask Peđa: when is a second framing of the same pose worth keeping?

**Q2 — Where does "exactly the same" end?**
- One: P1 (two frames at the altar, an important moment, the couple), M13.
- All: P21 (nine burst frames of one kiss; only the smoke changes), M2 and P10 (one second apart,
  only the step or a hand differs), P15.
- He calls the first "baš iste" and the second "nisu skroz iste". Similarity does not separate
  them: 0.95 for P1 and 0.95 for M2 ([research](research/2026-11-23-meeting-choices-vs-signals.md)).
- Safe default: "the same" only when nothing about the main people differs; otherwise keep both.
  In an important moment (`K3`) keep both in any case.
- How the program sees these two pairs: the similarity is 0.953 and 0.951, the same for it. It keeps one of P1 and both of M2, but only because a bystander's face was recognised on one frame of M2 and not on the other. On a crop around the couple the two pairs do separate (patch similarity 0.88 against 0.65), but over twenty pairs the crop does not separate his "one" from "both" ([research](research/2026-11-24-same-or-not-two-pairs.md)).
- Ask Peđa with three or four such pairs side by side.

**Q3 — The bride or the couple alone in similar frames: one or both?**
- One: M6 (bride in the old town, 30 s apart, head turned differently: "whichever, not that
  important"), M13, M15.
- Both: P9 (bride at the tables, 7 s apart: "a bride wants all her photos"), M8.
- Our reading, not confirmed: the posed sessions (boat, old town, pier) have many frames and get
  a selection; at the venue there were few.
- Safe default: keep both.
- Ask Peđa.

**Q6 — Dark frames and the order of the steps.**
- "Editing comes after culling" (`R1`), but a dark frame cannot be judged before it is fixed (M7:
  "I would give them nothing" as it is) and "I fix them and then choose the best" (X10).
- Safe default: a dark but recoverable frame passes culling unjudged and is marked "fix exposure
  first".
- Ask Ksenija what she does with such frames in JPG packages.

**Q7 — What the answers on the pair page mean for grouping.**
- "Same moment, both" was clicked for frames he called a different moment (M17) and for frames
  that are the same moment and both good (M2, M8). M12 ("different pictures") has no click.
- In `meeting_answers.json` every `both` answer is stored as label `same`. With `G1` that is wrong
  for some of them, so the file cannot be used as grouping ground truth as it is.
- The user decides pair by pair from the recording, or the pairs are asked again with the question
  "would you choose between these two?".

**Q8 — Which frames of a long series.**
- P6: "what matters is that they have two or three", clicked four of ten, three of them
  consecutive and nearly identical, which `K2` would reduce to one.
- Use what he said: the count matters, the exact frames do not.

**Q9 — Two clicks stricter than the rule stated with them.**
- P5: "different angles → two or three", kept one of three although the first is another angle.
- P22: "two photos of the table → both", kept one of two.
- Use the stated rule; it keeps more.

**Q11 — A new pose a few seconds later: the same moment or a new picture?**
- `G1`/`G2` say a new pose is a new group, `G5` keeps the look, the kiss and the smile (3 s)
  together. Between them: a look and a near-kiss 4 s later, a hug and a wave 10 s later
  (Talići 1 `7978`/`7979`, `8255`/`8256`). The labellers gave both answers
  ([research](research/2026-11-25-labels-v3-and-signal-ceiling.md)).
- Safe default: a new group when more than 2 s apart ([0026](decisions/0026-labelling-checks.md)).
- Ask Peđa: question `nova-poza` on the question page.

**Q12 — The same pose shot from another side: the same moment or a new picture?**
- `G3` says framing and orientation are not the criterion; nothing was said about the photographer
  walking around the subjects (4a `0072`/`0073`, Talići 1 `8059`/`8060`).
- Safe default: a new group when the subjects are seen from the opposite side.
- Ask Peđa: question `druga-strana`.

**Q13 — Scenery from two spots: one subject or two pictures?**
- `K9` and `G6` cover details of one object. For a house or a garden shot from two places
  (Talići 1 `8516`/`8517`, `8705`/`8706`) the labellers gave both answers.
- Safe default: a new group for another view.
- Ask Peđa: question `prostor`.

**Q14 — May the program drop a frame by itself only when frames are practically the same?**
- Ours, from `C1`–`C3` and `K2`: the program removes bad frames and practically identical ones
  (a burst), keeps every other similar frame and only shows them together. `K7` (many frames of
  one moment, a few are enough) asks for more than that.
- Safe default: drop only bad and practically identical frames.
- Ask Peđa: question `sme-da-izbaci`.

### Resolved

- **Q4 — Guests: one or all?** Resolved 2026-11-24 by the user from the recording: he said it was
  fine that both frames stayed, as he also decided for the guests under the parasol. Two frames
  stay two; with many frames a few would be selected. Now in `K6`.
- **Q5 — "Few" and "many" frames of what?** Resolved 2026-11-24 by the user from the recording:
  the frames of that one moment. The walk through the church is the example of many frames of one
  moment, where a few are enough. Now in `K7`. P22 (two frames of the table, one kept) stays under
  `Q9`.
- **Q10 — Two photographers in the Talići folders.** Resolved 2026-11-24: all five folders come
  from one camera body (one serial number), so every photo is Peđa's and Đole's photos of that day
  are not among them. `S5` still cannot be measured without a wedding from two cameras
  ([todo](todo.md)).

## What this changes in the pipeline

Ours; to be turned into decisions and todo items, not decided here.

- **Group rule.** Decided: [0025](decisions/0025-group-definition-v3.md) replaces 0014. A pose
  taken on purpose starts a new group; one continuous action, a wider or tighter framing and a
  vertical against a horizontal frame of the same moment stay one group. The labels of 4a and
  Talići 1 were redone against it on 2026-11-25 ([0026](decisions/0026-labelling-checks.md)); the
  current thresholds already score as well as similarity and gap can
  ([research](research/2026-11-25-labels-v3-and-signal-ceiling.md)).
- **"Stricter" is not only a higher similarity threshold.** Pairs he confirmed as one group have a
  DINOv2 similarity of 0.80–0.91, pairs he cut 0.73–0.82, and pairs he calls "the same" go down to
  0.65–0.71 (orientation, black-and-white against colour, details). Two of his three cuts are
  look-back joins 75–117 s apart
  ([research](research/2026-11-23-meeting-choices-vs-signals.md)).
- **Selection.** One winner per variant ([0022](decisions/0022-variants-in-code-model-ranks.md)) is
  stricter than `K3`–`K7` and `K10`. The order `K1` → `K2` → keep the rest is the safe core;
  everything beyond it needs signals the pipeline does not have: who is in the frame (the couple
  can be recognised, `S7`) and how important the moment is.
- **Exposure.** A check on the embedded preview must not count recoverable darkness against a
  frame (`B3`, `N4`). Many previews are black-and-white although the RAW is colour (`G4`).
- **Closed eyes.** A kiss is not a defect (`N3`): the per-photo check marked all nine frames of
  P21 "eyes closed" and all nine were kept.
- **Two cameras.** `S5` contradicts grouping per camera
  ([0003](decisions/0003-camera-by-serial-group-per-camera.md)).
