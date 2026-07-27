# cursorRepo

This repository hosts several small, independent learning projects. Each product lives on its **own branch** — the `main` branch intentionally contains only this file and `README.md`.

| Product | Branch | Directory | Stack |
|---------|--------|-----------|-------|
| Exam Quiz App | `cursor/exam-quiz-app-ec92` | `quiz-app/` | Static HTML/CSS/vanilla JS |
| Wortkarte (German flashcards) | `cursor/german-flashcard-app-a7bb` | `flashcard-app/`, `flashcard-share/` | Static HTML/CSS/vanilla JS, PWA |
| LinkedIn JD Bot | `cursor/linkedin-jd-bot-be67` | `linkedin_jd_bot/`, `tests/` | Python 3.11+ CLI package |

## Cursor Cloud specific instructions

- **Products live on separate branches, not on `main`.** To work on one, check out its branch (or use a `git worktree` per branch so multiple can run at once). `main` has no application code.
- **Static apps (Quiz, Wortkarte)** have no dependencies and no build step. Serve over HTTP (not `file://`, which breaks Wortkarte's service worker/PWA): from the app directory run `python3 -m http.server <port>` (e.g. quiz on 8080, flashcard on 8081) and open `http://localhost:<port>/`. There is no lint/test/build tooling for these — testing is manual in the browser. Flashcard progress/custom words persist in `localStorage`.
- **LinkedIn JD Bot** (`cursor/linkedin-jd-bot-be67`): install with `pip install --break-system-packages -e ".[dev]"` from the branch root (Ubuntu's Python is externally managed, hence `--break-system-packages`; the update script does this automatically when `pyproject.toml` is present). Optional browser fetch: `pip install --break-system-packages -e ".[browser]"` then `playwright install chromium`.
  - Run tests with `python3 -m pytest`. Note `tests/test_company_enrich.py::test_enrich_shiftmove_live` makes a real network request.
  - The `jd-bot` console script installs to `~/.local/bin`, which is not on `PATH` by default — either add it to `PATH` or run the module directly via `python3 -m linkedin_jd_bot.cli`.
  - Core usage is paste-first: pipe/paste JD text to `jd-bot` (structured extraction), add `--json` for machine output, `--enrich` to prefer the employer ATS, `--browser --storage-state <file>` for authenticated fetch.
