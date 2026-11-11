# Upvest interview brief

Senior Solutions Consultant, Pre-Sales. Prepared for Nicolas Picard from the job description, the October 2026 CV, and public sources through 6 November 2026 (Europe/Berlin).

**Second interview: about 45%** if you are already in a first round and you prepare the investment stack. **About 30%** that the CV alone produces that first conversation. From a cold application, those compound to roughly 15%.

The profile matches how this job is done, and it misses what the job is about. You can run discovery, a workshop, and a scoped proposal. You have done that at enterprise scale once, on the $23 million Oracle Utilities deal, and that role ended in 2017. The job description marks investment experience as essential. AstroFinance is the only recent investment work, and it is private aerospace assets, SPVs, and tokenised revenue rights.

---

## What this role is selling

Upvest is the regulated investment stack behind someone else's app. Banks, brokers, wealth managers, and fintechs keep the customer relationship and the interface. Upvest runs brokerage, settlement, custody, and most of the middle and back office through one Investment API. The Solutions Consultant owns discovery, the workshop, the architecture, and the proposal, then hands a scoped, compliant design to the client launch team.

| Figure | What to quote |
| --- | --- |
| €280 million | Capital raised, company FAQ and the job description |
| 100 million+ | Orders processed in 2025, up from 20 million in 2024 |
| 30+ | Institutional clients. The homepage has also shown 40+. Quote 30+. |
| 280 | People as of December 2025. The job description says 270+. |
| 20+ | Markets served |

Client reach (Revolut, N26, DKB) is not the same thing as accounts held at Upvest. Do not quote "2 million end users" from the marketing homepage.

---

## Product offering

Upvest is a B2B investment-infrastructure company, founded in Berlin in 2017. It is not a consumer broker. A client embeds fractions, savings plans, portfolios, or a local pension wrapper in its own product. Upvest is supervised by BaFin and the FCA, passported across the EU, with branches in France, Spain, and Austria, and hubs in Berlin, London, and Tallinn.

The current public universe is stocks, ETFs, mutual funds, money market funds, ELTIFs, securitised derivatives, and bonds, in EUR, USD, and GBP, across 100,000+ instruments. Crypto is listed as coming soon. The June 2022 Series B post said crypto brokerage and custody were in market. The current FAQ has moved crypto back to the roadmap. Do not describe crypto as live.

Connectivity named on the product page includes Tradegate, Quotrix, Börse Stuttgart, Vestima, JP Morgan, and CATs-OS. Order types are market, limit, and stop, straight-through or blocked. Fractions start at €1, £1, or $1, at up to 10 decimal places. The company is explicit that they are real property: co-ownership under German law (BGB section 741), with insolvency protection, and UK assets under the CASS regime. Historical uptime is stated as above 99.99%. The company says it automates more than 99% of middle- and back-office processing, including corporate actions, tax, reconciliation, and regulatory reporting. Sandbox and live environments exist. Webhooks are live. Kafka streams are described as coming.

### Three operating models

The first discovery question in this job is which of these three the prospect is. The operating-model page assigns a live logo to each. DKB, Openbank, IG, and CMC Markets are not publicly assigned to a model. Do not guess one in the room.

| Model | Who faces the end user | What the client still owns | Live example |
| --- | --- | --- | --- |
| Take-our-licence, single accounts | Both. Upvest is on the custody and execution contract and relies on the client's KYC. | The app, support, and reception-and-transmission of orders. Upvest can also offer a tied-agent umbrella. | N26. Stocks and ETFs, then a French PEA, on Upvest licences and Upvest operations. |
| Bring-your-own-licence, single accounts | The client. Upvest is sub-custodian and executing broker. | The licences and the customer relationship. Upvest still runs accounts, tax, corporate actions, and the middle and back office. | Raisin. Own licences, outsourced investment functionality, model portfolios. |
| Bring-your-own-licence, omnibus | The client. | The sub-ledger: accounts, tax wrappers, reporting, portfolios. Upvest provides fractional execution, settlement, custody at omnibus level, and B2B corporate-action information. | Revolut. Own investment-firm licences, European fractional stocks and ETFs, robo-advisor on top. |

---

## Business model

Revenue is enterprise and quote-based. The FAQ says pricing is tailored to product scope and does not publish a rate card. The economic logic of the stack, which is not a disclosed price list, is four layers a contract can contain:

1. Access to the API and an operating model.
2. Usage that scales with orders and assets.
3. Outsourced middle- and back-office work.
4. On Take-our-licence deals, the use of Upvest's own BaFin and FCA permissions.

The fee types in the developer docs are what the client charges its own customers, not what Upvest charges the client. Those are an ongoing service fee as a percentage of assets, and a per-order transaction fee. Openbank told the market it would charge end users 0.20% per trade with a €1 minimum and no custody fee, and described that price as a saving passed on from the infrastructure. That is a client outcome, not Upvest's price.

There is no public revenue, margin, or assets-under-administration figure. Two company statements are worth knowing and worth sourcing if you repeat them.

- At the December 2024 Series C, Upvest said revenue had grown 25% a month on average that year. Do not annualise that number. It is unaudited, and it was a launch-year growth rate.
- In October 2025, Martin Kassing told Börsen-Zeitung he expected the company to be profitable in 2027, possibly sooner, depending on how hard they keep investing. He declined to give current assets. He said the ambition is several hundred billion euros on the platform by the end of 2030. In May 2025 he told Maddyness he expected to cross €100 billion in assets and trading volume over the following few years on the back of contracts already signed.
- The one hard asset number in a case study is Raisin: a single-digit billion, migrated in a weekend.

---

## Ownership, shareholders, and financial performance

The company is still founder-run.

- Martin Kassing, CEO and co-founder. Private equity investing in financial software, then ShopCo (later with Klarna), Finleap, and Upvest.
- Tobias Auferoth, managing director and co-founder.
- Dr. Til Rochow, CPO and co-founder. Notion's profile says he joined to lead product in December 2020, so he is not a day-one founder.

The about page also lists Sebastien Jeanquier (CSO), Jonathan Brander (COO), Roberto Fajardo (CTO), Quiron Cunha (CFO), Symmie Swil (UK GM), and Jens Maluck (VP Client Impact). Jeanquier is the sales seat this role partners with. Client Impact is the closest public name to the launch team a pursuit hands over to.

The early product was a blockchain custody and digital-assets API. By the 2020 Series A the story had become a pan-European securities API, with a plan to add a German brokerage-bank licence. That pivot is the company story. The current product is regulated securities infrastructure.

| Round | When | Amount | Lead | What it funded |
| --- | --- | --- | --- | --- |
| Seed | 2017 | Undisclosed | HV Capital | Berlin founding. HV's portfolio page says it led the seed. |
| Series A | Mid-2020 | €7 million | Notion, HV, Partech | Securities API. Early customers included Bitwala and Exporo. |
| Series A+ | Dec 2020 | €5 million more, €12 million total | Earlybird | Angels included the founders of N26, IDnow, and Consorsbank. Path to a brokerage-bank licence. |
| Series B | 16 Jun 2022 | $42 million | Bessemer | BaFin securities and crypto licences already in hand. Earlybird, ABN AMRO Ventures, Notion, Partech, 10x, and Speedinvest participated. |
| Series C | 12 Dec 2024 | €100 million | Hedosophia, co-led by Sapphire | UK push after FCA authorisation. About 170 people. 20 million orders that year. Bessemer, BlackRock, Earlybird, HV, Motive, and Notion followed on. |
| Growth round | 17 Mar 2026 | See note | Sapphire and Tencent | Pensions (Altersvorsorgedepot, SIPPs) and AI-supported wealth. Bessemer and BlackRock again. Existing investors only. |

The March 2026 round is the same deal described three ways. The English company post says $125 million: $90 million of equity plus a $35 million debt facility that was still being finalised. The about page and this job description say €105 million. Handelsblatt reported €105 million, of which about €35 million was debt. Börsen-Zeitung reported €108 million, roughly €80 million equity and a €30 million credit line. HV Capital's portfolio page says €125 million. In the room, use the job description's figures: a €105 million round and €280 million raised in total.

Valuation was not disclosed by the company. The Next Web reported €640 million on 17 March 2026, nearly double a €360 million figure it attributed to the December 2024 round. Handelsblatt and Börsen-Zeitung reported only that it had risen into the high hundreds of millions of euros. Repeat the range, and name the source if you cite €640 million. Kassing also told Börsen-Zeitung that an IPO around 2030 is an option, alongside further equity or debt, and that nothing is decided.

Operating proof points, all company-stated:

- Orders went from 20 million in 2024 to more than 100 million in 2025, a fivefold increase. The March 2026 post says orders were still growing at a double-digit monthly rate, for more than 30 financial institutions.
- In May 2025 Kassing said the book was above 2 million orders a week and that he planned to triple that rate by year-end.
- Headcount went from about 170 at the Series C to over 280 by December 2025, across 70+ nationalities.
- Markets served crossed 20 during 2025.

---

## USP

The differentiation is not "we have an API." DriveWealth, Alpaca, and Apex have APIs. FNZ, Seccl, and WealthKernel sell investment operations in Europe. DWP Bank and Baader Bank are the German incumbents a direct bank already knows. Upvest's claim is the combination below. The incumbent proof point is DKB leaving DWP Bank.

| Claim | Proof you can cite | How to say it |
| --- | --- | --- |
| One regulated stack | Brokerage, settlement, custody, and middle/back office on one API. Above 99% of those processes automated. Above 99.99% historical uptime. | You stop stitching together a broker, a custodian, a tax engine, and a corporate-actions vendor. |
| Real fractions, not a synthetic exposure | German co-ownership under BGB §741, insolvency protection, UK assets under CASS. Up to 10 decimal places. From €1. | The end user owns the fraction. This is not a CFD and not an IOU. |
| The licence is a product choice | N26 on Take-our-licence. Raisin on Bring-your-own-licence, single accounts. Revolut on Bring-your-own-licence, omnibus. | We fit the licence you already have, or we bring one and get you live faster. |
| Local wrappers are the product | PEA live with N26. UK ISA, JISA, and SIPP. German Altersvorsorgedepot and Frühstart-Rente. Spanish traspasos. | The hard part of European investing is tax and product law. That is what the 2026 round is for. |
| They can migrate a book | Raisin moved a single-digit billion in a weekend. The company says zero issues. DKB is the prestige version: a large direct bank replacing its securities servicer. | Greenfield in months, or an existing depot book moved without a public outage. |
| European market structure | BaFin, FCA, EU passport, local venues, local tax including FTT and stamp duty, MiFIR trade reporting. | A US brokerage API is the wrong answer for a German depot, a PEA, or BaFin custody. |

---

## Company timeline

| When | What happened |
| --- | --- |
| 2017 | Founded in Berlin. HV Capital leads the seed. Early thesis is blockchain and digital assets. Kassing had just been CPO at Finleap. |
| 2019 | Notion Capital's first investment, per its portfolio page. |
| Mid-2020 | €7 million Series A. Securities API. Bitwala and Exporo are named customers, with €100 million+ of transaction volume claimed at the time. |
| Dec 2020 | Earlybird adds €5 million. Founders of N26, IDnow, and Consorsbank come in as angels. Plan to become a Wertpapierhandelsbank. Til Rochow joins. |
| 2022 | BaFin licences. 16 June: $42 million Series B led by Bessemer. Product described as live for ETFs, stocks, and crypto. |
| 2024 | FCA authorisation. 20 million orders, and the company says revenue grew 25% a month on average. 12 December: €100 million Series C. About 170 people. Clients named: Revolut, Raisin, N26, bunq. Revolut's robo-advisor goes live in February on the API. |
| 2025 | London office, the third hub. 20 markets, 250+ people, 70+ nationalities, 100 million orders. New names: DKB, Openbank, VisualVest, Salt Bank, Xaver, LIQID, IG, Webull UK, Zopa. N26 PEA in France. UK ISAs. ELTIFs added. |
| 9 Sep 2025 | DKB partnership announced. Upvest replaces DWP Bank. Target is a fully digital securities platform for 5.9 million end users by the end of 2026, including amount-based orders, fractions, and later children's and retirement accounts. |
| 21 Oct 2025 | Kassing tells Börsen-Zeitung: DKB has 5 million+ customers and about 860,000 securities accounts; cost per trade matters; he wants Frühstart-Rente and Altersvorsorgedepot live at the start of the year; profitability aimed at 2027; IPO is an option around 2030; several hundred billion euros of assets by end-2030. |
| 17 Mar 2026 | Sapphire and Tencent lead the new round. Use of proceeds: local pension products and AI-supported, programmable advice. About page labels it €105 million. English post labels it $125 million. |
| 14 Apr 2026 | CMC Markets will launch multi-currency stocks, ETFs, and mutual funds in Germany from autumn 2026, as the template for a wider European rollout and later pension wrappers. |
| Nov 2026 | Pensions and AI wealth are the stated growth bets. Crypto is "coming soon" on the public site. |

---

## Customer segments

| Segment | What they buy | Names |
| --- | --- | --- |
| Fintechs and neobanks | A brokerage they can launch in months, often on Upvest's licence, inside an app people already use for spending. | N26, Revolut, bunq, Salt Bank |
| Banks, especially direct and digital banks | A replacement for a legacy securities servicer. The business case is cost per trade, a modern depot, and speed to a new feature. | DKB, Openbank (Santander) |
| Brokers | Cash securities, multi-currency, and later a tax wrapper, added to an existing trading franchise. | IG, CMC Markets, Webull |
| Wealth managers and digital wealth | Model portfolios, robo, direct ETF trading, and a migration of assets already on a book. | Raisin, VisualVest (Union Investment), LIQID, Xaver |

---

## Ideal customer profile

A European or UK financial institution that already has distribution — an app, a brand, deposits, or a brokerage franchise — and wants investing as a product rather than a multi-year build. They are blocked by a legacy custodian, a pile of vendors, or the time it would take to get a licence and build ledger, tax, and corporate actions themselves. They want fractions, savings plans, portfolios, or a local wrapper (PEA, ISA, SIPP, Altersvorsorgedepot), and they can put a real book behind it: a neobank with millions of users, a direct bank with hundreds of thousands of depots, or a wealth platform with billions already invested. Their licence position maps cleanly onto Take-our-licence or Bring-your-own-licence.

The buying group is the head of investments or brokerage, the CTO or head of engineering, operations, compliance, and often the CFO, because the case is cost per trade and time to market. Sales owns the relationship. This role owns the technical thread across that group.

A poor fit is a retail consumer, a pre-distribution startup that needs a licence and a customer base, a US-only equity app, or a crypto-native exchange. Crypto is on the roadmap, not the product you would lead with. A firm that wants a cheap market-data or FIX line and intends to keep the full stack in-house is a Bring-your-own-licence omnibus conversation at best, and often not a deal.

---

## Named existing customers

Headcount and user counts below belong to the client, not to accounts custodied at Upvest, unless the line says otherwise.

| Client | What is public |
| --- | --- |
| Revolut | Bring-your-own-licence, omnibus. ETFs and fractional European stocks, about three months to an EU go-live, 5,000+ instruments, 80% of orders fractional. Robo-advisor in February 2024. Success page cites 45 million Revolut retail customers. |
| N26 | Take-our-licence, single accounts. Stocks and ETFs, Austria in six months, then Germany, Ireland, the Netherlands, France, and Spain. 25+ features since go-live. French PEA powered by the API, which Upvest says launched in weeks. |
| DKB | Announced 9 September 2025. Replaces DWP Bank. Digital securities platform aimed at 5.9 million end users by the end of 2026. Kassing: 5 million+ customers, about 860,000 securities accounts today. Fractions, amount-based orders, later children's and retirement accounts. |
| Raisin | Bring-your-own-licence, single accounts. Robo-advisor and model portfolios. Single-digit billion in assets migrated over one weekend. Company says zero issues. 1 million+ end users on Raisin's platform. |
| Openbank (Santander) | End-to-end brokerage, settlement, custody, and compliance via one API. Openbank described itself as Europe's largest fully digital bank by deposits, 2 million+ end users, and priced retail trades at 0.20% with a €1 minimum and no custody fee. |
| bunq | Named as a client since at least the December 2024 Series C. No public scope of the integration. |
| Webull | Named among current fintech clients. The 2025 review specifically pairs Webull UK with the new London office. |
| Zopa | Named in the 2025 review as a UK partner alongside Webull UK. Scope not public. |
| VisualVest | Union Investment subsidiary. October 2025: SelectETF, a curated list of about 200 ETFs, traded in the VisualVest app on Upvest trading, settlement, and custody. Sits next to their existing robo. |
| Salt Bank | 14 October 2025. Romania's digital bank, backed by Banca Transilvania, 500,000+ end users after about a year. First securities offering, inside the banking app. |
| IG | 18 November 2025. Stock and ETF trading in France, described as the first step of a European rollout. |
| CMC Markets | 14 April 2026. Multi-currency stocks, ETFs, and mutual funds in GBP, EUR, and USD for Germany, launch planned for autumn 2026, then a wider European template and pension wrappers. CMC Markets Germany is BaFin-regulated; the group is London-listed. |
| LIQID and Xaver | Both named in the 2025 review as new partners. No public case study. Do not invent the product scope. |
| Bitwala and Exporo | Named in December 2020 as early API customers. Treat them as history, not as the current book. |

---

## Products and solutions

| Product | One line |
| --- | --- |
| Investment API | One integration for accounts, orders, portfolios, savings plans, corporate actions, tax, and reporting. |
| Take-our-licence | Upvest's BaFin and FCA permissions and full end-user operations, for a firm that wants speed over holding the custody contract. |
| Bring-your-own-licence | The client's own permissions and customer contract, with Upvest as executing broker and sub-custodian, in single-account or omnibus depth. |
| Brokerage | Market, limit, and stop orders, straight-through or blocked, across Tradegate, Quotrix, Stuttgart, Vestima, JP Morgan, and CATs-OS. |
| Real fractional investing | From €1, £1, or $1, up to 10 decimal places, with real co-ownership rather than a synthetic line. |
| Savings and withdrawal plans | Recurring buys and sells, executed through the API. |
| Portfolio engine | Model portfolios, time- and threshold-based rebalancing, post-tax orders, and direct indexing up to 1,000 instruments. |
| Settlement | Pre-funded Upvest cash accounts or post-trade settlement against the client's own cash, with netted clearing and securities transfers. |
| Custody | Individual, joint, child, and business accounts, or omnibus when the client keeps the sub-ledger. |
| Tax and regulatory reporting | Withholding, local wrappers, financial transaction tax, stamp duty, and MiFID / MiFIR reporting, including MiFIR Article 26. |
| Corporate actions | Dividends, splits, mergers, voluntary elections, proxy voting, and digital AGM entry cards. |
| Pension and tax wrappers | UK ISA, JISA, and SIPP. German Altersvorsorgedepot and Frühstart-Rente. French PEA. Spanish traspasos. |
| Market and performance data | Instruments, prices, valuations, and time-weighted returns, which the client can enrich. |
| Fees engine | Lets the client configure transaction fees and assets-under-management service fees for its own end users. |
| Upfront | The operations console for the cases automation does not cover. The company says over 99% of support requests can be automated. |
| AI-supported advice | 2026 roadmap: recommendations alongside human advice, and programmable execution for more personalised portfolios. Company claim, not a case study yet. |

---

## Recent leadership interviews

### Börsen-Zeitung — Björn Godenrath, 21 October 2025

> "With more than five million customers, DKB currently has a good 860,000 securities accounts and now wants to expand its stock and investment business."

Kassing adds that cost per trade is part of why DKB moved off DWP Bank, and that Upvest wants children's accounts for the Frühstart-Rente and the Altersvorsorgedepot live at the start of the year, with ELTIFs eligible inside the tax wrapper. He aims at profitability in 2027, leaves an IPO open around 2030, and says the ambition is several hundred billion euros of assets by the end of 2030. He would not give today's assets.

Use this for the bank segment. The buyer is a direct bank losing money, or losing the product, on a legacy securities servicer. The German original ran on 21 October 2025. The English version ran on 3 November 2025.

### Maddyness — Quick Founder Questions, 7 May 2025

> "Banks are not particularly well set-up to develop and manage high-performing software. Fintechs often face challenges securing the regulatory oversight they need to launch and scale."

That is his one-sentence origin story. He also said the company was above 2 million orders a week and expected to cross €100 billion of assets and trading volume on signed contracts. He said the UK had 13 million adults holding £430 billion in cash that could be invested. Scaling, and hiring "Upvengers," was the current hard problem. His Wednesdays are for clients and partners. Culture, in his words: ambitious, exceptionally smart, and kind.

Use this for "why Upvest exists" and for the UK motion. He still takes client meetings himself.

### Handelsblatt — Dennis Schwarz, 17 March 2026

> "With this round we want to grow faster internationally and extend the product platform."

Kassing told Handelsblatt the company was already well funded and that demand was the reason to raise. They kept the round to existing investors, Sapphire and Tencent largest among them, so they would not get distracted from the core business. Valuation, per financial circles quoted in the piece: a high triple-digit million euro number, up from the December 2024 round.

Use this if they ask why the company raised again fifteen months after a €100 million Series C. The answer he gave is demand and focus. German business press did not confirm the €640 million figure that The Next Web reported the same day.

---

## Questions they will ask

Have three stories and one diagram ready.

- Oracle, the $23 million utilities deal: who was in the room, what was ambiguous, what you wrote.
- OpenSC and Nespresso: multi-party discovery, a business case, a handover.
- AstroFinance: seven workshops with investment professionals, and a clear line on what does not transfer to brokerage.
- The diagram: client app, then order, then venue, then settlement, then custody, then tax and corporate actions, with a label for which operating model you assumed.

### Why this seat, why now

| Question | What a prepared answer does |
| --- | --- |
| Why Upvest, and why a solutions role rather than the product roles on your CV? | They will hear a product person trying on a sales title unless you choose the pre-sales craft on purpose. Oracle is the evidence. AstroFinance is the detour. |
| What have you been doing since AstroFinance ended in June 2026? | The CV stops in June and this interview is November. Have one plain sentence. |
| Say what Upvest sells, in one sentence, to a bank that already has a custodian. | A regulated brokerage, settlement, and custody stack that replaces or sits under the incumbent, at a lower cost per trade and a faster path to fractions, portfolios, and local wrappers. |

### The investment stack

| Question | What a prepared answer does |
| --- | --- |
| A licensed European broker wants fractional stocks and a savings plan, and will not put Upvest on the customer contract. Which operating model, and what do they still have to build? | Bring-your-own-licence. Single accounts if they want Upvest to run tax, reporting, and corporate actions. Omnibus if they insist on keeping the sub-ledger. Revolut is the omnibus proof point. |
| What is the difference between a real fractional share, a CFD, and a synthetic fraction, and why does DKB's legal team care? | Real fractions here are co-ownership under German law, insolvency-remote, with UK assets under CASS. Do not answer with tokenisation. |
| What is a PEA, why is it hard, and what would you need to learn before you promised N26-style timing? | France is a live motion: N26's PEA, IG's French launch, an Upvest branch. Native French is an asset if you can talk about eligibility, contribution limits, and tax reporting. |
| Walk a savings plan from the end user's standing instruction to settlement. Where do tax and a corporate action touch it? | Order lifecycle, cash (pre-fund versus post-trade), custody, and the fact that a dividend or a split has to land on a fractional position. |
| A prospect leads with crypto. Where is crypto in the current product? | Coming soon, on the current FAQ. It was live in the 2022 messaging. |

### How you run a pursuit

| Question | What a prepared answer does |
| --- | --- |
| Take the $23 million Oracle deal. Who was in the room, what was the scope fight, and what did you personally produce? | Requirements from engineering and the business, the boundary of the API and data-workflow scope, and how that became a price. "Partnered with sales" is not an answer. |
| Tell me about a workshop that changed a deal. What did you cut when the room turned technical? | AstroFinance gives you seven workshops. OpenSC gives you a coffee trader and three teams. They want the edit you made for the audience. |
| Your last closed number in the investment world is about $56,000. Our buyers are DKB, Revolut, IG, and CMC. How should I think about that jump? | Do not inflate AstroFinance. Bridge with Oracle's enterprise cycle, then say what was different about a regulated infrastructure sale: legal, ops, and a launch team. |
| Sales owns the relationship, and the buyer will not give you engineering time until late. How do you run discovery anyway? | You partner with sales and still own the technical thread. They want a way of working. |
| What do you hand to the client launch team, and when is a pursuit not ready to hand over? | Name the artifacts: scope, architecture, open regulatory points, what was promised. OpenSC is the closest thing you have to delivery. |

### Technical credibility

| Question | What a prepared answer does |
| --- | --- |
| Sketch the integration for a Take-our-licence launch. What does the client build, and which events does their engineering lead ask about first? | Client builds the app, support, and order handoff. Upvest builds accounts, execution, settlement, custody, tax, corporate actions. A credible engineer asks about webhooks, partial fills, idempotency, and the sandbox. |
| You specified a Dun & Bradstreet API used by 500+ enterprises. How is that different from specifying order, settlement, and corporate-action flows? | Use IntegrityNext for the craft (data contract, failure modes, who consumes it), then show you know a securities flow has a ledger, a cash leg, and a regulator. |
| An architect says they want omnibus "so they keep control." What do they take back in-house, and when is that the wrong recommendation? | They take accounts, tax wrappers, reporting, and portfolio logic. They keep Upvest for fractional execution and sub-custody. It is the wrong recommendation when they do not actually have that stack. N26 versus Revolut is the comparison. |

### The CV, under pressure

| Question | What a prepared answer does |
| --- | --- |
| IntegrityNext was four months. What happened? | Say it in one sentence. A short stint reads as a misfit until you name it. |
| You have been a pre-sales analyst, an implementation lead, a product manager, and a fractional head of product. Which parts of those jobs do you not want here? | Give away the product-owner parts. Keep discovery, shaping the solution, and the technical sale. |
| The headline says five-plus years of pre-sales. Count it with me. | Oracle is October 2015 to December 2017. OpenSC is implementation. AstroFinance is product. Restate it as enterprise pre-sales plus later client-facing consulting. Do not defend the headline literally. |
| German is B2. This team sells to DKB. How do you run a workshop with a German-speaking COO? | French is the language that meets the C1 line. Offer France, the PEA, and IG. For Germany, you can follow and contribute, and you would not lead a BaFin negotiation alone. Spanish B2 is a similar point for Openbank and traspasos. |
| Tell me about a requirement you sent back to product, and one you told the client they would not get. | The job asks you to carry client feedback into the roadmap and to hold the line on compliance. They want both directions. |

### A case they can run in the room

CMC Markets is a CFD business launching multi-currency securities in Germany, then pensions. You have 45 minutes with the Head of Europe and a solutions architect. What do you ask, and what do you refuse to decide?

This deal was announced in April 2026, so it is a fair prompt. Discover which licence CMC Germany already holds, whether cash stays at CMC, which of GBP, EUR, and USD is day one, whether fractions are in the first release, and what "pension" means in Germany versus a UK SIPP. Refuse to pick single-account versus omnibus before you know who keeps the sub-ledger and the tax wrapper.

### Five questions worth asking them

| Ask | Why it lands |
| --- | --- |
| Which operating model is winning new logos this year, and where do live pursuits actually stall? | Shows you know the product has three shapes, and that you care where deals die. |
| What does a clean handover to the client launch team contain, and which pre-sales promise most often breaks? | The job description ends at that handover. |
| How has the Altersvorsorgedepot changed the conversation with banks, as opposed to fintechs? | Ties the 2026 round to a live sales motion, and separates the two segments. |
| What share of a Senior Solutions Consultant's week is live pursuits versus the reusable proposal and architecture kit? | The job asks for both. You want to know which one they are actually hiring. |
| In DACH, France, and Spain, which language does the technical workshop run in? | Makes French a concrete offer and surfaces the German B2 question on your terms. |

---

## Chances of a second interview

| Gate | Chance | Condition |
| --- | --- | --- |
| First interview to a second round | About 45% | You prepare the stack, not a longer retelling of the CV. Toward 60% if the five points below land. Toward 20% if the first technical question misses. |
| Cold CV to a first conversation | About 30% | The headline, Berlin, and native French get it read. A recruiter scoring "five years of solutions consulting in investments" will bounce it. |
| Cold application to a second interview | About 15% | The two gates compound, until someone has actually met you. |

### How the job description reads against the CV

| What they asked for | What the CV shows | Read |
| --- | --- | --- |
| Investments experience, marked essential | AstroFinance, Feb 2025–Jun 2026: discovery with investment professionals, asset due diligence, SPV structuring, revenue-rights tokenisation, investor qualification. Not listed securities, custody, or wealth infrastructure. | Partial. This is the screen that fails people. |
| Five or more years as a solutions consultant, pre-sales engineer, or client-facing consultant in complex financial services | Oracle pre-sales, Oct 2015–Dec 2017, is the only pure pre-sales title, and it is utilities. OpenSC, Oct 2021–Sep 2023, is implementation consulting in supply chains. The headline says five-plus years of pre-sales. The dates do not. | Partial. Restate it. Do not defend the headline literally. |
| Business and technical communication | Workshops, a whitepaper, demos, proposals, earlier RFP work. English and French native. | Meets. |
| Own the technical workstream in a multi-stakeholder enterprise or tier-1 sale, and talk integration with client engineering | Oracle: $65 million+ scoped with sales, including a $23 million deal where you took requirements from the buyer's engineering team and the business. API and data-workflow scope. Nothing at that scale since. Later technical work is a Dun & Bradstreet spec and a startup MVP. | Meets once, and it is nine years old. |
| Architecture diagrams, solution proposals, technical specifications | IntegrityNext process flows and API specs. OpenSC solution design and a mobile data-capture spec. Oracle scoping. The diagrams themselves are not in the CV. | Meets at a functional level. |
| C1 German, Spanish, French, or Italian, listed as beneficial | Native French. German B2. Spanish B2. | Meets, on French. German B2 is a real limit on a DKB workshop, not a requirement. |
| Berlin or Europe, autonomous, several live pursuits | Berlin. EU and US work authorisation. The later roles are self-directed. | Meets. |

### What gets you the second hour

- Place N26, Raisin, and Revolut on the three operating models, and say what the client still builds in each.
- Tell the Oracle story as a scope decision you made with engineering in the room. Names of artifacts, not the logo.
- Use AstroFinance for discovery and investor qualification, and say in the same breath what does not transfer to a securities ledger.
- Offer French as a concrete asset for the PEA, IG's French launch, and the French branch. Be plain that German is B2.
- One sentence each on IntegrityNext and on July to November 2026.

### What ends it in the first hour

- Answering a custody or operating-model question with tokenisation, SPVs, or the aerospace whitepaper.
- Defending "five-plus years of pre-sales" against the dates. Oracle plus OpenSC plus a fractional product role is a career. It is not five years of pre-sales.
- Treating the $56,000 AstroFinance close as comparable to a DKB or CMC pursuit. The bridge is the $23 million Oracle cycle, and even that was a different industry.
- Quoting 40+ clients, 2 million end users, or a €640 million valuation as if the company had stated them. Use 30+ clients, 100 million orders, €105 million and €280 million, and label the valuation as a press report.

A second interview is the bar this prep can move. Later rounds still have to close a real gap in brokerage and custody. A strong first hour does not make an offer likely. It makes the offer a conversation you are allowed to keep having.

---

## Sources

Primary sources: upvest.co (about, FAQ, product, operating models, 2025 review, funding posts, and the DKB, Revolut, N26, Raisin, Openbank, CMC, IG, Salt Bank, and VisualVest posts); Börsen-Zeitung, 21 October 2025; Maddyness, 7 May 2025; Handelsblatt, 17 March 2026; The Next Web, 17 March 2026, for the reported €640 million valuation. Where euro and dollar headlines disagree, both are shown. Nothing here is an audited financial statement.
