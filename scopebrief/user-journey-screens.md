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
- **Criticality** per row: **1–5 stars** plus **unknown** (default `unknown`, not 0 stars)

  | Stars | Meaning (production, not climate) |
  |---|---|
  | ★★★★★ | Cannot substitute — production / qualification stops without them |
  | ★★★★ | Very hard to substitute (long re-qualification, few alternatives) |
  | ★★★ | Moderate switching cost / time |
  | ★★ | Substitutable with some work |
  | ★ | Easily substitutable / commodity-like |
  | ? | Unknown — not rated yet |

  Stars do **not** decide in-chain vs outside-chain. They only constrain *which in-chain moves are allowed* (e.g. ★★★★★: do not default to “switch supplier”).
- After parse: inferred **material class** chip (steel, aluminium, plastics, electronics, chemicals, logistics, other) and optional **origin** chip
- Concentration already computed: e.g. “12 suppliers = 80% of spend”
- Short allow-list of columns they can add if they have them: volume (t), “PCF already on file?” — all optional

**User does**
- Pastes the SAP-ish list they already use
- Stars the few lines Einkauf would shout about; leaves the rest `?`
- Corrects a handful of wrong material chips; ignores the rest
- Continues — **does not** enter tier-2 names

**Must not ask**
- Named tier-2 / melt shop / farm
- Commodity as a required field
- True/false validation of an inferred supplier graph

**Empty / edge**
- 1–2 rows: still allow; say the split will be crude
- 200+ rows: auto-focus the head (e.g. top 80% spend + all ★★★★ / ★★★★★); long tail collapsed
- Unrecognised name: material class = `other`, confidence low — still in the table

**Done when.** There is a T1 list with spend. Criticality may still be mostly `?`. Next: the split, immediately.

---

## How Screen 3 decides in-chain vs outside-chain

This is a **boundary test on each ACTION**, not a score on the supplier, and not a function of stars or tonnes.

**The user is not asked these questions.** They are the product’s internal rule. The user sees the action already in a column plus a one-line why, and may override only as a flagged assumption.

A **supplier is always in the value chain** (they are already in Scope 3 purchased goods). What changes columns is **what you would spend money on**.

### The rule (apply in order, stop at first yes)

**1. Is the instrument a credit (or equivalent certificate) you would retire and disclose separately?**  
If yes → **outside-chain**.  
You are buying a claim sitting *beside* the THG-Bilanz. CSRD/ESRS E1 and SBTi do not let you subtract it from Scope 3.  
Examples: Verra/Gold Standard retirement, generic BVCM portfolio, a “climate contribution” with no change to the parts you buy.

**2. Does the activity change something already inside this company’s inventory boundary — a listed tier-1 product, a contracted inbound lane, a specified input to parts you buy — and would you book the result as updated activity data / emission factor / PCF, not as a retired credit?**  
If yes → **in-chain**.  
Examples: premium for a documented lower-carbon steel grade from mill X; co-fund efficiency at that mill and take it through their PCF; pay for a PCF (*enabling* in-chain: still in-chain, does not move tonnes this year); shift a contracted lane from air to rail.

**3. Otherwise → outside-chain.**  
No contractual or volume link to sourced goods/logistics (unrelated project, unrelated geography/sector). Treat as contribution.

**Double-count lock.** If a supplier project could be *either* a PCF reduction *or* sold credits, v1 picks **one**: credit retirement → outside-chain; procurement/PCF change and **no** credit taken → in-chain. Never both for the same tonnes.

### What does *not* decide the column

| Signal | What it actually does |
|---|---|
| Spend, hotspot size, €/t | Ranking / how much € to suggest — not the column |
| Criticality stars | Which in-chain *moves* are allowed (★★★★★: engage in place, don’t default to switch) |
| Confidence / unknown T2 | Whether in-chain spend may be described as a **reduction** vs **enabling only** |
| “Looks good in the report” | Out of product |

User may **override** a column only with an explicit assumption on the card (flagged on the brief). Silent overrides are not allowed.

### How the product applies this in v1 (no extra data)

It does not run an LLM vibe check. It **generates candidate actions** from (T1 + material class + spend + stars), then **stamps each candidate** with a default instrument type:

| Generated action type | Default column |
|---|---|
| Buy PCF / EPD from this T1 | In-chain, *enabling* |
| Documented lower-carbon grade / recycled content on this T1 PO | In-chain |
| Supplier energy / process measure at this T1, accounted via PCF | In-chain |
| Switch volume to an alternate T1 (only if stars ≤ ★★★ or `?`) | In-chain |
| Residual € after in-chain suggestions, as high-integrity credits | Outside-chain |
| Any marketplace-style credit tied to this supplier “as inset credits” | Outside-chain (v1 conservative) |

Left column of Screen 3 = **T1 rows with their in-chain actions**.  
Right column = **outside-chain actions**, usually one residual company-level line, not a second copy of the supplier list.

---

## Screen 3 — The split (hero)

**Job in the journey.** The “at a glance” moment. This is the product.

**User sees (one screen, two money columns)**

| In-chain — can count toward the target | Outside the chain — will not |
|---|---|
| **Tier-1 rows** with in-chain actions (material, energy, **enabling** PCF) | **Actions**, not suppliers: residual BVCM / credits, labeled as contribution |

Plus a **header bar** that always shows:
- Budget €X
- Suggested split: €A in-chain / €C outside-chain / € unallocated
- If gap exists: “this in-chain package is in the right *direction* for the gap; tonnes are ranges, not a booked reduction”
- If no gap: “leverage-only mode”

Each **left-column row is a tier-1 supplier** (not a T2 company). On the row:
- Name, spend, material chip, **star rating or `?`**
- **Confidence** (low / medium / high) — drives whether in-chain actions may be described as reductions vs enabling-only. Does not move the row to the right column.
- Suggested in-chain € (editable later in the drawer)
- One-line why, including the classification: *In-chain because it changes steel we already buy from this T1; no PCF → enabling only.*
- Right column is **not** that supplier duplicated; it is residual contribution for the gap the in-chain package will not close this year

**Criticality stars** constrain switching vs engaging in place. They do **not** get their own euro column.  
**Reputation / PR** does not appear.

**User does**
- Scans the two columns and the header split
- Opens a T1 row (in-chain actions) or the residual BVCM line (outside-chain actions) → Screen 3a
- Optionally expands “probable upstream” on the top few T1 rows (Screen 3b)
- Does **not** have to finish 3b to use 3a or go to Screen 4
- May override a card’s column only via the flagged control on the card

**Must not show**
- A single mixed leaderboard of “best practice insetting and offsetting”
- Named hypothetical tier-2 companies as if known
- “Risk-reputation €” as a third pile
- The same supplier sitting in both columns as if the *company* were outside the chain

**Empty / edge**
- All confidence low → in-chain column is mostly *enabling* (PCF, engagement), not “tCO2e reduced”
- ★★★★★ + low confidence → recommend enabling or park reductions; do not recommend switching away the qualified mill as a default
- Budget smaller than sum of suggestions → header shows over-alloc; user must cut on Screen 3a / 4

**Done when.** User understands the proposed split well enough to open rows or go write the brief. Value even if they stop here.

---

## Screen 3a — Action drawer (same page)

**Job in the journey.** Turn an action into fund / park / reject. Not a new wizard step.

**User sees**
- Open a **T1 row** → in-chain actions for that supplier only (lower-carbon grade, supplier energy via PCF, pay for PCF marked *enabling*). The drawer states *why this is in-chain* (rule 2: changes goods we already buy / booked as PCF, not as a credit).
- Open the **residual BVCM line** → outside-chain actions only (credits / contribution). The drawer states *why this is outside-chain* (rule 1 or 3: credit retirement or no link to sourced volumes).
- Do **not** put both lists on every supplier. A T1 is not “outside the chain.”
- Each action card:
  - Classification line (which rule fired) → evidence → assumption
  - Target-relevant: yes only if in-chain *and* not merely enabling
  - € suggested, tCO2e **range** (hidden or “n/a” on enabling), years to impact, confidence
  - “What would have to be true”
  - Override column only via a flagged control (lands on the brief as an assumption)
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
- Classify by impact, stars, or “best practice” instead of the boundary test

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
4. Criticality was stars (or `?`); PR/reputation was not a budget line.
5. Tier-2 names were not required and may be entirely wrong without breaking the brief.
