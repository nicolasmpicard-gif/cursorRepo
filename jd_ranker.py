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
   days_since_posted     : integer, or omit/null if unknown
   employees             : integer headcount if known (informational; not a Fit penalty)
   founded_year          : integer if known (HARD DQ if company age < 2 years)
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
final_score    = clamp(0, 100, base_score + recency_bump + contact_bump + funding_bump + applicant_bump)

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
5. Location (country/city/remote) must NOT raise or lower scores. Language
   requirements (e.g. German C1) still can.
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
~10 years PM and product operations experience.

### Key experience areas (in rough order of depth):
- B2B SaaS product management (IntegrityNext, OpenSC, Oracle Utilities)
- Supply chain transparency and agri-food traceability (OpenSC / Nespresso value chain)
- ESG/sustainability compliance SaaS (IntegrityNext — CSRD, supplier due diligence)
- Web3 / tokenized real-world assets (AstroFinance — aerospace assets on Algorand)
- Community platform management and growth (we are village / BuddyBoss)
- Implementation management and solutions consulting (OpenSC, Oracle)
- Public-sector / government proposal development (Asia Foundation — grant proposals)
- Pre-sales technical proposal contribution (Oracle Utilities)
- Product ops: KPI dashboards, Jira/Notion/Airtable, Agile/Kanban
- Data tools: SQL, Amazon QuickSight, Google Sheets modeling
- Design/discovery: Figma, Miro, AI-assisted prototyping

### Languages:
- English: Native
- French: Native
- German: B1-B2 (actively studying)
- Spanish: B2

### Education:
- MSc Policy Analysis & Management, Carnegie Mellon
- BA International Development, McGill

---

## What Nic is looking for RIGHT NOW

### Hard requirements (must-haves — failure = hard disqualifier or severe fit cut):
- Does NOT require German fluency (B2 and above required by employer = disqualifier; B2 optional is fine)
- NOT seed-stage (or pre-seed). Seed / pre-seed companies are a hard disqualifier regardless of
  mission quality. Series A+ or profitable/bootstrapped-beyond-seed is fine.
- NOT founded in the last 2 years. Companies younger than ~24 months are a hard disqualifier.
  Headcount does NOT matter — small teams are OK if the company clears age + stage gates.
- Company prizes knowledge management, experimentation, and structured research culture
- Not a high-burn startup in desperate scale-up mode (structured environment, sustainable pace)

### Strong preference (Fit factor — not a hard DQ by itself):
- At least one existing product supervisor (Head/Director/VP Product, CPO) OR product peer (another PM).
  "VP of Engineering" + "Product Engineer" + founders does NOT count as product supervision/peers.
  Solo / first-PM / blank-page product seats without a product counterpart → Fit cut (−10 to −20),
  not an automatic base_score cap unless combined with other hard DQs.

### Nice-to-have (appear as bonus flags in output, do NOT affect fit_score):
- Partially or fully remote within EU
- 4-day / part-time work week options mentioned
- NOTE: Location itself (Germany vs Greece vs France vs US, onsite city, etc.) must NOT
  change competitiveness_score, fit_score, or final_score. Remote/onsite may appear as
  bonus_flags only.

### Competitiveness boosters (Nic is more likely to get interviews):
- French language required or strongly preferred
- B2B SaaS
- Climate, sustainability, Agtech, or supply chain tech
- Regulatory tech, compliance, or ESG/reporting software
- Implementation, solutions, or customer-facing PM hybrid roles
- Roles valuing innovation, prototyping, or 0-to-1 thinking as a *candidate quality*:
  Nic has a strong track record here — clickable prototypes at AstroFinance (one built in
  Claude Code that placed top 6 of 100+ teams in the Algorand Foundation pitch competition),
  AI-assisted prototyping as a practised skill, launched a B2B CX diagnostic tool from
  scratch with 5 engineers, and "AI-assisted research & prototyping" explicitly on both CVs.
  This is a genuine differentiator. NOTE: do not confuse "builder/prototyper as a
  candidate quality" with a blank-page founding seat that lacks product peers — the
  latter is a Fit concern, the former is a Comp booster.

### Things that reduce fit (soft disqualifiers):
- Pure consumer product (no B2B component)
- Hard German fluency requirement
- Hyper-growth scale-up with unclear structure
- Requires deep technical background (engineering degree, ML expertise, CAx/CAD kernels, etc.)
- No sustainability or social impact angle at all (not disqualifying, just less motivating)
- No product supervisor or peer (solo / first-PM seat) — Fit cut, not hard DQ alone
- Roles that are pure blank-page founding functions with no scaffolding (workplace-style hit)

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
- "base_score": integer 0-100
- "competitiveness_score": integer 0-100 (how likely Nic is to get an interview/offer)
- "fit_score": integer 0-100 — incorporates TWO components equally:
  (a) PREFERENCE FIT: product supervisor/peer present, sustainable pace/culture, and
      maturity gates (not seed/pre-seed; not founded within last 2 years). Headcount is
      NOT a fit penalty. Autopilot/steady-state in 6-12 months is NOT required and must
      NOT drive fit_score. Remote work and 4-day week are NOT fit factors — bonus_flags only.
      LOCATION (country/city) is NEVER a fit factor.
  (b) WORKPLACE STYLE FIT: how well the role's day-to-day operating environment matches
      the Workplace Style traits in the profile (structure + autonomy, feedback loops,
      engaged counterpart, existing scaffolding vs blank-page chaos).
  The worst-case workplace style pattern (low structure + low autonomy simultaneously) should
  pull fit_score down by 20-25 pts on its own, noted explicitly in fit_concerns.
- "maturity_notes": one sentence on founding year / funding stage vs the hard gates
- "hard_disqualifiers": list of strings (deal-breakers) — include German B2+, seed/pre-seed,
  founded <2 years when applicable
- "fit_highlights": list of up to 5 strings
- "fit_concerns": list of up to 5 strings
- "bonus_flags": list of strings (remote, 4-day week, French, etc.)
- "which_cv": "product_ops" | "climate_pm" | "either"
- "recommended_action": "apply_now" | "apply_soon" | "apply_if_time" | "skip"
- "one_line_verdict": single sentence summary
- "funding_stage_inferred": one of pre_seed|seed|series_a|series_b_plus|profitable|unknown
  — only if metadata did not supply funding_stage; must be justified from known facts,
  never guessed upward from mission quality

base_score = 0.5 * competitiveness_score + 0.5 * fit_score

IMPORTANT RULES:
- Hard disqualifiers: German B2+/C1+ required; seed or pre-seed stage; company founded
  within the last 2 years. Any of these → cap base_score at 30 and recommend skip.
- Product supervisor OR peer is a strong Fit preference. Missing it → Fit −10 to −20,
  but NOT an automatic hard DQ / base cap by itself. Eng-only + founders ≠ product peer.
- Do NOT penalize fit for headcount or for "unlikely to reach autopilot in 6-12 months."
- Workplace style red flag: BOTH low structure (blank-page founding, no scaffolding) AND
  low autonomy/directive management → additional Fit −20 to −25; flag in fit_concerns.
- If a JD values innovation, prototyping, 0-to-1 work, or a "builder" mindset as a
  *candidate quality*, boost competitiveness_score by 5-8 pts (Nic's prototype track record).
- COMPETITIVENESS ≠ FIT. Never let Comp 75+ drag Fit upward.
- Do NOT use location (Germany/Greece/France/US/Berlin/Athens/remote) to raise or lower
  competitiveness_score, fit_score, or base_score. Language requirements may still disqualify.
- Be specific and honest — do not inflate scores. When uncertain on funding stage, use
  "unknown" (0 bump), never invent a later stage. When uncertain on founding year, say so
  in maturity_notes and do not invent a cleared age gate.

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

VALID_FUNDING = set(FUNDING_BUMPS)
VALID_CONTACT = set(CONTACT_BUMPS)
VALID_APPLICANTS = set(APPLICANT_BUMPS)


def apply_bumps(base, days, contact, funding, applicants="unknown"):
    r_pts, r_label = recency_bump(days)
    c_pts, c_label = CONTACT_BUMPS.get(contact, (0, "no prior contact"))
    f_pts, f_label = FUNDING_BUMPS.get(funding, (0, "funding stage unknown"))
    a_pts, a_label = APPLICANT_BUMPS.get(applicants, (0, "applicant volume unknown"))
    final = max(0, min(100, base + r_pts + c_pts + f_pts + a_pts))
    return final, r_pts, c_pts, f_pts, a_pts, r_label, c_label, f_label, a_label


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
        "Hard DQs: German B2+, seed/pre-seed, founded <2 years. "
        "Headcount is fine; product peer/supervisor is a Fit preference not a hard DQ. "
        "Do NOT score on autopilot-in-6-12-months."
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
CV_LABEL     = {"product_ops": "Product Ops CV", "climate_pm": "Climate PM CV", "either": "Either CV"}
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
        employees  = meta.get("employees")
        final, r_pts, c_pts, f_pts, a_pts, r_label, c_label, f_label, a_label = apply_bumps(
            ev.get("base_score", 0), days, contact, funding, applicants)
        results.append({**ev, "jd_key": key, "final_score": final,
                        "recency_pts": r_pts, "contact_pts": c_pts,
                        "funding_pts": f_pts, "applicant_pts": a_pts,
                        "recency_label": r_label, "contact_label": c_label,
                        "funding_label": f_label, "applicant_label": a_label,
                        "funding_stage": funding, "employees": employees})
    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results

def format_results(rankings):
    today = date.today().isoformat()
    lines = [f"# JD Ranking Results — {today}\n"]
    lines.append(f"{'#':<4} {'Score':<7} {'Base':<6} {'Fit':<5} {'Comp':<5} {'+Rec':<6} {'+Con':<6} {'+Fund':<7} {'+App':<6} {'Fund':<5} {'Act':<5} {'Company':<20} Title")
    lines.append("-" * 150)
    for i, r in enumerate(rankings, 1):
        emoji   = ACTION_EMOJI.get(r.get("recommended_action", "?"), "⚪")
        femoji  = FUNDING_EMOJI.get(r.get("funding_stage", "unknown"), "❓")
        f_pts   = r["funding_pts"]
        a_pts   = r["applicant_pts"]
        f_str   = f"+{f_pts}" if f_pts >= 0 else str(f_pts)
        a_str   = f"+{a_pts}" if a_pts >= 0 else str(a_pts)
        lines.append(
            f"{i:<4} {r['final_score']:<7} {r.get('base_score',0):<6} "
            f"{r.get('fit_score',0):<5} {r.get('competitiveness_score',0):<5} "
            f"+{r['recency_pts']:<5} +{r['contact_pts']:<5} {f_str:<7} {a_str:<6} "
            f"{femoji:<5} {emoji:<5} {r.get('company','?')[:18]:<20} {r.get('title','?')[:42]}"
        )
    lines.append("")
    for i, r in enumerate(rankings, 1):
        emoji  = ACTION_EMOJI.get(r.get("recommended_action", "?"), "⚪")
        femoji = FUNDING_EMOJI.get(r.get("funding_stage", "unknown"), "❓")
        f_pts  = r["funding_pts"]
        a_pts  = r["applicant_pts"]
        f_str  = f"+{f_pts}" if f_pts >= 0 else str(f_pts)
        a_str  = f"+{a_pts}" if a_pts >= 0 else str(a_pts)
        lines.append(f"---\n## {i}. {r.get('company','?')} — {r.get('title','?')}")
        emp_str = f"  |  👥 {r['employees']}" if r.get("employees") else ""
        lines.append(
            f"**Final score**: {r['final_score']}/100  "
            f"(base {r.get('base_score',0)} + recency +{r['recency_pts']} "
            f"+ contact +{r['contact_pts']} + funding {f_str} + applicants {a_str})"
        )
        lines.append(
            f"Fit: {r.get('fit_score',0)}/100  |  "
            f"Competitiveness: {r.get('competitiveness_score',0)}/100"
        )
        lines.append(
            f"**Action**: {emoji} {r.get('recommended_action','?').upper()}  |  "
            f"**CV**: {CV_LABEL.get(r.get('which_cv','either'))}  |  "
            f"{femoji} {r['funding_label']}{emp_str}"
        )
        lines.append(f"_{r['recency_label']}, {r['contact_label']}, {r['applicant_label']}_")
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
