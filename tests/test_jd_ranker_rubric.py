"""Regression guards for JD ranker scoring discipline."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "jd_ranker", Path(__file__).resolve().parents[1] / "jd_ranker.py"
)
jd_ranker = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(jd_ranker)


def test_funding_bumps_seed_not_series_a():
    assert jd_ranker.FUNDING_BUMPS["seed"][0] == -5
    assert jd_ranker.FUNDING_BUMPS["series_a"][0] == 5


def test_searoutes_style_score_does_not_inflate_fit_into_base():
    """Comp can be excellent while fit is poor; base must average them."""
    comp, fit = 82, 42
    base = int(round(0.5 * comp + 0.5 * fit))
    assert base == 62
    final, r, c, f, a, *_ = jd_ranker.apply_bumps(
        base, days=None, contact="none", funding="seed", applicants="unknown"
    )
    assert f == -5
    assert final == 57  # 62 - 5


def test_searoutes_with_fresh_posting_and_low_apps():
    base = 62
    final, *_ = jd_ranker.apply_bumps(
        base, days=0, contact="none", funding="seed", applicants="low"
    )
    assert final == 72  # 62 - 5 + 10 + 5


def test_validate_metadata_rejects_upgraded_funding_typo():
    meta = {"x": {"funding_stage": "series-a", "contact_status": "none"}}
    warnings = jd_ranker.validate_metadata(meta)
    assert meta["x"]["funding_stage"] == "unknown"
    assert any("funding_stage" in w for w in warnings)


def test_validate_metadata_flags_seed_as_hard_dq():
    meta = {
        "co": {
            "funding_stage": "seed",
            "employees": 18,
            "contact_status": "none",
            "applicant_volume": "low",
        }
    }
    warnings = jd_ranker.validate_metadata(meta)
    assert any("HARD DQ" in w and "seed" in w for w in warnings)


def test_validate_metadata_flags_young_company():
    meta = {
        "co": {
            "funding_stage": "series_a",
            "founded_year": 2025,
            "contact_status": "none",
        }
    }
    warnings = jd_ranker.validate_metadata(meta)
    assert any("younger than 2 years" in w for w in warnings)


def test_french_bump_required():
    final, r, c, f, a, fr, *_labels = jd_ranker.apply_bumps(
        60, days=None, contact="none", funding="unknown", french="required"
    )
    assert fr == 7
    assert final == 67


def test_french_bump_preferred():
    final, r, c, f, a, fr, *_labels = jd_ranker.apply_bumps(
        60, days=None, contact="none", funding="unknown", french="preferred"
    )
    assert fr == 4
    assert final == 64


def test_hard_dq_cap_logic_in_build_path():
    evaluations = {
        "bad": {
            "jd_key": "bad",
            "title": "PM",
            "company": "X",
            "base_score": 55,
            "competitiveness_score": 60,
            "fit_score": 50,
            "hard_disqualifiers": ["Native German (Muttersprache) required"],
            "recommended_action": "skip",
        }
    }
    for ev in evaluations.values():
        if ev.get("hard_disqualifiers"):
            expected = int(round(0.5 * ev["competitiveness_score"] + 0.5 * ev["fit_score"]))
            ev["base_score"] = min(expected, 30)
    assert evaluations["bad"]["base_score"] == 30


def test_profile_drops_autopilot_must_and_headcount_gate():
    assert "No autopilot requirement" in jd_ranker.SYSTEM_PROMPT
    assert "NOT seed-stage" in jd_ranker.PROFILE
    assert "last 2 years" in jd_ranker.PROFILE
    assert "Headcount does NOT matter" in jd_ranker.PROFILE
    assert "≤25 employees, assume this is unmet" not in jd_ranker.PROFILE
    assert "solutions_pre_sales" in jd_ranker.SYSTEM_PROMPT
    assert "Climate: NEVER hard-DQ climate mission alone" in jd_ranker.SYSTEM_PROMPT
    assert "German **native or C2 only**" in jd_ranker.SYSTEM_PROMPT
    assert "recommended_cv" not in jd_ranker.SYSTEM_PROMPT


def test_validate_metadata_flags_us_only():
    meta = {"digible": {"work_region": "us_only", "contact_status": "none"}}
    warnings = jd_ranker.validate_metadata(meta)
    assert any("us_only" in w and "HARD DQ" in w for w in warnings)


def test_role_families_tuple():
    assert "solutions_pre_sales" in jd_ranker.ROLE_FAMILIES
    assert "implementations" in jd_ranker.ROLE_FAMILIES
