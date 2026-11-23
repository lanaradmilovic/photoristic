# 0024 — Contradicting answers are asked again as two examples side by side

- Status: proposed (implemented; the user has not reviewed the page yet)
- Date: 2026-11-23
- Decided by: agent, on the user's request for a question page and for the best way to show contradictions

## Context
Peđa's answers on the meeting pages of 2026-11-19 contradict each other in several places
([requirements Q1–Q5](../requirements.md#open-questions)): the same kind of pair got "one" here and
"both" there. He saw one pair or one group per screen. The user wants a page with clear questions
that he can answer without hesitating, in the simple style of the earlier pages.

## Options considered
1. **Ask the rule in words** ("wide and tight framing: one or both?") — quick, but abstract; he has
   already given both answers to the rule.
2. **Show the old pairs again, one per screen** — the same way of judging that produced the
   contradictions.
3. **The two contradicting examples next to each other, each with what he said then, and written
   reasons to choose from.**

## Decision
Option 3, as a new step type of the meeting page (`questions` in `meeting.json`,
[spec](../spec/labels.md#agency-meeting-page)).

- **Side by side.** Choices made one option at a time and choices made with the options next to
  each other differ, because a feature that is hard to judge alone becomes easy to compare (joint
  against separate evaluation, Hsee 1996; Hsee, Loewenstein, Blount and Bazerman 1999). His first
  answers were all given separately.
- **The nearest contrast.** People explain a choice as "this rather than that", and the case it is
  contrasted with matters (Buçinca et al. 2025). Each card pairs the two examples that differ
  least and were answered differently: same people, same kind of difference.
- **Same layout on both sides, the difference marked.** A small fixed comparison works as two
  identical columns with the differing value highlighted (NN/g on comparison tables, Baymard on
  comparison tools). Here: the same card twice, the earlier answer as a coloured tag.
- **No blame.** The card says that both answers can be right and asks what makes the difference.
  Telling a respondent only that two answers conflict does not make the next answers better (a
  survey study found by the search; not read in full).
- **Reasons as answers.** Three or four written reasons, each one a rule the program can follow,
  plus "Drugačije" with a note. One question per screen, number keys, a list of all answers at the
  end.

Not option 1 or 2: both repeat a situation in which he already answered both ways.

## Consequences
- The examples and the wording are written by hand for every meeting; the wording of an answer is
  stored with it in `meeting_answers.json` (`choices`).
- Seen next to each other, small differences can weigh more than they do when a photo is seen
  alone (a known limit of joint evaluation). Every contrast card therefore offers a "no
  difference" answer.
- The written reasons are our guesses and can lead him; "Drugačije" and the note are on every
  screen, and the note should be read before the click is counted.
- The sources were read as search summaries on 2026-11-23, not in full.

## Evidence
- Hsee, Loewenstein, Blount, Bazerman 1999, preference reversals between joint and separate
  evaluation: <https://www.cmu.edu/dietrich/sds/docs/loewenstein/PrefRevJoint.pdf>; Hsee 1996, the
  evaluability hypothesis: <https://is.muni.cz/el/phil/jaro2017/PSX_512/um/BE_1996_Hsee.pdf?lang=en>
- Buçinca et al. 2025, contrastive explanations: <https://kgajos.seas.harvard.edu/papers/bucinca2025contrastive.pdf>
- NN/g, comparison tables: <https://nngroup.com/articles/comparison-tables/>; Baymard, comparison
  tools: <https://baymard.com/blog/user-friendly-comparison-tools>
- Tests: `tests/test_meeting.py`. The page was checked in the Browser pane at 1366×768: answers by
  click and by key, "Drugačije" with a note, the list at the end, `meeting-score`.
