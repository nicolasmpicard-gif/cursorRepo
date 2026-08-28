# JD Ranker rubric — scoring discipline

Use `jd_ranker.py` as the source of truth.

## Formula
`base = 0.5 * competitiveness + 0.5 * fit`  
`final = clamp(0, 100, base + recency + contact + funding + applicants)`

## Hard DQs (cap base at 30, skip)
- German B2+ / C1+ required
- Seed or pre-seed stage
- Company founded within the last 2 years
- US-only or UK-only hire (no EU eligibility) — set `work_region` in metadata

**Not hard DQs:** climate mission, small headcount, missing product peer (Fit cut only).

## Role lanes (competitiveness / interview signal)
Score `role_family` and `interview_signal` on every JD:

| Signal | Role families | Comp adjustment |
|--------|---------------|-----------------|
| **Strong** | Solutions / pre-sales / engagement / AI Solution Strategist; Implementations / onboarding | +8–12 / +5–8 |
| **Moderate** | PM at mature B2B SaaS; technical CS/onboarding | +3–6 |
| **Weak** | Account Manager, PMO/program, org consulting, sales ops | −5–12 |

**CV mapping:** `solutions_cv` (CV1) · `implementations_cv` (CV2) · `pm_cv`

## Climate nuance (important)
- **Do not** skip all climate roles.
- **Do** hard-DQ climate **startups** that fail maturity (seed, &lt;2 years) — interview activity without offers.
- **Prioritize** climate at **enterprise B2B SaaS** in solutions/implementations lanes (Pulsora pattern).
- Climate strategy consulting / mission-only CSM at young cos → `apply_if_time`, Comp −5–10.

## Fit (unchanged core)
- Product supervisor or peer = strong preference for PM roles (−10–20 if missing)
- Workplace style: low structure + low autonomy = −20–25
- No autopilot requirement; no headcount penalty

## Metadata
```json
{
  "pulsora_sc": {
    "days_since_posted": 5,
    "contact_status": "interview",
    "funding_stage": "series_a",
    "founded_year": 2019,
    "work_region": "eu",
    "applicant_volume": "low",
    "prior_interview": true
  }
}
```

`work_region`: `eu` | `global` | `us_only` | `uk_only` | `unknown`

## Funding bumps
| Stage | Bump |
|---|---:|
| pre_seed | −10 (also hard DQ) |
| seed | −5 (also hard DQ) |
| series_a | +5 |
| series_b_plus | +8 |
| profitable | +8 |
| unknown | 0 |
