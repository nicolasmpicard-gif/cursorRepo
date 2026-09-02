#!/usr/bin/env python3
"""
JD Ranker - Evaluates job descriptions and ranks them for Nic.

USAGE
-----
1. Create a folder for your JDs (e.g. ~/jds/)
2. Add one .txt file per JD (filename = your short label, e.g. klim_pm.txt)
3. Optionally add metadata.json in the same folder:

   {
     "klim_pm": {
       "days_since_posted": 3,
       "contact_status": "interview",
       "funding_stage": "series_a",
       "applicant_volume": "medium",
       "employees": 45,
       "last_raise_date": "2024-06-01"
     }
   }

   contact_status values : "none" | "positive_contact" | "interview"
   funding_stage values  : "pre_seed" | "seed" | "series_a" | "series_b_plus" | "profitable" | "unknown"
   applicant_volume      : "low" | "medium" | "high" | "unknown"
   french_language       : "required" | "preferred" | "none" | "unknown"
                         — required = fluent/native/mandatory; preferred = plus/advantage/nice-to-have
   german_requirement    : "none" | "plus" | "b2" | "fluent" | "c1" | "c2" | "native" | "unknown"
                         — lane-precedence + chart eligibility: pass if none/plus/b2/unknown;
                           fluent/c1 penalized; c2/native hard DQ
   days_since_posted     : integer, or omit/null if unknown
   employees             : integer headcount if known (informational; not a Fit penalty)
   founded_year          : integer if known (HARD DQ if company age < 2 years)
   work_region           : "eu" | "global" | "us_only" | "uk_only" | "unknown"
                         — us_only/uk_only when JD restricts hire to that region (HARD DQ for Berlin-based Nic)
   role_family           : optional override — see ROLE_FAMILIES in jd_ranker.py
   prior_interview       : true if Nic had prior interview pipeline at this company
   last_raise_date       : ISO date string if known (informational)

4. Run:
   python3 jd_ranker.py ~/jds/

Output: ranked table + per-JD detail printed to stdout,
        and jd_ranking_results.md saved in the current directory.

SCORING FORMULA
---------------
base_score     = 0.5 * competitiveness_score + 0.5 * fit_score
  competitiveness_score : how likely Nic is to get the interview/offer
  fit_score              : preference fit (product peer/supervisor, pace/culture, stage/age
                           gates) + workplace-style sustainability (structure/autonomy/feedback)
recency_bump   : 0-10 pts  (0-7d → +10, 8-14d → +6, 15-30d → +3, 31-60d → +1, >60d/unknown → 0)
contact_bump   : 0-15 pts  (none → 0, positive_contact → +7, interview → +15)
funding_bump   : -10 to +8 pts
  pre_seed     → -10
  seed         → -5
  series_a     →  +5
  series_b_plus→  +8
  profitable   →  +8
  unknown      →   0
applicant_bump : -5 to +5 pts (low competition → +5, high (100+) → -5)
french_bump    : 0-7 pts (required/fluent → +7, preferred/plus → +4, none → 0)
lane_bump      : 0-6 pts when language gate passes (solutions/impl +6, delivery PM/TPM +4; PM gets 0)
language_pen   : 0 to -12 pts (fluent −8, c1 −12; c2/native = hard DQ)
final_score    = clamp(0, 100, base + recency + contact + funding + applicants + french + lane + language_pen)

CRITICAL SCORING DISCIPLINE (read before every evaluation)
---------------------------------------------------------
1. VERIFY funding_stage from real data (Crunchbase/Tracxn/press). Do NOT infer
   "series_a" from "climate startup", "VC-backed", or mission quality.
2. competitiveness_score and fit_score are INDEPENDENT. Exceptional skill match
   must NOT inflate fit. A role can be Comp 80+ and Fit 40.
3. Hard maturity DQs: seed/pre-seed OR company founded within the last 2 years.
   Headcount is NOT a DQ — small teams are fine past those gates.
4. Product supervisor OR peer is a strong Fit preference (not a hard DQ alone).
   Eng-only leadership + founders does not count as product peer/supervisor.
5. Location (country/city) must NOT raise or lower Fit/Comp scores — but
   work_region=us_only or uk_only when Nic cannot legally/ practically work there
   is a HARD DQ (metadata or JD text).
6. Role family interview signals (see PROFILE) adjust competitiveness_score only —
   mission match must not override weak role-family signal.
"""

import sys
import os
import json
from pathlib import Path
from datetime import date

# ──────────────────────────────────────────────────────────────
# PROFILE
# ──────────────────────────────────────────────────────────────

PROFILE = """
## Candidate Background

Nicolas Picard — French-American, based in Berlin (EU/US work auth).
~10 years across product, implementations, and solutions/pre-sales.

### Strongest proof points (use for competitiveness, not fit inflation):
- Oracle Utilities Pre-Sales: scoped/negotiated/closed $65M+ SaaS incl. $23M deal; RFI/RFP; best writer on team
- OpenSC Lead/Sr Implementation: Nespresso QBRs, renewals, onboarding 4× cost cut, $130K business case, trusted advisor
- Pulsora Pre-Sales Solutions Consultant — reached OFFER (ESG/compliance B2B SaaS)
- Scale AI Engagement Manager EU — 3rd round | LeanIX Sr CS Onboarding EMEA — 2nd round
- Trade Republic Process Automation & Product/Data Analyst — final round
- NinjaOne Solutions Engineer — 2nd round (same company: Account Manager did not advance)
- Applied: Deel Product Ops, Insider One Solutions Consultant DACH, Paradox (French)

### Key experience areas (in rough order of depth):
- Solutions consulting & pre-sales (Oracle, OpenSC pitching, Pulsora offer-path)
- Software implementations & onboarding (OpenSC, LeanIX-shaped)
- B2B SaaS product management (IntegrityNext, OpenSC, Oracle Utilities)
- Supply chain / agri-food traceability & ESG compliance SaaS
- AI-assisted prototyping & workflow design (AstroFinance, IntegrityNext AI feature) — differentiator inside solutions/impl/PM, not a standalone "AI builder" title
- Product ops: KPI dashboards, Jira/Notion/Airtable, Agile/Kanban
- Data tools: SQL, QuickSight, basic Python
- Public-sector proposals (Asia Foundation, WEConnect)

### Languages:
- English: Native | French: Native | German: B1-B2 (actively studying) | Spanish: B2

### Education & certs:
- MSc Policy Analysis & Management, Carnegie Mellon | BA International Development, McGill
- PMP (2019) | IBM AI Product Manager Certificate (2024)

---

## Primary role lanes (Aug 2026 — rank and apply in this order)

**Protocol (Sep 2026):** Solutions consulting, implementation management, and delivery
project management roles that pass the language gate take **highest precedence** — even above
product manager roles. Language gate: English/French native OK; German requirement must be
**none, plus, or B2 at most** (fluent/C1/C2/native fails gate and loses lane bump).

1. **Solutions / Pre-Sales / Engagement (technical-commercial)** — STRONGEST interview signal
   Titles: Solutions Consultant, Pre-Sales Solutions, Technical Pre-Sales, Engagement Manager,
   Solutions Engineer (discovery/scoping-heavy), AI Solution Strategist, Customer Solutions Engineer

2. **Software Implementations / Onboarding / CS delivery** — STRONG second signal
   Titles: Implementation Manager, Lead Implementation, Onboarding Manager, CS Onboarding,
   Implementation Consultant, Deployment Strategist (if maturity gates pass), Technical CSE (integration-heavy)

3. **Delivery project management** — third priority lane (above PM)
   Titles: Technical Project Manager, Implementation PM, Delivery PM (NOT PMO / program coordinator)

4. **Product Manager** — parallel track; best at mature product orgs (Typeform, n8n, NiCE)

WEAKER interview signal (deprioritize unless exceptional JD): pure Account Manager, Strategic AM,
PMO / Program Manager / prof-services coordinator, org-transformation consulting, sales-ops,
monitoring/eval ops, venture-builder biz dev, manufacturing/industrial domain PM.

---

## What Nic is looking for RIGHT NOW

### Hard requirements (must-haves — failure = hard disqualifier):
- HARD DQ German only for **native German** or **C2** (or "Muttersprache"/native-level).
  C1, B2 required, "fluent", or "professional working proficiency" are NOT hard DQs — use language_pen + Fit penalties.
- Language gate for lane precedence: English/French native OK; German must be **none / plus / B2 max**.
  Fluent, C1, professional working, C2, native → no lane bump; fluent −8, C1 −12 on final score.
- NOT seed-stage (or pre-seed). Hard DQ regardless of mission.
- NOT founded in the last 2 years. Hard DQ. Headcount does NOT matter — small teams OK past gates.
- NOT US-only or UK-only remote/hire when Nic is Berlin-based EU/US (must be EU-eligible or global remote)
- Not a high-burn "always-on" culture explicitly requiring 9-5+ intensity with no structure (Almedia-style)

### Strong preference (Fit factor — not hard DQ alone):
- At least one product supervisor (Head/Director/VP Product, CPO) OR product peer — for PM roles especially.
  Missing → Fit −10 to −20. Eng-only + founders ≠ product peer.
- For solutions/implementations roles: existing CS/implementation/solutions team or clear handoff to delivery
  (not lone commercial hire with no delivery scaffold — Fit −10 to −15).

### Climate / mission — IMPORTANT NUANCE (read carefully):
- Climate, sustainability, ESG, supply chain mission is a COMPETITIVENESS BOOSTER when paired with
  enterprise B2B SaaS and a solutions or implementations role (Pulsora, OpenSC, IntegrityNext pattern).
- Climate-first STARTUPS (seed, <2 years) are HARD DQ on maturity — not because climate is bad, but because
  Nic's interview data shows first rounds without offers there (Renew Earth, Sustaain, many Plan A/CEEZER/Regrow shapes).
- Climate **strategy consulting at industrials** (GEA-style) or **mission-only CS at young climate cos**:
  OK to apply if time, but LOWER competitiveness_score (−5 to −10 vs enterprise SaaS solutions) — interview
  activity without close history. Do NOT treat mission match as substitute for role family + maturity.
- DO NOT skip all climate roles — prioritize climate AT Series A+ / profitable B2B SaaS with solutions/impl titles.

### Nice-to-have (bonus_flags only — do NOT affect fit_score):
- EU remote or hybrid | French required/preferred | 4-day week mentioned
- Location (city/country) is NEVER a score factor except work_region hard DQ above

### Competitiveness boosters (interview probability — adjust Comp, not Fit):
- Role family: solutions/pre-sales/engagement (+8 to +12 Comp vs baseline)
- Role family: implementations/onboarding (+5 to +8 Comp)
- Role family: PM at mature B2B SaaS with product org (+3 to +6 Comp)
- French required or strongly preferred (+5 to +8 Comp)
- B2B SaaS | compliance/regtech/ESG/supply chain domain (+5 Comp if role family also strong)
- Prior interview at company (metadata prior_interview=true): +5 Comp via contact bump path
- AI-assisted prototyping / evals / workflow scoping as candidate quality (+5 to +8 Comp)

### Competitiveness reducers (lower Comp, not automatic skip):
- Pure Account Manager / quota-carrying AM (−8 to −12 Comp) — NinjaOne AM vs SE lesson
- Program Manager / PMO / prof-services coordinator (−5 to −10 Comp)
- Org transformation / NGO ops / strategy consulting without SaaS product (−5 to −10 Comp)
- "AI builder" / founding PM / solo product at seed — weak interview history (−5 Comp unless mature org)
- Climate mission-only at non-SaaS employer (−5 Comp; see climate nuance above)
- Intensity culture ("not 9-5", perpetual urgency, venture builder) (−5 to −10 Fit and −3 Comp)

### Things that reduce fit (soft):
- Pure consumer (no B2B) | German B2/C1/fluent required (not hard DQ) | Hyper-growth chaos | Engineering-degree gate
- No product supervisor/peer on PM roles | Blank-page founding with no scaffolding (workplace style)
- Low structure AND low autonomy simultaneously (−20 to −25 Fit)

## Workplace Style — environmental factors for sustained performance

Nic performs in a high-variance pattern: excellent in the right container, genuinely
compromised in the wrong one (not a flat, consistent performer across environments).
The following traits predict which side of that line a role falls on. Score these as
their own factor — they are about sustainability and long-term fit, not raw
competitiveness or stated preference match.

Environments where Nic has consistently thrived:
- Bounded deliverables with a real audience (a deck, a workshop, a deal, a pitch)
  rather than open-ended or purely theoretical work
- Personal/intellectual investment in the subject matter — not just competence at it
- An engaged counterpart (manager, client, partner) rather than anonymous process —
  he performs FOR people, not just for material
- Real autonomy in execution within a structured outer container — fixed deliverable,
  latitude in approach
- Short-to-medium feedback loops (weeks, not quarters or years) that keep effort and
  visible result connected
- Structured processes that already exist (not a blank-page/0-to-1 founding function
  with no scaffolding)

Environments where Nic has consistently struggled:
- Low structure AND low autonomy at the same time — diffuse expectations combined
  with top-down directives, with no room to bring his own thinking to the work (this
  is the worst-case combination; it removes both of his main success levers at once)
- Rote, repetitive, low-narrative work with no room for interpretation, regardless of
  his competence at it
- Long-horizon work with infrequent feedback and no intermediate checkpoints
- Environments requiring sustained effort generated purely by internal discipline,
  independent of interest or external structure (he does not reliably have this —
  effort tracks engagement, not willpower)
- Conflict-heavy or adversarial cultures requiring direct confrontation with authority
  to get needs met (he tends toward quiet disengagement or eventual exit rather than
  renegotiation)
- Seed / pre-seed orgs (also a hard DQ on maturity) where "ownership" means absorbing chaos
"""

# ──────────────────────────────────────────────────────────────
# SCORING PROMPT
# ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are an expert career advisor and talent evaluator. You receive a candidate profile and job descriptions.

For each JD produce a JSON evaluation object:
- "title": job title
- "company": company name (use "Unknown" if unclear)
- "role_family": one of:
    solutions_pre_sales  — Solutions Consultant, Pre-Sales, Technical Pre-Sales, Engagement Manager,
                          Solutions Engineer (scoping/demo-heavy), AI Solution Strategist, Customer Solutions Engineer
    implementations      — Implementation Manager, Lead Implementation, Onboarding, CS Onboarding, CSE (integration-heavy),
                          Implementation Consultant
    project_management   — Technical Project Manager, Implementation PM, Delivery PM (software delivery; NOT PMO)
    product_manager      — Product Manager, Product Ops (with product org)
    customer_success     — generic CSM / AM without solutions or implementation depth
    account_manager      — quota-carrying AM / Strategic AM
    program_manager      — PMO, Program Manager, Prof Services coordinator (no lane bump)
    consulting_other     — org transformation, strategy consulting, NGO ops, sales ops
    other
- "german_requirement": "none" | "plus" | "b2" | "fluent" | "c1" | "c2" | "native" — from JD text
- "language_gate_pass": true if german_requirement is none/plus/b2; false if fluent/c1/c2/native
- "interview_signal": "strong" | "moderate" | "weak"
- "french_language": "required" | "preferred" | "none" — from JD text (required/fluent/mandatory vs plus/preferred)
- "base_score": integer 0-100
- "competitiveness_score": integer 0-100 — interview/offer probability; MUST reflect role_family
  signal above (solutions +8-12, implementations +5-8, AM/PMO -5-12 vs neutral baseline).
  Climate mission alone must NOT inflate Comp if role_family is weak or company fails maturity gates.
- "fit_score": integer 0-100 — TWO components equally:
  (a) PREFERENCE FIT: product supervisor/peer (PM roles), delivery scaffold (solutions/impl roles),
      maturity gates, sustainable pace. No autopilot requirement. No headcount penalty.
  (b) WORKPLACE STYLE FIT: structure + autonomy, feedback loops, scaffolding vs blank-page chaos.
  Low structure + low autonomy together → Fit −20 to −25.
- "maturity_notes": founding year / funding stage vs hard gates; note if climate startup fails gates
- "hard_disqualifiers": list — German native/C2 only; seed/pre-seed; founded <2 years; US-only/UK-only hire
- "fit_highlights", "fit_concerns", "bonus_flags" (max 5 each)
- "recommended_action": "apply_now" | "apply_soon" | "apply_if_time" | "skip"
  — apply_now: strong role_family + passes maturity + no hard DQ
  — apply_soon: good fit but moderate signal or one soft concern
  — apply_if_time: climate mission-only, weak role_family, or stretch domain
  — skip: any hard DQ
- "one_line_verdict": single sentence
- "funding_stage_inferred": pre_seed|seed|series_a|series_b_plus|profitable|unknown

base_score = 0.5 * competitiveness_score + 0.5 * fit_score

IMPORTANT RULES:
- Hard DQs → cap base_score at 30, recommend skip: German **native or C2 only**; seed/pre-seed;
  founded <2 years; JD restricts to US-only or UK-only without EU work eligibility.
- German C1 / B2 required / "fluent" / professional proficiency → NOT hard DQ; set language_gate_pass=false,
  reduce Fit (−8 to −15), language_pen applied in post-processing (fluent −8, c1 −12).
  Do not add c1/fluent to hard_disqualifiers. c2/native → hard_disqualifiers.
- Lane precedence (post-processing): when language_gate_pass=true, solutions_pre_sales +6,
  implementations +6, project_management +4. product_manager and PMO get 0. This can outrank PM on chart.
- french_language "required" → +7 competitiveness worth (applied as french_bump in post-processing).
  french_language "preferred" → +4. Always set french_language field from JD.
- Climate: NEVER hard-DQ climate mission alone. Seed/young climate startups DQ on maturity, not mission.
  Climate strategy consulting / young-climate CSM → lower Comp (−5-10), apply_if_time at best.
  Climate + enterprise B2B SaaS + solutions/impl → strong Comp (Pulsora pattern).
- Product peer/supervisor: Fit preference for PM roles; missing → Fit −10 to −20, not base cap alone.
- AI prototyping/evals: Comp booster as candidate quality, not a separate "AI builder" role family.
- COMPETITIVENESS ≠ FIT. Profitable mature SaaS + weak role (AM) can be Fit 70 / Comp 45.
- Do not invent Series A+ from "climate tech" or "VC-backed". Unknown funding → unknown (0 bump).

Return ONLY valid JSON, no markdown fences:
{"evaluations": [{"jd_key": "<key>", ...}, ...]}
"""

# ──────────────────────────────────────────────────────────────
# BUMP TABLES
# ──────────────────────────────────────────────────────────────

def recency_bump(days):
    if days is None:
        return 0, "unknown posting date"
    if days == 0:
        return 10, "posted today"
    if days <= 7:
        return 10, f"posted {days}d ago"
    if days <= 14:
        return 6, f"posted {days}d ago"
    if days <= 30:
        return 3, f"posted {days}d ago"
    if days <= 60:
        return 1, f"posted {days}d ago"
    return 0, f"posted {days}d ago (stale)"

CONTACT_BUMPS = {
    "none":             (0,  "no prior contact"),
    "positive_contact": (7,  "prior positive contact"),
    "interview":        (15, "previously in interview pipeline"),
}

FUNDING_BUMPS = {
    "pre_seed":      (-10, "pre-seed"),
    "seed":          (-5,  "seed stage"),
    "series_a":      (+5,  "Series A"),
    "series_b_plus": (+8,  "Series B+"),
    "profitable":    (+8,  "profitable / privately held"),
    "unknown":       (0,   "funding stage unknown"),
}

# Applicant volume: high competition reduces expected return on application effort
APPLICANT_BUMPS = {
    "low":     (+5,  "<30 applicants — low competition"),
    "medium":  (0,   "30-99 applicants — moderate competition"),
    "high":    (-5,  "100+ applicants — high competition"),
    "unknown": (0,   "applicant volume unknown"),
}

FRENCH_BUMPS = {
    "required":  (+7, "French fluent/required/mandatory"),
    "preferred": (+4, "French preferred/plus/advantage"),
    "none":      (0,  "no French requirement"),
    "unknown":   (0,  "French requirement unknown"),
}

# German requirement levels — language gate for lane precedence
VALID_GERMAN = {"none", "plus", "b2", "fluent", "c1", "c2", "native", "unknown"}

LANGUAGE_GATE_PASS = {"none", "plus", "b2", "unknown"}

LANGUAGE_PENALTIES = {
    "none":    (0,  "no German requirement"),
    "plus":    (0,  "German plus/bonus only"),
    "b2":      (0,  "German B2 max — passes language gate"),
    "unknown": (0,  "German requirement unknown"),
    "fluent":  (-8, "fluent German required — fails language gate"),
    "c1":      (-12, "German C1 required — fails language gate"),
    "c2":      (-15, "German C2 required — hard DQ"),
    "native":  (-15, "native German required — hard DQ"),
}

# Lane precedence bumps when language gate passes (Sep 2026 protocol)
LANE_PRECEDENCE_BUMPS = {
    "solutions_pre_sales": (6, "solutions/pre-sales lane — highest precedence"),
    "implementations":     (6, "implementations lane — highest precedence"),
    "project_management":  (4, "delivery project management lane"),
}

VALID_FUNDING = set(FUNDING_BUMPS)
VALID_CONTACT = set(CONTACT_BUMPS)
VALID_APPLICANTS = set(APPLICANT_BUMPS)
VALID_FRENCH = set(FRENCH_BUMPS)
VALID_WORK_REGIONS = {"eu", "global", "us_only", "uk_only", "unknown"}

# Role families with strongest historical interview → offer signal (non-PM track)
ROLE_FAMILIES = (
    "solutions_pre_sales",
    "implementations",
    "project_management",
    "product_manager",
    "customer_success",
    "account_manager",
    "program_manager",
    "consulting_other",
    "other",
)


def passes_language_gate(german_req):
    """True when German requirement is none/plus/b2/unknown (English/French native OK)."""
    return german_req in LANGUAGE_GATE_PASS


def lane_precedence_bump(role_family, german_req):
    """+6 solutions/impl, +4 delivery PM when language gate passes."""
    if not passes_language_gate(german_req):
        return 0, "language gate failed — no lane bump"
    entry = LANE_PRECEDENCE_BUMPS.get(role_family)
    if entry:
        return entry
    return 0, "not a priority lane"


def language_penalty(german_req):
    """Penalty for German above B2 (fluent/C1); c2/native also hard DQ."""
    return LANGUAGE_PENALTIES.get(german_req, (0, "German requirement unknown"))


def apply_bumps(base, days, contact, funding, applicants="unknown", french="unknown",
                role_family="other", german_req="unknown"):
    r_pts, r_label = recency_bump(days)
    c_pts, c_label = CONTACT_BUMPS.get(contact, (0, "no prior contact"))
    f_pts, f_label = FUNDING_BUMPS.get(funding, (0, "funding stage unknown"))
    a_pts, a_label = APPLICANT_BUMPS.get(applicants, (0, "applicant volume unknown"))
    fr_pts, fr_label = FRENCH_BUMPS.get(french, (0, "French requirement unknown"))
    lane_pts, lane_label = lane_precedence_bump(role_family, german_req)
    lang_pts, lang_label = language_penalty(german_req)
    final = max(0, min(100, base + r_pts + c_pts + f_pts + a_pts + fr_pts + lane_pts + lang_pts))
    return (final, r_pts, c_pts, f_pts, a_pts, fr_pts, lane_pts, lang_pts,
            r_label, c_label, f_label, a_label, fr_label, lane_label, lang_label)


def validate_metadata(metadata):
    """Warn on bad funding/contact/applicant values; never silently upgrade stage."""
    warnings = []
    for key, meta in metadata.items():
        funding = meta.get("funding_stage", "unknown")
        if funding not in VALID_FUNDING:
            warnings.append(f"{key}: invalid funding_stage={funding!r} → treating as unknown")
            meta["funding_stage"] = "unknown"
        contact = meta.get("contact_status", "none")
        if contact not in VALID_CONTACT:
            warnings.append(f"{key}: invalid contact_status={contact!r} → treating as none")
            meta["contact_status"] = "none"
        apps = meta.get("applicant_volume", "unknown")
        if apps not in VALID_APPLICANTS:
            warnings.append(f"{key}: invalid applicant_volume={apps!r} → treating as unknown")
            meta["applicant_volume"] = "unknown"
        french = meta.get("french_language", "unknown")
        if french not in VALID_FRENCH:
            warnings.append(f"{key}: invalid french_language={french!r} → treating as unknown")
            meta["french_language"] = "unknown"
        german = meta.get("german_requirement", "unknown")
        if german not in VALID_GERMAN:
            warnings.append(f"{key}: invalid german_requirement={german!r} → treating as unknown")
            meta["german_requirement"] = "unknown"
        elif german in {"c2", "native"}:
            warnings.append(
                f"{key}: german_requirement={german} — HARD DQ (native/C2 German required)"
            )
        # Soft warning: seed/pre-seed is a hard maturity DQ — flag loudly
        if meta.get("funding_stage") in {"seed", "pre_seed"}:
            warnings.append(
                f"{key}: funding_stage={meta.get('funding_stage')} — HARD DQ under current rubric "
                f"(no seed/pre-seed companies)"
            )
        if meta.get("founded_year") is not None:
            try:
                age = date.today().year - int(meta["founded_year"])
                if age < 2:
                    warnings.append(
                        f"{key}: founded_year={meta['founded_year']} — HARD DQ "
                        f"(company younger than 2 years)"
                    )
            except (TypeError, ValueError):
                pass
        wr = meta.get("work_region", "unknown")
        if wr not in VALID_WORK_REGIONS:
            warnings.append(f"{key}: invalid work_region={wr!r} → treating as unknown")
            meta["work_region"] = "unknown"
        elif wr in {"us_only", "uk_only"}:
            warnings.append(
                f"{key}: work_region={wr} — HARD DQ for Berlin-based Nic unless JD allows EU"
            )
    return warnings

# ──────────────────────────────────────────────────────────────
# INPUT LOADING
# ──────────────────────────────────────────────────────────────

def load_jds_from_folder(folder):
    jds = {}
    for f in sorted(folder.glob("*.txt")):
        jds[f.stem] = f.read_text(encoding="utf-8").strip()
    meta_path = folder / "metadata.json"
    metadata = {}
    if meta_path.exists():
        metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        print(f"Loaded metadata for: {', '.join(metadata.keys())}", file=sys.stderr)
        for w in validate_metadata(metadata):
            print(f"⚠ metadata: {w}", file=sys.stderr)
    else:
        print(
            "No metadata.json found — recency, contact, and funding signals will be neutral.\n"
            "⚠ Without verified funding_stage, do NOT guess Series A+ from mission quality.",
            file=sys.stderr,
        )
    return jds, metadata

# ──────────────────────────────────────────────────────────────
# EVALUATION
# ──────────────────────────────────────────────────────────────

def evaluate_jds(jds):
    try:
        import anthropic
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "anthropic package required to evaluate JDs. pip install anthropic"
        ) from exc
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    jd_block = ""
    for idx, (key, text) in enumerate(jds.items(), 1):
        jd_block += f"\n\n=== JD {idx} (key: {key}) ===\n{text}\n"
    user_message = (
        f"## Candidate Profile\n{PROFILE}\n\n## Job Descriptions\n{jd_block}\n\n"
        f"Evaluate all {len(jds)} JDs and return JSON.\n\n"
        "REMINDER: Keep competitiveness_score and fit_score independent. "
        "Hard DQs: German native/C2 only, seed/pre-seed, founded <2 years, US-only/UK-only hire. "
        "Score role_family interview signal on Comp (solutions/impl strong; AM/PMO weak). "
        "Climate mission is NOT a DQ — maturity gates are. Climate-only weak roles → apply_if_time."
    )
    print(f"Sending {len(jds)} JD(s) to Claude...\n", file=sys.stderr)
    response = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=4096, system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    evaluations = {e["jd_key"]: e for e in json.loads(raw)["evaluations"]}
    # Enforce hard-DQ base cap locally so a model slip cannot bypass it
    for key, ev in evaluations.items():
        if ev.get("hard_disqualifiers"):
            capped = min(int(ev.get("base_score", 0)), 30)
            if capped != ev.get("base_score"):
                print(
                    f"⚠ {key}: hard disqualifiers present — capping base_score "
                    f"{ev.get('base_score')} → {capped}",
                    file=sys.stderr,
                )
                ev["base_score"] = capped
        # Recompute base from components if present (guards Comp/Fit inflation mismatch)
        if "competitiveness_score" in ev and "fit_score" in ev:
            expected = int(round(0.5 * ev["competitiveness_score"] + 0.5 * ev["fit_score"]))
            if ev.get("hard_disqualifiers"):
                expected = min(expected, 30)
            if abs(expected - int(ev.get("base_score", expected))) > 1:
                print(
                    f"⚠ {key}: base_score {ev.get('base_score')} ≠ 0.5*comp+0.5*fit "
                    f"({expected}) — correcting",
                    file=sys.stderr,
                )
                ev["base_score"] = expected
    return evaluations

# ──────────────────────────────────────────────────────────────
# DISPLAY
# ──────────────────────────────────────────────────────────────

ACTION_EMOJI = {"apply_now": "🟢", "apply_soon": "🟡", "apply_if_time": "🟠", "skip": "🔴"}
INTERVIEW_SIGNAL_EMOJI = {"strong": "📈", "moderate": "➖", "weak": "📉", "unknown": "❓"}
FUNDING_EMOJI = {
    "pre_seed": "🌱", "seed": "🌿", "series_a": "🅰️",
    "series_b_plus": "🅱️", "profitable": "💰", "unknown": "❓"
}

def build_rankings(evaluations, metadata):
    results = []
    for key, ev in evaluations.items():
        meta     = metadata.get(key, {})
        days       = meta.get("days_since_posted")
        contact    = meta.get("contact_status", "none")
        funding    = meta.get("funding_stage") or ev.get("funding_stage_inferred") or "unknown"
        if funding not in VALID_FUNDING:
            funding = "unknown"
        applicants = meta.get("applicant_volume", "unknown")
        french     = meta.get("french_language") or ev.get("french_language") or "unknown"
        if french not in VALID_FRENCH:
            french = "unknown"
        german     = meta.get("german_requirement") or ev.get("german_requirement") or "unknown"
        if german not in VALID_GERMAN:
            german = "unknown"
        role_family = meta.get("role_family") or ev.get("role_family") or "other"
        employees  = meta.get("employees")
        bump_result = apply_bumps(
            ev.get("base_score", 0), days, contact, funding, applicants, french,
            role_family=role_family, german_req=german)
        (final, r_pts, c_pts, f_pts, a_pts, fr_pts, lane_pts, lang_pts,
         r_label, c_label, f_label, a_label, fr_label, lane_label, lang_label) = bump_result
        results.append({**ev, "jd_key": key, "final_score": final,
                        "recency_pts": r_pts, "contact_pts": c_pts,
                        "funding_pts": f_pts, "applicant_pts": a_pts,
                        "french_pts": fr_pts, "lane_pts": lane_pts, "language_pts": lang_pts,
                        "recency_label": r_label, "contact_label": c_label,
                        "funding_label": f_label, "applicant_label": a_label,
                        "french_label": fr_label, "lane_label": lane_label,
                        "language_label": lang_label,
                        "german_requirement": german, "language_gate_pass": passes_language_gate(german),
                        "funding_stage": funding, "employees": employees, "role_family": role_family})
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results

def format_results(rankings):
    today = date.today().isoformat()
    lines = [f"# JD Ranking Results — {today}\n"]
    lines.append(f"{'#':<4} {'Score':<7} {'Base':<6} {'Fit':<5} {'Comp':<5} {'+Rec':<6} {'+Con':<6} {'+Fund':<7} {'+App':<6} {'+Fr':<5} {'+Lane':<6} {'+Lang':<6} {'Gate':<5} {'Fund':<5} {'Act':<5} {'Company':<20} Title")
    lines.append("-" * 175)
    for i, r in enumerate(rankings, 1):
        emoji   = ACTION_EMOJI.get(r.get("recommended_action", "?"), "⚪")
        femoji  = FUNDING_EMOJI.get(r.get("funding_stage", "unknown"), "❓")
        f_pts   = r["funding_pts"]
        a_pts   = r["applicant_pts"]
        fr_pts  = r.get("french_pts", 0)
        lane_pts = r.get("lane_pts", 0)
        lang_pts = r.get("language_pts", 0)
        gate    = "✓" if r.get("language_gate_pass") else "✗"
        f_str   = f"+{f_pts}" if f_pts >= 0 else str(f_pts)
        a_str   = f"+{a_pts}" if a_pts >= 0 else str(a_pts)
        fr_str  = f"+{fr_pts}" if fr_pts >= 0 else str(fr_pts)
        lane_str = f"+{lane_pts}" if lane_pts >= 0 else str(lane_pts)
        lang_str = f"+{lang_pts}" if lang_pts >= 0 else str(lang_pts)
        lines.append(
            f"{i:<4} {r['final_score']:<7} {r.get('base_score',0):<6} "
            f"{r.get('fit_score',0):<5} {r.get('competitiveness_score',0):<5} "
            f"+{r['recency_pts']:<5} +{r['contact_pts']:<5} {f_str:<7} {a_str:<6} {fr_str:<5} "
            f"{lane_str:<6} {lang_str:<6} {gate:<5} "
            f"{femoji:<5} {emoji:<5} {r.get('company','?')[:18]:<20} {r.get('title','?')[:42]}"
        )
    lines.append("")
    for i, r in enumerate(rankings, 1):
        emoji  = ACTION_EMOJI.get(r.get("recommended_action", "?"), "⚪")
        femoji = FUNDING_EMOJI.get(r.get("funding_stage", "unknown"), "❓")
        f_pts  = r["funding_pts"]
        a_pts  = r["applicant_pts"]
        fr_pts = r.get("french_pts", 0)
        lane_pts = r.get("lane_pts", 0)
        lang_pts = r.get("language_pts", 0)
        f_str  = f"+{f_pts}" if f_pts >= 0 else str(f_pts)
        a_str  = f"+{a_pts}" if a_pts >= 0 else str(a_pts)
        fr_str = f"+{fr_pts}" if fr_pts >= 0 else str(fr_pts)
        lane_str = f"+{lane_pts}" if lane_pts >= 0 else str(lane_pts)
        lang_str = f"+{lang_pts}" if lang_pts >= 0 else str(lang_pts)
        gate_str = "pass" if r.get("language_gate_pass") else "FAIL"
        lines.append(f"---\n## {i}. {r.get('company','?')} — {r.get('title','?')}")
        emp_str = f"  |  👥 {r['employees']}" if r.get("employees") else ""
        lines.append(
            f"**Final score**: {r['final_score']}/100  "
            f"(base {r.get('base_score',0)} + recency +{r['recency_pts']} "
            f"+ contact +{r['contact_pts']} + funding {f_str} + applicants {a_str} "
            f"+ french {fr_str} + lane {lane_str} + language {lang_str})"
        )
        lines.append(
            f"Fit: {r.get('fit_score',0)}/100  |  "
            f"Competitiveness: {r.get('competitiveness_score',0)}/100"
        )
        lines.append(
            f"**Action**: {emoji} {r.get('recommended_action','?').upper()}  |  "
            f"**Lane**: {r.get('role_family','?')} {INTERVIEW_SIGNAL_EMOJI.get(r.get('interview_signal','unknown'), '❓')}  |  "
            f"**Language gate**: {gate_str} (German: {r.get('german_requirement','unknown')})  |  "
            f"{femoji} {r['funding_label']}{emp_str}"
        )
        lines.append(
            f"_{r['recency_label']}, {r['contact_label']}, {r['applicant_label']}, "
            f"{r.get('french_label', 'French requirement unknown')}, {r.get('lane_label', '')}, "
            f"{r.get('language_label', '')}_"
        )
        lines.append(f"\n**Maturity**: {r.get('maturity_notes', 'N/A')}")
        lines.append(f"\n> {r.get('one_line_verdict','')}\n")
        if r.get("hard_disqualifiers"):
            lines.append("**🚫 Hard disqualifiers:**")
            for d in r["hard_disqualifiers"]: lines.append(f"  - {d}")
            lines.append("")
        if r.get("fit_highlights"):
            lines.append("**✅ Fit highlights:**")
            for h in r["fit_highlights"]: lines.append(f"  - {h}")
            lines.append("")
        if r.get("bonus_flags"):
            lines.append("**⭐ Bonus flags:**")
            for b in r["bonus_flags"]: lines.append(f"  - {b}")
            lines.append("")
        if r.get("fit_concerns"):
            lines.append("**⚠️ Concerns:**")
            for c in r["fit_concerns"]: lines.append(f"  - {c}")
            lines.append("")
    return "\n".join(lines)

# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    folder = Path(sys.argv[1])
    if not folder.is_dir():
        print(f"Error: {folder} is not a directory", file=sys.stderr)
        sys.exit(1)
    jds, metadata = load_jds_from_folder(folder)
    if not jds:
        print(f"No .txt files found in {folder}", file=sys.stderr)
        sys.exit(1)
    print(f"Loaded {len(jds)} JD(s): {', '.join(jds.keys())}\n", file=sys.stderr)
    evaluations = evaluate_jds(jds)
    rankings    = build_rankings(evaluations, metadata)
    output      = format_results(rankings)
    print(output)
    out_file = Path("jd_ranking_results.md")
    out_file.write_text(output, encoding="utf-8")
    print(f"\n✅ Results saved to: {out_file.resolve()}", file=sys.stderr)

if __name__ == "__main__":
    main()
