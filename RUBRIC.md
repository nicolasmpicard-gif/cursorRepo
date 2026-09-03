# JD Ranker rubric — scoring discipline

Use `jd_ranker.py` as the source of truth.

## Formula
`base = 0.5 * competitiveness + 0.5 * fit`  
`final = clamp(0, 100, base + recency + contact + funding + applicants + french + lane + pm_domain + language_pen)`

## Hard DQs (cap base at 30, skip)

### German (only none / plus / B2 max pass)
| `german_requirement` | Verdict |
|---|---|
| none / unknown / plus / b2 | OK — passes language gate |
| **proficiency** | **HARD DQ** |
| **business_professional** | **HARD DQ** (professional/business working proficiency) |
| **fluent** | **HARD DQ** |
| **c1 / c2 / native** | **HARD DQ** |

### Domain expertise (required background Nic does not have)
Set `required_domain` and `domain_fit`. **Hard DQ** when `domain_fit=mismatch` OR `required_domain` is:

| `required_domain` | Why DQ |
|---|---|
| `fintech_payments` | Payments/fraud/acquiring (ACI-shaped) |
| `financial_services` | Deep finance/banking domain |
| `electronics_semiconductor` | Electronics/MOM-MES (Siemens-shaped) |
| `manufacturing_engineering` | Plant/manufacturing engineering depth |
| `machining_hardware` | CNC/machining/industrial hardware |
| `capital_markets` | IB/asset management product |
| `oil_gas` | Oil & gas / heavy industrial |
| `defense` | Defense/aerospace regulated |
| `medical_devices_deep` | Deep med-device/QMS specialist |
| `automotive_oem` | Automotive OEM engineering depth |

**Nic domain strengths (match/adjacent OK):** `general_b2b_saas`, `solutions_impl`, `supply_chain_esg`, `climate_compliance`, `data_ai_internal`, `product_management`, `hr_enterprise_saas`, `logistics_tech`

### Other hard DQs
- Seed or pre-seed stage
- Company founded within the last 2 years
- US-only or UK-only hire (no EU eligibility)

## Language gate (lane / pm_domain bumps)
Only roles with `german_requirement` in **none / plus / b2 / unknown** get lane (+6/+6/+4) and pm_domain (+4/+3) bumps.

## Lane precedence (when language gate passes)

| `role_family` | Lane bump |
|---|---:|
| `solutions_pre_sales` | +6 |
| `implementations` | +6 |
| `project_management` (TPM, delivery PM — not PMO) | +4 |
| `product_manager` | 0 |

## PM domain bumps (when language gate passes)

| `pm_domain` | Bump | Examples |
|---|---:|---|
| `data_ai_internal` | +4 | Internal BI/data platform PM |
| `data_ai_product` | +3 | External data/AI SaaS PM |
| `none` | 0 | General PM without data/AI focus |

## French bump
| Level | Bump |
|---|---:|
| required / fluent / mandatory | +7 |
| preferred / plus / advantage | +4 |
| none | 0 |

## Metadata
```json
{
  "kainos_sc": {
    "days_since_posted": 5,
    "contact_status": "none",
    "funding_stage": "profitable",
    "applicant_volume": "low",
    "german_requirement": "none",
    "required_domain": "solutions_impl",
    "domain_fit": "match",
    "role_family": "solutions_pre_sales"
  },
  "aci_sc": {
    "german_requirement": "none",
    "required_domain": "fintech_payments",
    "domain_fit": "mismatch"
  },
  "personio_ps": {
    "german_requirement": "proficiency",
    "required_domain": "hr_enterprise_saas",
    "domain_fit": "match"
  }
}
```

`german_requirement`: `none` | `plus` | `b2` | `proficiency` | `business_professional` | `fluent` | `c1` | `c2` | `native` | `unknown`  
`required_domain`: see `REQUIRED_DOMAINS` in `jd_ranker.py`  
`domain_fit`: `match` | `adjacent` | `mismatch` | `unknown`  
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
