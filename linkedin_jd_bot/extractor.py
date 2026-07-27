from __future__ import annotations

import re
from typing import Optional

from bs4 import BeautifulSoup, NavigableString, Tag

from linkedin_jd_bot.cleaner import clean_text

DESCRIPTION_SELECTORS = [
    ".show-more-less-html__markup",
    ".description__text",
    ".jobs-description__content",
    ".jobs-box__html-content",
    "div.description__text--rich",
    "article.jobs-description__container",
    "div[class*='description']",
]

TITLE_SELECTORS = [
    "h1.top-card-layout__title",
    "h2.top-card-layout__title",
    "h1.topcard__title",
    "h2.topcard__title",
    ".top-card-layout__title",
    ".topcard__title",
    "h1.job-details-jobs-unified-top-card__job-title",
    "h1",
]

COMPANY_SELECTORS = [
    "a.topcard__org-name-link",
    "a.topcard__flavor--black-link",
    ".job-details-jobs-unified-top-card__company-name a",
    ".topcard__flavor a",
    "a[data-tracking-control-name*='company']",
]

LOCATION_SELECTORS = [
    ".topcard__flavor--bullet",
    ".job-details-jobs-unified-top-card__bullet",
    "span.topcard__flavor--bullet",
]

# LinkedIn guest HTML often injects tags mid-word (anti-scrape). Join those splits.
# Keep this case-sensitive: only join when both sides are lowercase letters.
MIDWORD_TAG_RE = re.compile(
    r"(?<=[a-z])(?:\s*</?(?:p|ul|ol|li|br|div|span|strong|em|b|i)[^>]*>\s*)+(?=[a-z])"
)

LABEL_PREFIX_RE = re.compile(
    r"^(seniority level|employment type|job function|industries)\s*[:|]?\s*",
    re.IGNORECASE,
)


def _plain(el: Optional[Tag]) -> Optional[str]:
    if el is None:
        return None
    value = clean_text(el.get_text(" ", strip=True))
    return value or None


def _first_match(soup: BeautifulSoup, selectors: list[str]) -> Optional[str]:
    for selector in selectors:
        el = soup.select_one(selector)
        text = _plain(el)
        if text:
            return text
    return None


def _deobfuscate_html(html: str) -> str:
    return MIDWORD_TAG_RE.sub("", html)


def _description_from_element(el: Tag) -> str:
    node = BeautifulSoup(str(el), "lxml")
    root = node.body or node

    for br in root.find_all("br"):
        br.replace_with(NavigableString("\n"))

    for li in root.find_all("li"):
        li.insert_before(NavigableString("\n- "))
        li.insert_after(NavigableString("\n"))

    for block in root.find_all(["p", "h1", "h2", "h3", "h4", "section", "div"]):
        # Only pad leaf-ish blocks to avoid huge spacing
        if block.find(["p", "li", "div", "section"]):
            continue
        block.insert_before(NavigableString("\n"))
        block.insert_after(NavigableString("\n"))

    text = root.get_text("", strip=False)
    # Collapse spaces but keep newlines introduced above
    lines = []
    for line in text.splitlines():
        collapsed = re.sub(r"[ \t]+", " ", line).strip()
        lines.append(collapsed)
    text = "\n".join(lines)
    return clean_text(text)


def _description_from_soup(soup: BeautifulSoup) -> Optional[str]:
    for selector in DESCRIPTION_SELECTORS:
        el = soup.select_one(selector)
        if el is None:
            continue
        text = _description_from_element(el)
        if text and len(text) > 80:
            return text

    candidates: list[str] = []
    for el in soup.find_all(["section", "article", "div"]):
        if not isinstance(el, Tag):
            continue
        text = _description_from_element(el)
        if text and len(text) > 200:
            candidates.append(text)
    if not candidates:
        return None
    return max(candidates, key=len)


def _criteria(soup: BeautifulSoup) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in soup.select(".description__job-criteria-item"):
        header = item.select_one(".description__job-criteria-subheader")
        value = item.select_one(".description__job-criteria-text")
        if header and value:
            key = header.get_text(" ", strip=True).strip().lower()
            out[key] = value.get_text(" ", strip=True).strip()
    return out


def _meta_bits(soup: BeautifulSoup) -> tuple[Optional[str], Optional[str]]:
    criteria = _criteria(soup)
    employment = criteria.get("employment type")
    seniority = criteria.get("seniority level")
    if employment and seniority:
        return employment, seniority

    for el in soup.find_all(["span", "li", "div"]):
        text = (el.get_text(" ", strip=True) or "").strip()
        if not text or len(text) > 80:
            continue
        normalized = LABEL_PREFIX_RE.sub("", text).strip()
        lower = text.lower()
        if employment is None and "employment type" in lower:
            employment = normalized
        if seniority is None and "seniority level" in lower:
            seniority = normalized
        if employment and seniority:
            break
    return employment, seniority


def parse_linkedin_html(html: str) -> dict[str, Optional[str]]:
    fixed = _deobfuscate_html(html)
    soup = BeautifulSoup(fixed, "lxml")
    title = _first_match(soup, TITLE_SELECTORS)
    company = _first_match(soup, COMPANY_SELECTORS)
    location = _first_match(soup, LOCATION_SELECTORS)
    description = _description_from_soup(soup)
    employment_type, seniority = _meta_bits(soup)

    if not title:
        page_title = _plain(soup.find("title"))
        if page_title and " | " in page_title:
            title = page_title.split(" | ", 1)[0].strip()
        elif page_title:
            title = page_title

    if employment_type:
        employment_type = LABEL_PREFIX_RE.sub("", employment_type).strip()
    if seniority:
        seniority = LABEL_PREFIX_RE.sub("", seniority).strip()

    return {
        "title": title,
        "company": company,
        "location": location,
        "employment_type": employment_type,
        "seniority": seniority,
        "description": description,
    }
