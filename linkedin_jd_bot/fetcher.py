from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import httpx

from linkedin_jd_bot.urls import canonicalize_job_url, is_linkedin_job_url

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
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
        "join linkedin",
        "sign in to view",
        "challenge-form",
        "captcha",
        "security verification",
        "session redirect",
        "page not found",
        "we can’t seem to find the page",
        "we can't seem to find the page",
        "this job is no longer available",
    ]
    return any(token in lower for token in blockers)


def fetch_with_httpx(url: str, timeout: float = 20.0) -> FetchResult:
    if not is_linkedin_job_url(url):
        raise ValueError("Not a LinkedIn job URL")
    canonical = canonicalize_job_url(url) or url
    with httpx.Client(headers=DEFAULT_HEADERS, follow_redirects=True, timeout=timeout) as client:
        response = client.get(canonical)
    html = response.text
    blocked = _looks_blocked(html, response.status_code)
    message = ""
    if blocked:
        if response.status_code == 404 or "page not found" in html.lower():
            message = "job page not found or removed"
        else:
            message = "LinkedIn blocked or login-walled the request"
    return FetchResult(
        url=str(response.url),
        html=html,
        status_code=response.status_code,
        blocked=blocked,
        method="httpx",
        message=message,
    )


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

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context_kwargs = {}
        if storage_state:
            context_kwargs["storage_state"] = storage_state
        context = browser.new_context(**context_kwargs)
        page = context.new_page()
        response = page.goto(canonical, wait_until="domcontentloaded", timeout=timeout_ms)
        # Give LinkedIn a moment to hydrate the JD panel when logged in
        page.wait_for_timeout(1500)
        html = page.content()
        final_url = page.url
        status = response.status if response else 0
        browser.close()

    blocked = _looks_blocked(html, status)
    return FetchResult(
        url=final_url,
        html=html,
        status_code=status,
        blocked=blocked,
        method="playwright",
        message="Page looks login-walled; paste the JD or provide --storage-state"
        if blocked
        else "",
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
