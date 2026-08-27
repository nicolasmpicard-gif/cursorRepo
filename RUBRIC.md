# JD Ranker rubric — scoring discipline

Use `jd_ranker.py` as the source of truth.

## Formula
`base = 0.5 * competitiveness + 0.5 * fit`  
`final = clamp(0, 100, base + recency + contact + funding + applicants)`

## Non-negotiables
1. **Verify `funding_stage`** from Crunchbase/Tracxn/press. Never infer Series A+ from “climate startup” or mission quality. If unsure → `unknown` (0).
2. **Comp ≠ Fit.** A role can be Comp 80+ and Fit ~40. Do not let skill match inflate fit.
3. **Hard maturity DQs:** seed / pre-seed **or** company founded within the last 2 years → leave out / cap base at 30. **Headcount is fine** — small teams OK past those gates.
4. **Product supervisor or peer** (Head/Director/VP Product, CPO, or another PM) is a **strong Fit preference**, not a hard DQ alone. Eng-only + founders does not count. Solo / first-PM → Fit −10 to −20.
5. **Autopilot / steady-state in 6–12 months is NOT required** and must not drive Fit.
6. **Location is score-neutral** (DE/GR/FR/US/remote). Language gates (e.g. German B2+) still apply.
7. **Hard DQs** (German B2+, seed/pre-seed, founded <2 years) → **cap `base_score` at 30**.

## Funding bumps
| Stage | Bump |
|---|---:|
| pre_seed | −10 |
| seed | −5 (also a hard DQ under current preference) |
| series_a | +5 |
| series_b_plus | +8 |
| profitable | +8 |
| unknown | 0 |

## Metadata fields to prefer
```json
{
  "example": {
    "days_since_posted": 3,
    "contact_status": "none",
    "funding_stage": "series_a",
    "applicant_volume": "low",
    "employees": 18,
    "founded_year": 2021,
    "last_raise_date": "2024-06-01"
  }
}
```
