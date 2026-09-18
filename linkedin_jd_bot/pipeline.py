from __future__ import annotations

from typing import Optional

from linkedin_jd_bot.cleaner import clean_text, guess_title_company_from_paste
from linkedin_jd_bot.company_enrich import maybe_enrich_job
from linkedin_jd_bot.extractor import parse_linkedin_html
from linkedin_jd_bot.fetcher import fetch_job_html
from linkedin_jd_bot.models import JobDescription, SourceKind
from linkedin_jd_bot.urls import canonicalize_job_url, is_linkedin_job_url, looks_like_url


class ExtractionError(Exception):
    """Raised when a JD cannot be extracted."""


def extract_from_text(
    text: str,
    *,
    url: Optional[str] = None,
    title: Optional[str] = None,
    company: Optional[str] = None,
) -> JobDescription:
    cleaned = clean_text(text)
    if len(cleaned) < 40:
        raise ExtractionError("Pasted text is too short to be a job description")

    guessed_title, guessed_company = guess_title_company_from_paste(cleaned)
    return JobDescription(
        title=title or guessed_title,
        company=company or guessed_company,
        description=cleaned,
        url=canonicalize_job_url(url) if url and is_linkedin_job_url(url) else url,
        source=SourceKind.PASTE,
        raw_length=len(cleaned),
    )


def extract_from_html(
    html: str,
    *,
    url: Optional[str] = None,
    source: SourceKind = SourceKind.HTML,
) -> JobDescription:
    parsed = parse_linkedin_html(html)
    description = parsed.get("description")
    if not description:
        # Last resort: clean all body text
        from bs4 import BeautifulSoup

        body = BeautifulSoup(html, "lxml").get_text("\n", strip=True)
        description = clean_text(body)
    if not description or len(description) < 40:
        raise ExtractionError(
            "Could not find a job description in the HTML. "
            "Paste the JD text instead."
        )

    canonical = None
    if url and is_linkedin_job_url(url):
        canonical = canonicalize_job_url(url)

    return JobDescription(
        title=parsed.get("title"),
        company=parsed.get("company"),
        location=parsed.get("location"),
        employment_type=parsed.get("employment_type"),
        seniority=parsed.get("seniority"),
        description=description,
        url=canonical or url,
        linkedin_url=canonical if canonical else None,
        source=source,
        raw_length=len(description),
    )


def extract_job(
    input_value: str,
    *,
    use_browser: bool = False,
    storage_state: Optional[str] = None,
    headless: bool = True,
    html_file: bool = False,
    enrich: bool = False,
) -> JobDescription:
    """
    Main entry: accept a LinkedIn URL, pasted JD text, or HTML document.
    When enrich=True, try to replace LinkedIn text with the employer ATS JD.
    """
    value = input_value.strip()
    if not value:
        raise ExtractionError("Empty input")

    if html_file or (value.lstrip().startswith("<") and "</" in value):
        job = extract_from_html(value, source=SourceKind.HTML)
    elif looks_like_url(value):
        if not is_linkedin_job_url(value):
            raise ExtractionError("URL does not look like a LinkedIn job posting")
        result = fetch_job_html(
            value,
            use_browser=use_browser,
            storage_state=storage_state,
            headless=headless,
        )
        if result.blocked:
            detail = result.message or "login wall, anti-bot, or missing job page"
            raise ExtractionError(
                f"LinkedIn fetch failed ({detail}). "
                "Retry with `--browser`, or `--browser --storage-state path/to/linkedin.json` "
                "after exporting a logged-in session via "
                "`python scripts/save_linkedin_session.py`. "
                "As a fallback, save the page as HTML (`jd-bot -f page.html`) "
                "or paste the JD text."
            )
        job = extract_from_html(
            result.html,
            url=result.url,
            source=SourceKind.FETCH,
        )
    else:
        job = extract_from_text(value)

    if enrich:
        job, _note = maybe_enrich_job(job)
    return job
