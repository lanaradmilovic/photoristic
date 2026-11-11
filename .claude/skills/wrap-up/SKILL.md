---
name: wrap-up
description: End-of-session documentation update for Photoristic - updates docs/todo.md and docs/log.md, writes decision records for decisions made or ideas rejected, updates docs/spec and docs/research. Use when the user says the session is ending, asks to wrap up, or asks to record what was done.
---

# Wrap up the session

Go through the conversation and the git diff of this session (`git status`, `git diff`,
`git log` since the session started), then update the docs. English, short, link instead of copy.

1. **docs/todo.md** — remove items that are done; add new open items in the right section
   (Now / Next / Later); mark items that need the user with **(user)**.
2. **docs/log.md** — append `## Session N — YYYY-MM-DD` with 3–6 bullets: what changed (with commit
   hashes), what was decided (link the decision), test count, what stays open. No measurement tables.
3. **docs/decisions/** — for every decision the user made and every idea that was tried and
   rejected in this session: copy `_template.md` to the next free number, fill in context, options,
   decision with the *why*, consequences, evidence; add a row to `docs/decisions/README.md`. If it
   replaces an older decision, change only the old one's `Status` line to `superseded by NNNN`.
4. **docs/spec/** — if behaviour, commands, config keys or file formats changed, update the matching
   spec so it describes the code as it is now.
5. **docs/research/** — new measurements or experiments go into a new
   `YYYY-MM-DD-<topic>.md` (data, numbers, what was concluded). Never edit an old research note.
6. **CLAUDE.md** — touch only if a project-wide rule or environment fact changed. Keep it under ~60 lines.

Finally show the user a short summary of what was updated, and ask before committing.
