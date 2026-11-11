# Photoristic — automatic culling of wedding photos

Pre-selects 2,000–3,000 wedding photos (two photographers, NEF/JPG) so the agency reviews for ~20
minutes instead of culling for 3 hours.

## Hard rules
- **Never lose a good photo.** A false reject is the failure; a false keep or a missed merge only
  costs review time. When in doubt: split groups, send photos to review.
- **Privacy:** photos show guests' faces. Nothing leaves the machine except to the user's own vLLM
  server. Never log image content or base64.
- Simple, readable code, no over-abstraction, no frameworks. Every tunable lives in `config.yaml`
  (defaults in `culling/config.py`; unknown keys are errors).
- No model training before phase 7. No GUI except static HTML reports.
- A grouping change is measured, not eyeballed: `cull.py score` on labelled folders, before and after.

## Environment
- Windows, Python 3.11, CPU only. Always use `.venv\Scripts\python` (system Python has no `rawpy`).
- Tests: `.venv\Scripts\python -m pytest` (synthetic data only). CLI: `cull.py`, see README.
- Main branch is `main`; feature work on its own branch. Test data is in `data/` and OneDrive, never in git.
- The Chrome extension cannot open localhost here; verify report UI with headless Chrome ([spec/labels.md](docs/spec/labels.md#verifying-the-report-ui)).

## Documentation (read on demand)
| File | Read when |
|---|---|
| [docs/todo.md](docs/todo.md) | **at the start of every session** — what is next |
| [docs/plan.md](docs/plan.md) | goal, fixed constraints, phases |
| [docs/decisions/](docs/decisions/README.md) | before changing behaviour — was it decided or already rejected? |
| [docs/spec/](docs/spec/) | how ingest, grouping, faces, labels, VLM judge/scoring and output files work now |
| [docs/research/](docs/research/) | measurements and experiments behind decisions (dated, never edited) |
| [docs/datasets.md](docs/datasets.md) | where the five test folders and their outputs are |
| [docs/log.md](docs/log.md) | what happened in earlier sessions |

One fact lives in one place; link instead of copying. Current threshold values are only in `config.yaml`.

## End of session (or run `/wrap-up`)
1. `docs/todo.md`: remove done items, add new ones.
2. `docs/log.md`: append a short entry with links.
3. A decision was made or an idea rejected → new file in `docs/decisions/` + index row.
4. Behaviour or file formats changed → update `docs/spec/`. New measurements → `docs/research/YYYY-MM-DD-*.md`.
