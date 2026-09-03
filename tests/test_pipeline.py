from __future__ import annotations

from pathlib import Path

import pytest

from linkedin_jd_bot.fetcher import _looks_blocked
from linkedin_jd_bot.pipeline import ExtractionError, extract_from_html, extract_from_text, extract_job
from linkedin_jd_bot.urls import canonicalize_job_url, extract_job_id, is_linkedin_job_url

FIXTURE = Path(__file__).parent / "fixtures" / "sample_job.html"


def test_linkedin_job_url_parsing() -> None:
    url = "https://www.linkedin.com/jobs/view/1234567890/?refId=abc"
    assert is_linkedin_job_url(url)
    assert extract_job_id(url) == "1234567890"
    assert canonicalize_job_url(url) == "https://www.linkedin.com/jobs/view/1234567890"


def test_reject_non_job_url() -> None:
    assert not is_linkedin_job_url("https://www.linkedin.com/in/someone")


def test_looks_blocked_detects_404_page() -> None:
    html = "<html><body>Page not found. Uh oh, we can’t seem to find the page you’re looking for.</body></html>"
    assert _looks_blocked(html, 200)
    assert _looks_blocked("<html></html>", 404)

def test_extract_from_html_fixture() -> None:
    html = FIXTURE.read_text(encoding="utf-8")
    job = extract_from_html(html, url="https://www.linkedin.com/jobs/view/1234567890")
    assert job.title == "Senior Backend Engineer"
    assert job.company == "Acme Corp"
    assert job.location == "San Francisco Bay Area"
    assert "Senior Backend Engineer to build APIs" in job.description
    assert "5+ years backend experience" in job.description
    assert job.url is not None
    assert str(job.url).endswith("/1234567890")


def test_extract_from_paste() -> None:
    text = """
    Staff Platform Engineer
    Northwind · Remote · Full-time

    About the job
    Build internal developer platforms.

    Requirements
    - Kubernetes
    - Go or Python
    """
    job = extract_from_text(text)
    assert job.title == "Staff Platform Engineer"
    assert job.company == "Northwind"
    assert "Kubernetes" in job.description


def test_extract_job_rejects_short_paste() -> None:
    with pytest.raises(ExtractionError):
        extract_job("too short")


def test_extract_job_html_detection() -> None:
    html = FIXTURE.read_text(encoding="utf-8")
    job = extract_job(html)
    assert job.title == "Senior Backend Engineer"
    assert "Postgres" in job.description


def test_extract_guest_ops_manager_html() -> None:
    html = (Path(__file__).parent / "fixtures" / "guest_ops_manager.html").read_text(
        encoding="utf-8"
    )
    job = extract_from_html(html, url="https://www.linkedin.com/jobs/view/4434551058")
    assert job.title == "Operations Manager"
    assert "SR2" in (job.company or "")
    assert job.location == "Berlin, Germany"
    assert "Operations Manager" in job.description
    assert "renewable energy" in job.description.lower()
    # Mid-word anti-scrape tags should be repaired
    assert "doing:" in job.description.lower() or "What you'll be doing" in job.description


def test_extract_guest_product_manager_html() -> None:
    html = (
        Path(__file__).parent / "fixtures" / "guest_product_manager.html"
    ).read_text(encoding="utf-8")
    job = extract_from_html(html, url="https://www.linkedin.com/jobs/view/4435971172")
    assert "Product Manager" in (job.title or "")
    assert job.company == "Shiftmove"
    assert "fleet" in job.description.lower()
    assert job.employment_type == "Full-time"
