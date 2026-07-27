# LinkedIn JD Bot

Paste-first bot that extracts clean job description text from LinkedIn JDs.

## Approach

1. **LinkedIn job URL** — fetches via LinkedIn's public guest job endpoint first (`/jobs-guest/jobs/api/jobPosting/{id}`), then falls back to the normal job page  
2. **Paste text** — always works if a URL fetch fails  
3. **HTML file** — save page HTML and extract structured fields  
4. **Optional Playwright** — browser fetch / logged-in session (`--browser --storage-state`)

LinkedIn can still block or change endpoints. Guest fetch works for many public postings without login.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# optional browser fetch
pip install -e ".[browser]"
playwright install chromium
```

## Usage

```bash
# interactive paste / URL prompt
jd-bot

# paste JD text directly
jd-bot "Staff Engineer
Acme · Remote

Build APIs and own reliability.
- Python
- Postgres"

# from a file of pasted text
jd-bot -f jd.txt

# from saved LinkedIn HTML
jd-bot -f job.html

# try URL fetch (often blocked)
jd-bot "https://www.linkedin.com/jobs/view/1234567890"

# authenticated browser fetch
python scripts/save_linkedin_session.py --out linkedin_state.json
jd-bot --browser --storage-state linkedin_state.json "https://www.linkedin.com/jobs/view/1234567890"

# JSON output
jd-bot -f jd.txt --json -o out.json

# REPL loop
jd-bot interactive
```

## Library

```python
from linkedin_jd_bot import extract_job, extract_from_text, extract_from_html

job = extract_from_text(open("jd.txt").read())
print(job.title, job.company)
print(job.description)
```

## Tests

```bash
pytest
```
