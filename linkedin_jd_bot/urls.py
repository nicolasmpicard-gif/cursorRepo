from __future__ import annotations

import re
from typing import Optional
from urllib.parse import urlparse

LINKEDIN_JOB_HOSTS = {"linkedin.com", "www.linkedin.com"}
JOB_PATH_RE = re.compile(r"/jobs/(?:view/)?(?:[\w%-]+-)?(\d+)", re.IGNORECASE)
CANONICAL_JOB_URL = "https://www.linkedin.com/jobs/view/{job_id}"


def is_linkedin_job_url(url: str) -> bool:
    try:
        parsed = urlparse(url.strip())
    except ValueError:
        return False
    host = (parsed.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    if host not in {"linkedin.com"} and not host.endswith(".linkedin.com"):
        return False
    return bool(JOB_PATH_RE.search(parsed.path or ""))


def extract_job_id(url: str) -> Optional[str]:
    try:
        parsed = urlparse(url.strip())
    except ValueError:
        return None
    match = JOB_PATH_RE.search(parsed.path or "")
    return match.group(1) if match else None


def canonicalize_job_url(url: str) -> Optional[str]:
    job_id = extract_job_id(url)
    if not job_id:
        return None
    return CANONICAL_JOB_URL.format(job_id=job_id)


def looks_like_url(value: str) -> bool:
    text = value.strip()
    if not text or "\n" in text:
        return False
    return text.startswith(("http://", "https://"))
