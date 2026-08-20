# One-pager PRD — Scopebrief v1

Working title for a planning-brief product. Structure follows [Planio’s lean PRD](https://plan.io/blog/one-pager-prd-product-requirements-document/): purpose, features, release criteria, constraints — destination, not implementation.

| | |
|---|---|
| **Product** | Scopebrief v1 |
| **Status** | Draft / pre-build |
| **Owner** | Founder / PM |
| **Audience** | Eng, design, advisors |
| **Release** | First internal prototype that can run a real manufacturer spend list end-to-end |

---

## 1. Purpose

**Elevator pitch.** When a sustainability manager at a German manufacturer must allocate a limited climate budget against a Scope 3 target, they cannot quickly see which supply-chain nodes would reduce *claimable* emissions, which only reduce risk or reputation, and which residual tonnes belong outside the value chain. Scopebrief produces that split as a planning brief they can take to Einkauf and the CFO.

**Who it is for.** Primary: Leiter/in Nachhaltigkeit (or Scope 3 lead) at German *Maschinenbau*, automotive suppliers, and similar industrials. Co-readers, not daily users: Einkauf (criticality, leverage) and Finance (claims, budget). Not for: carbon-market desks, offset project developers, or full GHG-inventory teams replacing Sphera/Watershed.

**Why build this now.** CSRD/ESRS E1 and SBTi force a wedge between **gross inventory** and **credits**. Existing tools measure hotspots; they do not allocate € by *claim type*. German manufacturers have SAP supplier lists and production-critical vendors; they do not have a trustworthy tier-2 graph. Insetting vs offsetting is still sold as a menu. The “at a glance” job is a brief, not a marketplace.

**Goals (this release).**

- A user can go from spend list + budget to a three-bucket plan in one session (~30–40 min).
- Every recommended euro is labeled **claimable / risk-reputation / residual BVCM** with a visible chain of logic.
- The takeaway is a shareable brief, not a purchase.

**Assumptions.**

- Users have (or can paste) tier-1 names, spend, and a rough criticality tag; they often lack mass, PCF, and origin.
- Tier-1 legal entities are the right primary object in this vertical (unlike agri traders).
- Material class (Warengruppe) can be inferred well enough to pick a lever class; user corrects chips.
- Users will be wrong about tier-2 names; the product must not depend on them.
- Spend-based estimates can rank *leverage*; they cannot, alone, book claimable tonnes — confidence must cap the claimable column.
- v1 is a planning brief. Marketplace / collaborator links are out.

**Open questions (do not block v1 copy, do block over-claiming).** Exact SBTi/FLAG language in UI; how much GHG-factor coverage we need for DE manufacturing Warengruppen; whether target gap is required or optional with a “leverage-only” mode.

---

## 2. Features

### Problems this release solves

- Cannot discriminate inventory-moving spend from risk spend from outside-chain contribution.
- Cannot start without a complete multi-tier map or a full carbon inventory.
- Cannot defend a mixed insetting/offsetting ranking to audit/finance.

### Core user stories

1. **As a** sustainability manager, **I want to** enter a climate budget, year, optional Scope 3 gap, and a tier-1 list (name, spend, criticality), **so that** the product ranks nodes with the data I already have.
2. **As a** sustainability manager, **I want** material class and origin inferred and editable, **so that** I am not blocked on commodity fields I do not have.
3. **As a** sustainability manager, **I want an immediate three-bucket allocation on tier 1**, **so that** I see the plan before any upstream enrich.
4. **As a** sustainability manager, **I want** probable upstream *structure* (stage / origin cluster) on top nodes only, with look-right / wrong / don’t-know, **so that** unknown T2 cannot be promoted into claimable.
5. **As a** sustainability manager, **I want** ranked actions split by claim type — not one mixed leaderboard — each with evidence, assumption, €/t range, time-to-impact, and confidence, **so that** I can fund / park / reject with editable €.
6. **As a** sustainability manager, **I want to** lock a decision record and export a one-page brief for Einkauf/CFO, **so that** the session produces an artifact, not a dashboard screenshot.

### Core interaction flow

`Budget + gap + T1 spend/criticality` → `At-a-glance split (claimable / risk / residual)` → `Optional review of inferred upstream on top nodes` → `Actions by claim type` → `Fund / park / reject` → `Locked brief`

**Look and feel (intent, not mockups).** One working screen is the allocation view: three bands, nodes as rows, confidence chips, no true/false supplier grid. Brief export should read as a Vorstand/Einkauf memo (allocation, assumptions, open questions), not as a carbon app.

**Glossary the UI must use consistently.** *Inventory / THG-Bilanz* = official gross GHG account. *Claimable* = can lower that account if MRV exists. *Risk* = protects production, compliance, or data; not a booked reduction. *BVCM* = beyond value chain mitigation; contribution/credits; never netted off Scope 3.

---

## 3. Release criteria

**Functionality (must ship).** Intake of budget + T1 table; three-bucket engine that never places a low-confidence or no-PCF node in claimable without an explicit user override flagged as assumption; partitioned action list; fund/park/reject; brief export. Inference of material class for common DE manufacturing categories (steel, aluminium, plastics, electronics, chemicals, logistics) with user correction.

**Usability.** First allocation visible without completing upstream review. Criticality is a tag, not a homework “segment the portfolio” step. Unknown is a valid state.

**Reliability.** Deterministic: same inputs → same bucket labels. No silent promotion of residual/BVCM into inventory language. If target gap is missing, UI states that ranking is leverage-only.

**Performance.** Paste/upload of ~50–200 suppliers returns the first allocation without a “come back tomorrow” wait for a full graph.

**Supportability.** Assumptions and factor sources are listed on the brief so a human can defend or reject them. No live credit-market integration to maintain.

### Not in v1 (explicit)

- Marketplace, project-developer links as climax, credit checkout
- True/false validation of named tier-2 companies
- Full Scope 1–3 inventory, CSRD report generation, or SBTi validator
- Replacing Einkauf / SAP as system of record
- Multi-tenant supplier portal / PCF collection campaign (later: “what would have to be true”)
- Agri/FLAG origin-insetting as the primary UX (wrong vertical)

---

## 4. Constraints (not dates)

- **Scope constraint:** one vertical (DE manufacturing), one job (planning brief), one session to value.
- **Data constraint:** no requirement for primary PCF, bill of materials, or correct T2 names to complete a brief.
- **Claim constraint:** product copy must stay on the mitigation hierarchy — abate in-chain first; BVCM labeled as residual contribution.
- **Trust constraint:** ranking must not look like lead-gen for offset vendors.
- **Team/resource constraint:** v1 is a prototype that can be run on a real anonymized spend extract; pixel-perfect design and ERP connectors are not required to learn.
- **Ideal first test:** a German manufacturer sustainability manager (or a proxy who has sat in that budget meeting) completes the flow with their T1 list and says whether they would forward the brief to Einkauf. Launch date is flexible around that learning, not a calendar gate.

**Done means the user can say:** “Of this €X, €A goes to in-chain work that can move the inventory, €B goes to risk at critical suppliers where tonnes are uncertain, €C is residual BVCM and we will not claim it as Scope 3. Here is the evidence and the unknowns.”
