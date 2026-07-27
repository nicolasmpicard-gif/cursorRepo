from __future__ import annotations

import re
from typing import Optional

# UI chrome / LinkedIn chrome that often leaks into pasted text
NOISE_PATTERNS = [
    re.compile(r"^Show more$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^Show less$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^Report this job$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^Apply$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^Save$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^Easy Apply$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^Set alert for similar jobs$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^People also viewed$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^Similar jobs$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^About the company$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^See more jobs like this$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^Sign in to.*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^Join now$", re.IGNORECASE | re.MULTILINE),
]

WHITESPACE_RE = re.compile(r"[ \t]+\n")
MULTI_BLANK_RE = re.compile(r"\n{3,}")
BULLET_RE = re.compile(r"^[ \t]*[•●▪◦‣]\s*", re.MULTILINE)


def clean_text(text: str) -> str:
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = cleaned.replace("\xa0", " ")
    cleaned = BULLET_RE.sub("- ", cleaned)
    for pattern in NOISE_PATTERNS:
        cleaned = pattern.sub("", cleaned)
    cleaned = WHITESPACE_RE.sub("\n", cleaned)
    cleaned = MULTI_BLANK_RE.sub("\n\n", cleaned)
    return cleaned.strip()


def first_nonempty_line(text: str) -> Optional[str]:
    for line in text.splitlines():
        candidate = line.strip()
        if candidate:
            return candidate
    return None


def guess_title_company_from_paste(text: str) -> tuple[Optional[str], Optional[str]]:
    """Heuristic for pasted LinkedIn JDs where the first lines are title/company."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None, None
    title = lines[0] if len(lines[0]) < 160 else None
    company = None
    if len(lines) > 1 and len(lines[1]) < 120:
        # LinkedIn paste often: Title / Company · Location
        second = lines[1]
        if "·" in second:
            company = second.split("·", 1)[0].strip() or None
        elif not second.lower().startswith(("about", "http", "http")):
            company = second
    return title, company
