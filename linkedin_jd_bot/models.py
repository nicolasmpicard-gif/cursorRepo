from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class SourceKind(str, Enum):
    PASTE = "paste"
    HTML = "html"
    FETCH = "fetch"


class JobDescription(BaseModel):
    """Normalized LinkedIn (or pasted) job description."""

    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    seniority: Optional[str] = None
    description: str = Field(..., min_length=1)
    url: Optional[HttpUrl] = None
    source: SourceKind = SourceKind.PASTE
    raw_length: int = 0

    def summary_lines(self) -> list[str]:
        lines: list[str] = []
        if self.title:
            lines.append(f"Title: {self.title}")
        if self.company:
            lines.append(f"Company: {self.company}")
        if self.location:
            lines.append(f"Location: {self.location}")
        if self.employment_type:
            lines.append(f"Type: {self.employment_type}")
        if self.seniority:
            lines.append(f"Seniority: {self.seniority}")
        if self.url:
            lines.append(f"URL: {self.url}")
        lines.append(f"Source: {self.source.value}")
        lines.append("")
        lines.append(self.description)
        return lines
