from __future__ import annotations

from linkedin_jd_bot.company_enrich import (
    company_slug_candidates,
    looks_like_recruiter,
    title_similarity,
    enrich_from_company_site,
)


def test_company_slug_candidates() -> None:
    assert "shiftmove" in company_slug_candidates("Shiftmove")
    slugs = company_slug_candidates(
        "SR2 | Socially Responsible Recruitment | Certified B Corporation™"
    )
    assert any("sr2" in s for s in slugs)


def test_title_similarity() -> None:
    assert title_similarity(
        "(Senior) Product Manager (all genders)",
        "(Senior) Product Manager (all genders)",
    ) == 1.0
    assert (
        title_similarity("Senior Product Manager", "(Senior) Product Manager (all genders)")
        >= 0.55
    )


def test_recruiter_detection() -> None:
    assert looks_like_recruiter(
        "SR2 | Socially Responsible Recruitment | Certified B Corporation™"
    )
    assert not looks_like_recruiter("Shiftmove")


def test_enrich_shiftmove_live() -> None:
    result = enrich_from_company_site(
        title="(Senior) Product Manager (all genders)",
        company="Shiftmove",
        linkedin_url="https://www.linkedin.com/jobs/view/4435971172",
    )
    assert result.job is not None
    assert result.job.source.value == "company"
    assert "fleet" in result.job.description.lower()
    assert "workable" in str(result.job.url).lower()


def test_enrich_skips_recruiter() -> None:
    result = enrich_from_company_site(
        title="Operations Manager",
        company="SR2 | Socially Responsible Recruitment | Certified B Corporation™",
        description="SR2 is partnering with an exciting clean energy business",
    )
    assert result.job is None
    assert "recruiter" in result.message.lower()
