from __future__ import annotations

import re
from typing import Optional

from bs4 import BeautifulSoup, Tag

from linkedin_jd_bot.cleaner import clean_text

DESCRIPTION_SELECTORS = [
    ".description__text",
    ".show-more-less-html__markup",
    ".jobs-description__content",
    ".jobs-box__html-content",
    "div.description__text--rich",
    "article.jobs-description__container",
    "div[class*='description']",
]

TITLE_SELECTORS = [
    "h1.top-card-layout__title",
    "h1.topcard__title",
    "h1.job-details-jobs-unified-top-card__job-title",
    "h1",
]

COMPANY_SELECTORS = [
    "a.topcard__org-name-link",
    "a.top-card-layout__card a",
    ".job-details-jobs-unified-top-card__company-name a",
    ".topcard__flavor a",
    "a[data-tracking-control-name*='company']",
]

LOCATION_SELECTORS = [
    ".topcard__flavor--bullet",
    ".job-details-jobs-unified-top-card__bullet",
    "span.topcard__flavor--bullet",
]

META_ITEM_RE = re.compile(
    r"(full[- ]time|part[- ]time|contract|temporary|internship|entry level|"
    r"associate|mid-senior|director|executive|remote|hybrid|on-site)",
    re.IGNORECASE,
)


def _text(el: Optional[Tag]) -> Optional[str]:
    if el is None:
        return None
    value = clean_text(el.get_text("\n", strip=True))
    return value or None


def _first_match(soup: BeautifulSoup, selectors: list[str]) -> Optional[str]:
    for selector in selectors:
        el = soup.select_one(selector)
        text = _text(el)
        if text:
            return text
    return None


def _description_from_soup(soup: BeautifulSoup) -> Optional[str]:
    for selector in DESCRIPTION_SELECTORS:
        el = soup.select_one(selector)
        text = _text(el)
        if text and len(text) > 80:
            return text

    # Fallback: largest text block that looks like a JD
    candidates: list[str] = []
    for el in soup.find_all(["section", "article", "div"]):
        if not isinstance(el, Tag):
            continue
        text = _text(el)
        if text and len(text) > 200:
            candidates.append(text)
    if not candidates:
        return None
    return max(candidates, key=len)


def _meta_bits(soup: BeautifulSoup) -> tuple[Optional[str], Optional[str]]:
    employment = None
    seniority = None
    for el in soup.find_all(["span", "li", "div"]):
        text = (el.get_text(" ", strip=True) or "").strip()
        if not text or len(text) > 60:
            continue
        if not META_ITEM_RE.search(text):
            continue
        lower = text.lower()
        if any(k in lower for k in ("full", "part", "contract", "temporary", "intern")):
            employment = employment or text
        if any(
            k in lower
            for k in ("entry", "associate", "mid", "senior", "director", "executive")
        ):
            seniority = seniority or text
    return employment, seniority


def parse_linkedin_html(html: str) -> dict[str, Optional[str]]:
    soup = BeautifulSoup(html, "lxml")
    title = _first_match(soup, TITLE_SELECTORS)
    company = _first_match(soup, COMPANY_SELECTORS)
    location = _first_match(soup, LOCATION_SELECTORS)
    description = _description_from_soup(soup)
    employment_type, seniority = _meta_bits(soup)

    # LinkedIn public pages sometimes put title in <title>
    if not title:
        page_title = _text(soup.find("title"))
        if page_title and " | " in page_title:
            title = page_title.split(" | ", 1)[0].strip()
        elif page_title:
            title = page_title

    return {
        "title": title,
        "company": company,
        "location": location,
        "employment_type": employment_type,
        "seniority": seniority,
        "description": description,
    }
