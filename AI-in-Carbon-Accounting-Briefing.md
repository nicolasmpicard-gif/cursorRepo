# What Role Should AI Play in Carbon Accounting — and for What Purpose?

*Research briefing · September 2026*

---

## 1. What "AI in carbon accounting" actually means

The methodology has not changed. It is still the GHG Protocol, still Scope 1/2/3, still CO₂e. What AI changes is **who does the grunt work between the source document and the disclosure**. The term covers four distinct layers, and conflating them is the main source of confusion:

| Layer | What AI does | Maturity |
|---|---|---|
| **Capture** | OCR and LLM parsing of utility bills, fuel receipts, freight invoices, supplier PDFs; connectors into ERP, procurement, travel, HR | Production-grade |
| **Mapping** | Matching thousands of activity/spend lines to the right emission factor or LCI process; unit and geography harmonisation | Works, but error-prone |
| **Estimation** | Gap-filling, proxy selection, anomaly detection, supplier-data enrichment | Useful, needs governance |
| **Narrative** | Drafting disclosures; pushing one dataset into ESRS, IFRS S2, CDP and CBAM at once | Fast, highest greenwashing risk |

A fifth, newer sense is AI as the **subject** of carbon accounting — measuring the emissions of the company's own AI usage. That is genuinely unsolved (§5).

The purpose, correctly framed, is not to have AI produce the number. It is to compress the data-janitorial work so that scarce expert judgement goes to boundaries, materiality, assumptions and reduction decisions.

## 2. Who is doing this today

- **Watershed** — the clearest agent-first play: agents for ingestion, cleaning, anomaly detection, analysis and report drafting, plus expert-built "skills" (methodology comparison, YoY root-cause). Claims 65–80% time savings on data cleaning.
- **Persefoni** — finance-grade positioning: Copilot, anomaly detection on million-row datasets, natural-language factor mapping, strong on PCAF/financed emissions.
- **Sweep, Normative, CO2 AI, Net0, Plan A** — AI-assisted mapping, supplier engagement, multi-framework disclosure. Normative launched an AI-driven SKU-level PCF product in 2026 for CSRD/CBAM; Net0 markets 10,000+ connectors against 50,000+ factors.
- **Climatiq** — the infrastructure layer: an API that AI-selects the best-fitting factor with documented region/year fallback logic, embedded inside other ERP and ESG products.
- **Incumbents** — IBM Envizi, Microsoft Sustainability Manager, SAP Sustainability Footprint Management, embedding the same capabilities into systems companies already own.

## 3. Trends and projections

**Market.** Analysts put carbon accounting software at **$27.5–27.8bn in 2026 rising to ~$63.5bn by 2030** (≈23% CAGR); the narrower "AI carbon footprint management" segment at **$2.17bn in 2026 → $5.56bn by 2031**. Treat these directionally — definitions differ between houses and the reports are commercially produced.

**Regulation just moved.** EU **Omnibus I** (Directive (EU) 2026/470, in force February 2026) cut CSRD scope to companies above **both** €450m turnover and 1,000 employees from FY2027, first reports in 2028, non-EU groups 2029. Fewer filers, but each reporting under simplified ESRS 2.0 with assurance attached. In the US, **California SB 253** Scope 1 and 2 reports are due **10 November 2026** under enforcement discretion.

**Assurance arrives next.** **ISSA 5000** applies to periods beginning on or after **15 December 2026**, requiring practitioners to evaluate the reliability of entity-produced information and obtain evidence of its accuracy and completeness — precisely where an opaque AI pipeline fails. The IAASB added AI questions in sustainability assurance to its Technology Catalog in 2026.

**The methodology floor is moving too.** GHG Protocol and ISO are consolidating the Corporate, Scope 2, Scope 3 and Actions & Market Instruments workstreams with ISO 14064-1 into one co-branded standard: consultation **Q2 2027**, publication targeted **Q4 2028**. Tooling bought today must survive that rewrite.

## 4. Advantages in practice

1. **Throughput on the actual bottleneck.** Scope 3 line-item mapping and unstructured-document extraction are the real constraints, and they are classification tasks rather than judgement — which is why the reported 65–80% time reductions are credible.
2. **Continuous rather than annual.** Near-real-time capture means emissions data arrives early enough to influence procurement and operations, not just to be reported.
3. **Error detection at inhuman scale.** Anomaly detection across millions of rows catches double-counting, unit errors and missing meters before an auditor does.
4. **One dataset, many frameworks.** Mapping a single inventory into ESRS, IFRS S2, CDP and CBAM removes weeks of reformatting and inter-disclosure inconsistency.
5. **Emissions joined to spend.** Analysing CO₂e alongside financial data turns sustainability work into a cost-savings argument — the thing that keeps budget attached to it.

## 5. Issues and disadvantages in practice

**The accuracy evidence is sobering, and it is now measured rather than asserted.**

- **PCFBench** (2026; 614 expert-labelled items, eight frontier LLMs): the best models land within 2× of declared product totals for 77% of products — but step-by-step accuracy falls to **37–58%**, and only **45–75%** of outputs obey mass conservation. Scoring totals alone hides errors that cancel out.
- A **467-question emission-factor benchmark** across five frontier models found **43–65% unaided accuracy**, and models named the **correct publisher alongside a wrong number in up to 58% of cases**. That is the failure that survives review: a wrong number wearing DEFRA's name.
- **FAULDIER**, an LLM-assisted LCI mapping framework, reached ~57% process/flow mapping accuracy with hallucinated and run-to-run inconsistent mappings.

**Beyond accuracy:**

- **New greenwashing vectors** — hallucinated figures, stale factor versions baked into model weights, optimistic scenarios presented as base case, and hardest to catch, fabricated citations to *real* standards with invented paragraph numbers.
- **Automation complacency.** In a 2026 experiment, well-trained preparers using generative AI produced vague, unspecific reports and only recognised it on later reflection; they skipped the quality checks the workflow assumed.
- **AI's own footprint.** The IEA projects data centre electricity roughly doubling from **485 TWh in 2025 to ~950 TWh in 2030** (~3% of global demand), AI-focused capacity tripling, and associated emissions near 350 Mt CO₂ by 2035.
- **Accounting for your own AI use is unstandardised.** Per-query estimates differ by orders of magnitude, and the common fallback — a generic ICT-sector EEIO spend factor — **overstates AI inference emissions by 10–40×** versus physical methods. Only one frontier provider publishes per-prompt figures, and only as a fleet-wide median.

## 6. Why this is pressing for carbon accountants

Three deadlines converge inside twelve months: SB 253 filings in November 2026; ISSA 5000 for periods beginning December 2026, the first cycle in which an assurance provider formally tests whether your data is reliable, accurate and complete; and the GHG Protocol–ISO consultation in Q2 2027.

Meanwhile the workload has not shrunk for those still in scope. Omnibus I removed filers, not Scope 3, and the companies remaining are the ones with the most complex value chains. The indirect pull matters too: in-scope companies now demand data from suppliers with no reporting obligation of their own, dragging smaller organisations into the market ahead of their own deadlines.

The risk is asymmetric. A team that refuses AI will miss deadlines or burn expert capacity on invoice transcription. A team that adopts it naively will sign off on numbers it cannot defend, under a standard that now makes someone personally accountable for them.

## 7. What is preventing progress or clarity

- **No agreed definition of "AI-assisted" in an inventory.** ISSA 5000 tells auditors to evaluate reliability; it does not describe an acceptable AI control environment. Every firm is improvising.
- **Vendor claims are unfalsifiable.** "AI-powered emission factor matching" is marketed without published accuracy rates, evaluation method or error bars, so buyers cannot compare.
- **Benchmarks exist but nobody demands them.** PCFBench and the factor benchmarks appeared in 2026; no regulator, assurance provider or procurement process yet requires vendors to report against them.
- **A moving methodology floor.** With the consolidated standard not final until late 2028, factor libraries, Scope 2 treatment and Scope 3 category rules are provisionally correct at best.
- **Structural opacity upstream, and a skills gap downstream.** Cloud and model providers withhold the energy and grid-mix data needed to account for AI workloads. And the reviewer who can catch "right publisher, wrong number" — fluent in both inventories and models — is rare.

## 8. Four things that would move this forward

**1. Mandate retrieval, prohibit recall.** The highest-leverage control available. In the 467-question benchmark, giving models a sourced factor-lookup tool moved accuracy from 38–50% to **98.7–100%**, with large errors falling to ~1% or zero. Policy: no emission factor enters an inventory from a model's weights — only from a versioned, cited database lookup. Cheap, testable, immediately auditable.

**2. Make data lineage a procurement gate, not a feature.** Require every figure to trace to a source document, a named factor with its version, and an approval chain. If a vendor cannot produce that trail for an arbitrary line item during evaluation, it is a black box and assurance will reject it. Pair with an ISSA 5000-mapped control set: immutable logs, prompt and model versioning, a rule that AI never decides materiality, and a named human sign-off per disclosure.

**3. Evaluate step-wise, and publish the results.** Totals hide cancelling errors — 77% accuracy on totals collapsed to 37–58% on intermediate steps. Industry bodies should require vendors to publish per-task accuracy against open benchmarks. Internally, run a labelled sample of your own line items through any tool before trusting it at scale.

**4. Bring AI use inside the inventory.** Adopt a tiered method now: provider-reported figures where they exist, token- and GPU-benchmark physical estimation next, spend-based EEIO only as a last resort with an explicit note that it can overstate by 10–40×. Doing this early gives the profession standing to demand better provider disclosure, and avoids an unmeasured, fast-growing line item.

## 9. Three free, in-depth reads

1. **PCFBench: A Diagnostic Benchmark for Product Carbon Footprint Estimation** (arXiv:2608.27716, Aug 2026) — [arxiv.org/abs/2608.27716](https://arxiv.org/abs/2608.27716). The best single source on where AI breaks in carbon work: 614 expert-labelled items across six decomposed tasks, eight frontier models, dataset and evaluation harness released openly. Read before believing any vendor accuracy claim.

2. **IEA, *Key Questions on Energy and AI*** (16 April 2026) — [iea.org/reports/key-questions-on-energy-and-ai](https://www.iea.org/reports/key-questions-on-energy-and-ai). Free and CC BY 4.0; the authoritative non-commercial account of AI's own energy and emissions trajectory. Essential for the "is the cure worse than the disease" question.

3. **Estimating GHG Emissions from AI Use: Framework for Corporate-Level Measurement** (arXiv:2608.06733, Aug 2026) — [arxiv.org/abs/2608.06733](https://arxiv.org/abs/2608.06733). A tiered, openly published methodology for putting corporate AI usage into an inventory, honest about data constraints and the unresolved Scope 2 debate it inherits. The most directly actionable of the three.

*Worth a look, with a caveat:* **"How Accurate Is AI on Emission Factors? 467 Tested"** ([greencalculus.com/guides/ai-emission-factors-accuracy](https://greencalculus.com/guides/ai-emission-factors-accuracy/)), dataset public on Hugging Face and Zenodo. The retrieval-versus-recall finding is the most useful practical result here, but it is published by a factor-data vendor whose product the conclusion favours — read it as a reproducible experiment, not neutral analysis.
