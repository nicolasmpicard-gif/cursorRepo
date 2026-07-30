# JD Ranker rubric — scoring discipline

Use `jd_ranker.py` as the source of truth. This note exists so agents don’t repeat the Searoutes inflation bug.

## Formula
`base = 0.5 * competitiveness + 0.5 * fit`  
`final = clamp(0, 100, base + recency + contact + funding + applicants)`

## Non-negotiables
1. **Verify `funding_stage`** from Crunchbase/Tracxn/press. Never infer Series A+ from “climate startup” or mission quality. If unsure → `unknown` (0).
2. **Comp ≠ Fit.** A role can be Comp 80+ and Fit ~40. Do not let skill match inflate fit.
3. **Existing product team** = PM peers / Head-Director of Product / multi-person product org.  
   `VP Eng + Product Engineer + founders` at ≤25 people does **not** count.
4. **Stale seed / tiny headcount is a fit penalty** (−15 to −25): seed with no follow-on for 3+ years and/or ~15–25 employees without clear product leadership — even if mission is perfect.
5. **Autopilot** (−20 to −25 fit if unlikely): founding, speedboat, perpetual growth/strategist ownership at a tiny company, blank-page functions.
6. **Location is score-neutral** (DE/GR/FR/US/remote). Language gates (e.g. German C1) still apply.
7. **Hard DQs** (German C1+, no product team) → **cap `base_score` at 30**.

## Funding bumps
| Stage | Bump |
|---|---:|
| pre_seed | −10 |
| seed | −5 |
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
    "funding_stage": "seed",
    "applicant_volume": "low",
    "employees": 18,
    "last_raise_date": "2021-11-23"
  }
}
```

## Regression example (Searoutes)
- Mission/comp exceptional (climate + supply chain + French) → Comp ~82  
- Seed Nov 2021, ~18 employees, weak product-team peers → Fit ~42  
- Base ~62, funding −5 → final ~57 (or ~72 if fresh posting + low applicants)  
- **Not** a 90+ role.
