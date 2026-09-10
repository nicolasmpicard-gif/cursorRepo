# JD Ranker rubric — scoring discipline

Use `jd_ranker.py` as the source of truth.

## Formula
`base = 0.7 * competitiveness + 0.3 * fit`  
`final = clamp(0, 100, base + recency + contact + funding + applicants + french + lane + pm_domain + language_pen)`

## Hard DQs (cap base at 30, skip)

### German (only C2 / native)
| `german_requirement` | Verdict |
|---|---|
| none / unknown / plus / b2 / proficiency / business_professional / fluent / c1 | OK — passes language gate |
| **c2 / native** | **HARD DQ** |

### Germany office (Berlin-based Nic)
| `germany_work_mode` | Verdict |
|---|---|
| `berlin` | OK (hybrid or office) |
| `remote` | OK (fully remote / remote-in-Germany) |
| `other_de_hybrid` | OK — other DE city **and** JD states hybrid / &lt;5 days in office |
| **`other_de_onsite`** | **HARD DQ** — Hamburg/Munich/etc. with **no** hybrid/remote stated |
| `outside_de` / `unknown` | OK (no Germany-office DQ) |

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
| `agtech_farmer_product` | Farmer/grower-facing product design (Klim-shaped); enterprise SC/ESG ≠ on-farm UX |

**Nic domain strengths (match/adjacent OK):** `general_b2b_saas`, `solutions_impl`, `supply_chain_esg`, `climate_compliance`, `data_ai_internal`, `product_management`, `hr_enterprise_saas`, `logistics_tech`

**Interview Comp notes:** Solutions/impl lane Comp stays high after NinjaOne (craft miss, not lane miss). Builder/climate founding PM Comp stays low (CEEZER). Salary rejects (SumSub) do not lower SC Comp.

### Other hard DQs
- Seed or pre-seed stage
- Company founded within the last 2 years
- US-only or UK-only hire (no EU eligibility)

## Language gate (lane / pm_domain bumps)
Passes unless `german_requirement` is **c2** or **native**.  
Proficiency / fluent / C1 still get lane and PM-domain bumps.

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
    "germany_work_mode": "remote",
    "required_domain": "solutions_impl",
    "domain_fit": "match",
    "role_family": "solutions_pre_sales"
  },
  "eqs_c2": {
    "german_requirement": "c2",
    "germany_work_mode": "remote",
    "required_domain": "climate_compliance",
    "domain_fit": "match"
  },
  "beiersdorf_hamburg": {
    "germany_work_mode": "other_de_onsite",
    "german_requirement": "none"
  }
}
```

`german_requirement`: `none` | `plus` | `b2` | `proficiency` | `business_professional` | `fluent` | `c1` | `c2` | `native` | `unknown`  
`germany_work_mode`: `berlin` | `remote` | `other_de_hybrid` | `other_de_onsite` | `outside_de` | `unknown`  
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
