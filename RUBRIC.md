# JD Ranker rubric — scoring discipline

Use `jd_ranker.py` as the source of truth.

## Formula
`base = 0.5 * competitiveness + 0.5 * fit`  
`final = clamp(0, 100, base + recency + contact + funding + applicants + french + lane + pm_domain + language_pen)`

## Hard DQs (cap base at 30, skip)
- **Native German** or **C2** required (Muttersprache / native-level)
- Seed or pre-seed stage
- Company founded within the last 2 years
- US-only or UK-only hire (no EU eligibility) — set `work_region` in metadata

**Not hard DQs:** German C1 / B2 / "fluent" / professional working proficiency (language_pen + Fit penalty instead); climate mission; small headcount; missing product peer (Fit cut only).

## Language gate (Sep 2026)
English/French native OK. German requirement must be **none, plus, or B2 max** to pass.

| `german_requirement` | Gate | Lane bump | language_pen |
|---|---|---|---|
| none / unknown | pass | eligible | 0 |
| plus | pass | eligible | 0 |
| b2 | pass | eligible | 0 |
| fluent | **fail** | none | −8 |
| c1 | **fail** | none | −12 |
| c2 / native | **hard DQ** | — | −15 |

## Lane precedence (when language gate passes)
Solutions / implementations / delivery PM outrank generic PM on the chart — but **do not discount PM entirely**.

| `role_family` | Lane bump |
|---|---:|
| `solutions_pre_sales` | +6 |
| `implementations` | +6 |
| `project_management` (TPM, delivery PM — not PMO) | +4 |
| `product_manager` | 0 |

## PM domain bumps (when language gate passes)
Nic strengths: **internal tooling, data platform / BI-as-product, AI product PM**.

| `pm_domain` | Bump | Examples |
|---|---:|---|
| `data_ai_internal` | +4 | Holidu Data & AI PM, internal analytics/BI platform |
| `data_ai_product` | +3 | External data/AI SaaS PM |
| `none` | 0 | General PM without data/AI focus |

## French bump
| Level | Bump |
|---|---:|
| required / fluent / mandatory | +7 |
| preferred / plus / advantage | +4 |
| none | 0 |

Set `french_language` in metadata or let the model infer from JD text.

## Role lanes (competitiveness / interview signal)
Score `role_family` and `interview_signal` on every JD:

| Signal | Role families | Comp adjustment |
|--------|---------------|-----------------|
| **Strong** | Solutions / pre-sales / engagement / AI Solution Strategist / CSE; Implementations / onboarding | +8–12 / +5–8 |
| **Moderate** | Delivery TPM; PM at mature B2B SaaS; technical CS/onboarding | +3–6 |
| **Weak** | Account Manager, PMO/program, org consulting, sales ops, venture-builder biz dev, manufacturing domain | −5–12 |

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
    "french_language": "required",
    "german_requirement": "none",
    "pm_domain": "data_ai_internal",
    "role_family": "product_manager",
    "prior_interview": true
  }
}
```

`work_region`: `eu` | `global` | `us_only` | `uk_only` | `unknown`  
`french_language`: `required` | `preferred` | `none` | `unknown`  
`german_requirement`: `none` | `plus` | `b2` | `fluent` | `c1` | `c2` | `native` | `unknown`  
`pm_domain`: `none` | `data_ai_internal` | `data_ai_product` | `unknown`  
`role_family`: see `ROLE_FAMILIES` in `jd_ranker.py`

## Funding bumps
| Stage | Bump |
|---|---:|
| pre_seed | −10 (also hard DQ) |
| seed | −5 (also hard DQ) |
| series_a | +5 |
| series_b_plus | +8 |
| profitable | +8 |
| unknown | 0 |
