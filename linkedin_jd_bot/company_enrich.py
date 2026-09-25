from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from linkedin_jd_bot.cleaner import clean_text
from linkedin_jd_bot.extractor import _description_from_element
from linkedin_jd_bot.models import JobDescription, SourceKind

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/html",
    "Accept-Language": "en-US,en;q=0.9",
}

RECRUITER_HINTS = (
    "recruit",
    "staffing",
    "talent partner",
    "talent acquisition agency",
    "search firm",
    "headhunt",
    "rpo",
    "socially responsible recruitment",
    "sr2",
)

ATS_SLUG_RE = re.compile(r"[^a-z0-9]+")


@dataclass
class EnrichmentResult:
    job: Optional[JobDescription]
    attempted: list[str]
    message: str = ""


def company_slug_candidates(company: str) -> list[str]:
    raw = company.lower()
    raw = re.sub(r"[™®]", "", raw)
    raw = re.sub(r"\([^)]*\)", " ", raw)
    # Drop common legal suffixes / noise after | or dash
    raw = re.split(r"[|–—]", raw)[0]
    raw = re.sub(
        r"\b(inc|llc|ltd|gmbh|ag|corp|corporation|company|co|plc|group)\b\.?",
        " ",
        raw,
    )
    slug = ATS_SLUG_RE.sub("", raw).strip()
    dashed = ATS_SLUG_RE.sub("-", company.lower())
    dashed = re.sub(r"-{2,}", "-", dashed).strip("-")
    out: list[str] = []
    for candidate in (slug, dashed, dashed.replace("-", "")):
        if candidate and candidate not in out and len(candidate) >= 2:
            out.append(candidate)
    return out


def looks_like_recruiter(company: Optional[str], description: str = "") -> bool:
    blob = f"{company or ''}\n{description[:500]}".lower()
    if any(h in blob for h in RECRUITER_HINTS):
        return True
    if re.search(r"\bwe(?:'re| are) (?:partnering|hiring on behalf)\b", blob):
        return True
    return False


def _normalize_title(title: str) -> str:
    text = title.lower()
    text = re.sub(r"\(.*?\)", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def title_similarity(a: str, b: str) -> float:
    na, nb = _normalize_title(a), _normalize_title(b)
    if not na or not nb:
        return 0.0
    if na == nb:
        return 1.0
    if na in nb or nb in na:
        return 0.9
    sa, sb = set(na.split()), set(nb.split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def _html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    root = soup.body or soup
    return _description_from_element(root) if root else clean_text(soup.get_text("\n"))


def _location_from_workable(job: dict) -> Optional[str]:
    loc = job.get("location") or {}
    parts = [loc.get("city"), loc.get("region"), loc.get("country")]
    value = ", ".join(p for p in parts if p)
    return value or None


def enrich_via_workable(
    client: httpx.Client,
    *,
    company: str,
    title: str,
    linkedin_url: Optional[str] = None,
) -> tuple[Optional[JobDescription], list[str]]:
    attempted: list[str] = []
    best: Optional[tuple[float, JobDescription]] = None

    for slug in company_slug_candidates(company):
        list_url = f"https://apply.workable.com/api/v1/accounts/{slug}/jobs"
        attempted.append(list_url)
        response = client.post(list_url, json={})
        if response.status_code != 200:
            continue
        try:
            payload = response.json()
        except ValueError:
            continue
        results = payload.get("results") or []
        for item in results:
            item_title = item.get("title") or ""
            score = title_similarity(title, item_title)
            if score < 0.55:
                continue
            shortcode = item.get("shortcode")
            if not shortcode:
                continue
            detail_url = (
                f"https://apply.workable.com/api/v1/accounts/{slug}/jobs/{shortcode}"
            )
            attempted.append(detail_url)
            detail = client.get(detail_url)
            if detail.status_code != 200:
                continue
            try:
                data = detail.json()
            except ValueError:
                continue
            html = data.get("description") or ""
            if not html or len(html) < 40:
                continue
            description = _html_to_text(html)
            source_url = f"https://apply.workable.com/{slug}/j/{shortcode}/"
            job = JobDescription(
                title=data.get("title") or item_title,
                company=company.split("|")[0].strip(),
                location=_location_from_workable(data) or _location_from_workable(item),
                employment_type=(
                    "Full-time"
                    if data.get("type") == "full"
                    else ("Contract" if data.get("type") == "contract" else None)
                ),
                description=description,
                url=source_url,
                linkedin_url=linkedin_url,
                source=SourceKind.COMPANY,
                raw_length=len(description),
            )
            if best is None or score > best[0]:
                best = (score, job)
        if best:
            break
    return (best[1] if best else None), attempted


def enrich_via_greenhouse(
    client: httpx.Client,
    *,
    company: str,
    title: str,
    linkedin_url: Optional[str] = None,
) -> tuple[Optional[JobDescription], list[str]]:
    attempted: list[str] = []
    best: Optional[tuple[float, JobDescription]] = None
    for slug in company_slug_candidates(company):
        list_url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
        attempted.append(list_url)
        response = client.get(list_url)
        if response.status_code != 200:
            continue
        try:
            payload = response.json()
        except ValueError:
            continue
        for item in payload.get("jobs") or []:
            item_title = item.get("title") or ""
            score = title_similarity(title, item_title)
            if score < 0.55:
                continue
            html = item.get("content") or ""
            if not html:
                continue
            description = _html_to_text(html)
            loc = None
            if item.get("location") and isinstance(item["location"], dict):
                loc = item["location"].get("name")
            source_url = item.get("absolute_url") or (
                f"https://boards.greenhouse.io/{slug}/jobs/{item.get('id')}"
            )
            job = JobDescription(
                title=item_title,
                company=company.split("|")[0].strip(),
                location=loc,
                description=description,
                url=source_url,
                linkedin_url=linkedin_url,
                source=SourceKind.COMPANY,
                raw_length=len(description),
            )
            if best is None or score > best[0]:
                best = (score, job)
        if best:
            break
    return (best[1] if best else None), attempted


def enrich_via_lever(
    client: httpx.Client,
    *,
    company: str,
    title: str,
    linkedin_url: Optional[str] = None,
) -> tuple[Optional[JobDescription], list[str]]:
    attempted: list[str] = []
    best: Optional[tuple[float, JobDescription]] = None
    for slug in company_slug_candidates(company):
        list_url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
        attempted.append(list_url)
        response = client.get(list_url)
        if response.status_code != 200:
            continue
        try:
            payload = response.json()
        except ValueError:
            continue
        if not isinstance(payload, list):
            continue
        for item in payload:
            item_title = item.get("text") or ""
            score = title_similarity(title, item_title)
            if score < 0.55:
                continue
            lists = item.get("lists") or []
            chunks = [item.get("descriptionPlain") or item.get("description") or ""]
            for block in lists:
                header = block.get("text") or ""
                content = block.get("content") or ""
                chunks.append(f"{header}\n{content}".strip())
            description = clean_text("\n\n".join(c for c in chunks if c))
            if len(description) < 40:
                continue
            loc = None
            cats = item.get("categories") or {}
            if isinstance(cats, dict):
                loc = cats.get("location")
            job = JobDescription(
                title=item_title,
                company=company.split("|")[0].strip(),
                location=loc,
                description=description,
                url=item.get("hostedUrl") or item.get("applyUrl"),
                linkedin_url=linkedin_url,
                source=SourceKind.COMPANY,
                raw_length=len(description),
            )
            if best is None or score > best[0]:
                best = (score, job)
        if best:
            break
    return (best[1] if best else None), attempted


def enrich_from_company_site(
    *,
    title: str,
    company: str,
    description: str = "",
    linkedin_url: Optional[str] = None,
    timeout: float = 20.0,
) -> EnrichmentResult:
    """
    Given LinkedIn title/company, try to pull a cleaner JD from the employer's ATS.
    Currently probes Workable, Greenhouse, and Lever public boards.
    """
    if not title or not company:
        return EnrichmentResult(
            job=None,
            attempted=[],
            message="Need both title and company to search employer careers pages",
        )

    if looks_like_recruiter(company, description):
        return EnrichmentResult(
            job=None,
            attempted=[],
            message=(
                f"'{company}' looks like a recruiter/agency posting, so the real "
                "employer careers page is unknown. LinkedIn text is the best source."
            ),
        )

    attempted: list[str] = []
    with httpx.Client(headers=DEFAULT_HEADERS, follow_redirects=True, timeout=timeout) as client:
        for enricher in (enrich_via_workable, enrich_via_greenhouse, enrich_via_lever):
            job, tried = enricher(
                client,
                company=company,
                title=title,
                linkedin_url=linkedin_url,
            )
            attempted.extend(tried)
            if job:
                return EnrichmentResult(job=job, attempted=attempted, message="")

    return EnrichmentResult(
        job=None,
        attempted=attempted,
        message=(
            f"No matching opening found on Workable/Greenhouse/Lever for "
            f"{company!r} / {title!r}."
        ),
    )


def maybe_enrich_job(job: JobDescription) -> tuple[JobDescription, str]:
    """Prefer company ATS description when available; otherwise return original."""
    result = enrich_from_company_site(
        title=job.title or "",
        company=job.company or "",
        description=job.description,
        linkedin_url=str(job.url) if job.url else None,
    )
    if result.job:
        note = f"Enriched from company careers page ({result.job.url})"
        return result.job, note
    return job, result.message or "No company-site enrichment available"
