"""LinkedIn JD bot: paste-first extraction with optional browser fetch."""

from linkedin_jd_bot.models import JobDescription
from linkedin_jd_bot.pipeline import extract_from_html, extract_from_text, extract_job

__all__ = [
    "JobDescription",
    "extract_from_html",
    "extract_from_text",
    "extract_job",
]

__version__ = "0.1.0"
