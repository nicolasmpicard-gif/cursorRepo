# Scopebrief v1 — screens (user journey)

One session. Sustainability manager at a German manufacturer. Output is a **planning brief**, not a purchase.

**Instrument split (money):** in-chain (can count toward the Scope 3 target if measured) vs outside-chain / BVCM (will not).  
**Not a money bucket:** reputation / PR. Criticality and confidence are **attributes**, not destinations for euros.

```text
[1 Set the job] → [2 Load suppliers] → [3 The split]
                                              ├─ drawer: actions (fund / park / reject)
                                              └─ optional: upstream structure on top nodes
                                         → [4 The brief]
```

---

## Screen 1 — Set the job

**Job in the journey.** Name the constraint so later screens can allocate against a real number.

**User sees**
- Working title: *Allocate this year’s climate budget against your Scope 3 target*
- Fields:
  - Climate budget (€) — required
  - Budget year — required (e.g. 2026)
  - Scope 3 target gap — optional (tCO2e still to cut by a year, or “% remaining”)
- One sentence of help: *We will split this € into work that can count toward the target vs contribution that will not. This is a plan for Einkauf/CFO, not a checkout.*
- If gap is empty: inline note *Without a gap, we rank leverage only. We will not say you are “on track.”*

**User does**
- Enters budget + year
- Enters gap if they have it (from SBTi, CSRD plan, or last inventory)
- Continues

**Must not ask**
- Full GHG inventory upload
- Offset registry login
- Company-wide ESG questionnaire

**Empty / edge**
- Budget = 0 → cannot continue
- Gap present but tiny vs spend-based footprint later → warn on Screen 3, don’t block

**Done when.** A budget (and optional gap) exists. Next: suppliers.

---

## Screen 2 — Load suppliers

**Job in the journey.** Get the objects German manufacturing actually has: named tier-1 rows, spend, criticality.

**User sees**
- Paste/upload table (CSV or ~20-row grid): supplier name, annual spend €
- Criticality as a **tag per row**, not a homework “segment your portfolio” step: `must-have` / `substitutable` / `unknown` (default `unknown`)
- After parse: inferred **material class** chip (steel, aluminium, plastics, electronics, chemicals, logistics, other) and optional **origin** chip
- Concentration already computed: e.g. “12 suppliers = 80% of spend”
- Short allow-list of columns they can add if they have them: volume (t), “PCF already on file?” — all optional

**User does**
- Pastes the SAP-ish list they already use
- Tags a few must-have lines (the ones Einkauf would shout about)
- Corrects a handful of wrong material chips; ignores the rest
- Continues — **does not** enter tier-2 names

**Must not ask**
- Named tier-2 / melt shop / farm
- Commodity as a required field
- True/false validation of an inferred supplier graph

**Empty / edge**
- 1–2 rows: still allow; say the split will be crude
- 200+ rows: auto-focus the head (e.g. top 80% spend + all must-haves); long tail collapsed
- Unrecognised name: material class = `other`, confidence low — still in the table

**Done when.** There is a T1 list with spend. Criticality may still be mostly `unknown`. Next: the split, immediately.

---

## Screen 3 — The split (hero)

**Job in the journey.** The “at a glance” moment. This is the product.

**User sees (one screen, two money columns)**

| In-chain — can count toward the target | Outside the chain — will not |
|---|---|
| Supplier actions, material switches, supplier energy, **enabling** spend (e.g. buy a PCF) | Residual BVCM / credits, labeled as contribution |

Plus a **header bar** that always shows:
- Budget €X
- Suggested split: €A in-chain / €C outside-chain / € unallocated
- If gap exists: “this in-chain package is in the right *direction* for the gap; tonnes are ranges, not a booked reduction”
- If no gap: “leverage-only mode”

Each **row is a tier-1 supplier** (not a T2 company). On the row:
- Name, spend, material chip, criticality badge
- **Confidence** (low / medium / high) — drives whether in-chain actions may be described as target-relevant reductions vs enabling-only
- Suggested € in this column (editable later in the drawer)
- One-line why: *High spend, steel, no PCF → don’t book tonnes; fund data or a documented grade if leverage exists*

**Criticality** is a badge (don’t break must-have supply). It does **not** get its own euro column.  
**Reputation / PR** does not appear.

**User does**
- Scans the two columns and the header split
- Opens a row to decide actions (Screen 3a)
- Optionally expands “probable upstream” on the top few rows (Screen 3b)
- Does **not** have to finish 3b to use 3a or go to Screen 4

**Must not show**
- A single mixed leaderboard of “best practice insetting and offsetting”
- Named hypothetical tier-2 companies as if known
- “Risk-reputation €” as a third pile

**Empty / edge**
- All confidence low → in-chain column is mostly *enabling* (PCF, engagement), not “tCO2e reduced”
- Must-have + low confidence → recommend enabling or park reductions; do not recommend switching away the qualified mill as a default
- Budget smaller than sum of suggestions → header shows over-alloc; user must cut on Screen 3a / 4

**Done when.** User understands the proposed split well enough to open rows or go write the brief. Value even if they stop here.

---

## Screen 3a — Action drawer (same page)

**Job in the journey.** Turn a node into fund / park / reject. Not a new wizard step.

**User sees (panel on the selected T1)**
- Two stacked lists, never merged:
  1. **In-chain** — e.g. documented lower-carbon grade; supplier PPA/efficiency; pay for PCF (marked *enabling: does not move the inventory this year*)
  2. **Outside-chain** — e.g. high-integrity credits for residual gap this year (marked *will not count toward the target*)
- Each action card:
  - Evidence → assumption → target-relevant: yes/no
  - € suggested, tCO2e **range** (hidden or “n/a” on enabling), years to impact, confidence
  - “What would have to be true” (e.g. mill sends PCF; Einkauf accepts a premium)
- Controls: **Fund** / **Park** / **Reject**
  - **Fund** = this year’s euros, in the brief (amount editable). Not a PO.
  - **Park** = not this cycle, keep on the list (€ = 0).
  - **Reject** = off the plan; optional one-line reason so it isn’t re-pitched as new.

**User does**
- Funds a small set (typical: 3–8 actions, not 40)
- Parks the right-idea-too-soon items
- Rejects anything that treats credits as if they cut Scope 3, or where they have no leverage
- Closes the drawer; header bar on Screen 3 updates live

**Must not**
- Send them to a marketplace or “choose a project developer”
- Require a T2 name to fund an in-chain action on the T1 contract they already have

**Done when.** At least the header split reflects *their* choices, not only the default suggestion. They can fund nothing yet and still continue — Screen 4 will say the plan is empty.

---

## Screen 3b — Upstream structure (optional, same page, top nodes only)

**Job in the journey.** Improve confidence. Never a quiz, never a gate.

**User sees**
- For the current (or top N) T1: *Probable upstream structure* — process stage + likely origin cluster, **not** a company name  
  Example: *Machined steel from Müller Präzision → likely bar/melt on a coal-heavy grid, confidence 40–70%.*
- Three answers: **looks right** / **looks wrong** / **I don’t know**

**User does**
- Answers only if they have a hunch; skip is equivalent to “I don’t know”
- If wrong: they can type a correction at structure level (“we buy from a DE EAF route”) — still not a T2 legal entity requirement

**Effect**
- Don’t know / skip → confidence stays low → in-chain *reductions* stay capped; enabling actions remain fundable
- Looks right → confidence may rise; still no invented T2 row in the brief
- Looks wrong → drop or replace the assumption; do not invent a new named supplier

**Must not**
- Block Screen 3 or 4 on completion
- Ask “is this mill the real tier 2? yes/no” for a generated list of names

**Done when.** Either skipped or answered for a few head nodes. Journey continues either way.

---

## Screen 4 — The brief

**Job in the journey.** Produce the artifact the session was for. Lock the plan as a **decision record**, not a purchase.

**User sees**
- The sentence they must be able to say out loud:  
  *Of €X, €A is in-chain work that can count toward the target (of which €A1 is enabling data, €A2 is potential reductions). €C is residual contribution outside the value chain and will not be claimed as Scope 3. €U unallocated. Assumptions and unknowns listed below.*
- Tables: Funded / Parked / Rejected
- Open questions for Einkauf (leverage, premium, dual source — as *questions*, not as climate-budget line items)
- Assumption log (material class, confidence, no PCF, upstream unknown)
- Buttons: **Lock plan** · **Export PDF** · **Copy link** (share to Einkauf/CFO)
- Explicit non-goal on the page: *This is not an order and not a credit purchase.*

**User does**
- Skims; jumps back to Screen 3 to change a fund/park/reject if needed
- Locks
- Exports / copies the link and leaves

**Must not**
- Collaborator marketplace, “buy this project,” offset checkout
- Auto-emailing suppliers
- Claiming tonnes as already reduced

**Empty / edge**
- Nothing funded → brief can still export as “no allocation this cycle; here is the ranked pipeline (parked)” — honest, still useful
- Over-allocated → cannot lock until € funded ≤ budget

**Done when.** A locked brief exists. That is the end of v1.

---

## What “done” is for the whole journey

The user can forward a one-pager that Einkauf/CFO can argue with, in which:

1. Every euro is **in-chain** or **outside-chain**, never both.
2. In-chain enabling spend is not dressed up as tonnes already moved.
3. Outside-chain is not dressed up as Scope 3 reduction.
4. Must-have suppliers were visible; PR/reputation was not a budget line.
5. Tier-2 names were not required and may be entirely wrong without breaking the brief.
