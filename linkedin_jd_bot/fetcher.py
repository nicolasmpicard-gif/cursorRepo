from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import httpx

from linkedin_jd_bot.urls import canonicalize_job_url, guest_job_url, is_linkedin_job_url

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


@dataclass
class FetchResult:
    url: str
    html: str
    status_code: int
    blocked: bool
    method: str
    message: str = ""


def _looks_blocked(html: str, status_code: int) -> bool:
    if status_code in {401, 403, 404, 999}:
        return True
    lower = html.lower()
    blockers = [
        "authwall",
        "challenge-form",
        "captcha",
        "security verification",
        "session redirect",
        "page not found",
        "we can’t seem to find the page",
        "we can't seem to find the page",
        "this job is no longer available",
    ]
    # Guest payloads can mention "sign in" in chrome without being blocked.
    if "show-more-less-html" in lower or "description__text" in lower:
        if "authwall" not in lower and status_code == 200:
            return False
    if "sign in to view" in lower or "join linkedin" in lower:
        return True
    return any(token in lower for token in blockers)


def _has_job_content(html: str) -> bool:
    lower = html.lower()
    return any(
        token in lower
        for token in (
            "show-more-less-html",
            "description__text",
            "top-card-layout__title",
            "topcard__title",
        )
    )


def fetch_with_httpx(url: str, timeout: float = 20.0) -> FetchResult:
    if not is_linkedin_job_url(url):
        raise ValueError("Not a LinkedIn job URL")

    canonical = canonicalize_job_url(url) or url
    guest = guest_job_url(url)
    candidates: list[tuple[str, str]] = []
    if guest:
        candidates.append(("httpx-guest", guest))
    candidates.append(("httpx", canonical))

    last: Optional[FetchResult] = None
    with httpx.Client(headers=DEFAULT_HEADERS, follow_redirects=True, timeout=timeout) as client:
        for method, candidate in candidates:
            response = client.get(candidate)
            html = response.text
            blocked = _looks_blocked(html, response.status_code)
            usable = (not blocked) and _has_job_content(html)
            message = ""
            if blocked:
                if response.status_code == 404 or "page not found" in html.lower():
                    message = "job page not found or removed"
                else:
                    message = "LinkedIn blocked or login-walled the request"
            result = FetchResult(
                url=canonical,
                html=html,
                status_code=response.status_code,
                blocked=not usable,
                method=method,
                message=message if not usable else "",
            )
            if usable:
                return result
            last = result

    assert last is not None
    return last


def fetch_with_playwright(
    url: str,
    *,
    storage_state: Optional[str] = None,
    headless: bool = True,
    timeout_ms: int = 30000,
) -> FetchResult:
    """Optional authenticated browser fetch. Requires `pip install '.[browser]'`."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:  # pragma: no cover - optional dep
        raise RuntimeError(
            "Playwright is not installed. Run: pip install '.[browser]' "
            "&& playwright install chromium"
        ) from exc

    if not is_linkedin_job_url(url):
        raise ValueError("Not a LinkedIn job URL")
    canonical = canonicalize_job_url(url) or url
    # Prefer guest endpoint even in browser mode; fall back to canonical.
    guest = guest_job_url(url)
    start_url = guest or canonical

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context_kwargs = {}
        if storage_state:
            context_kwargs["storage_state"] = storage_state
        context = browser.new_context(**context_kwargs)
        page = context.new_page()
        response = page.goto(start_url, wait_until="domcontentloaded", timeout=timeout_ms)
        page.wait_for_timeout(1500)
        html = page.content()
        status = response.status if response else 0
        if (not _has_job_content(html) or _looks_blocked(html, status)) and guest:
            response = page.goto(canonical, wait_until="domcontentloaded", timeout=timeout_ms)
            page.wait_for_timeout(1500)
            html = page.content()
            status = response.status if response else 0
        browser.close()

    usable = (not _looks_blocked(html, status)) and _has_job_content(html)
    return FetchResult(
        url=canonical,
        html=html,
        status_code=status,
        blocked=not usable,
        method="playwright",
        message=(
            "Page looks login-walled; paste the JD or provide --storage-state"
            if not usable
            else ""
        ),
    )


def fetch_job_html(
    url: str,
    *,
    use_browser: bool = False,
    storage_state: Optional[str] = None,
    headless: bool = True,
) -> FetchResult:
    if use_browser:
        return fetch_with_playwright(
            url, storage_state=storage_state, headless=headless
        )
    return fetch_with_httpx(url)
