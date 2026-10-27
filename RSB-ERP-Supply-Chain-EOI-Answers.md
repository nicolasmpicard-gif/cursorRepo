# RSB External Consultant Roster

## ERP & Supply Chain Systems Consultant — questionnaire draft

**Applicant:** Nicolas Picard, independent consultant, Berlin
**Profile covered:** partial coverage — chain-of-custody data flows, process and materials-flow mapping, requirements-to-system translation, SOPs, training and handover
**Status:** draft for your review. Figures and statements marked **CONFIRM** are not on the CV. Change them before you submit.

The call listed a submission deadline of 24 October 2026. Today is 27 October 2026 (Europe/Berlin). Send this only if the portal is still open, or with a short note if RSB has allowed a late expression of interest.

### Positioning paragraph (optional cover note)

I am applying as an individual consultant, for partial coverage of this profile. My implementation work is the design of chain-of-custody data flows, process maps, control points, operating procedures and training, delivered inside a client’s real supply chain rather than in a parallel spreadsheet. The reference project is an end-to-end coffee traceability implementation in the Democratic Republic of Congo. Alongside that, I have scoped enterprise data workflows and API integrations in pre-sales for Oracle Utilities. I will use RSB’s roster onboarding to align that delivery method with the RSB chain-of-custody models and with the client’s specific ERP.

---

### 1. Daily rate (EUR), availability (days/month), and notice to mobilise

**Daily rate:** EUR 950 per day. **CONFIRM.**

**Availability:** about 10 days per month as a standing commitment, and up to 15 days per month for a time-bound assignment with an agreed end date.

**Notice to mobilise:** 10 working days from acceptance of a Terms of Reference. I can start sooner when my calendar is clear.

The rate is a professional day rate for remote delivery in English, covering preparation, client working sessions, documentation and handover. Travel, if an assignment requires time on site, would be agreed separately in the Terms of Reference. I invoice as an individual consultant tax-resident in Germany.

---

### 2. Chain-of-custody or mass-balance accounting system

Yes. From October 2021 to September 2023, as Lead Implementation Manager at OpenSC, I supported Nespresso in implementing an end-to-end chain-of-custody traceability system for its coffee supply chain in the Democratic Republic of Congo.

**Framework.** The system served Nespresso’s supply-chain transparency programme. It was specified as critical tracking events and key data elements along the physical chain, from cooperative reception through processing and onward movement. It was not an RSB, ISCC, EU RED or CORSIA implementation.

**Model.** Identity preserved. Lots stayed identifiable through the chain, with data captured at each hand-off on a mobile flow used by workers at two coffee cooperatives. The design separated traced product from untraced product by recording the event, the lot and the party at each step. I have not implemented a mass-balance credit account, or a book-and-claim registry, inside an ERP.

**Audit.** I do not have a record of a certification body subsequently auditing that system. **CONFIRM** if a buyer audit, internal assurance review, or certification-body audit took place and should be named. What I can stand behind is the operating result: quarterly business reviews with Nespresso’s senior sustainability leaders against a joint success plan, data-collection success above 90 percent, and detection of data issues in under 24 hours, down from 3 days. The client renewed the project.

The same method — map the physical flow, define the events and data elements, put the control in the system people already use, and leave an evidence trail — is what I would apply to an RSB identity-preserved, segregation or mass-balance design after RSB’s onboarding.

---

### 3. Client processes that are unclear or undocumented

I start from the work as it is done, and I write it down with the people who do it, before any system design.

On the coffee programme, the chain was not documented to the level a traceability design needs. I ran discovery with the trader’s operational teams and with the cooperatives, and I used that to cut a week out of discovery once the teams were willing to share how product and data actually moved. The output was a single map of actors, hand-offs, documents and systems, then a short list of critical tracking events and key data elements. We agreed a written success plan before build, piloted the capture flow at two cooperatives, and only then tightened it. Simplifying that flow cut onboarding cost by a factor of four and onboarding staffing by half, which is usually the sign that the first draft of the process was heavier than the operation could carry.

The sequence I use is:

1. **As-is, from the operators.** Short working sessions with procurement, warehouse, production and dispatch, plus a sample of real documents (orders, goods receipts, batch tickets, invoices, dispatch notes). Management interviews set context. They do not replace the floor-level walkthrough.
2. **One picture.** A process map and a system map on a shared board (I use Miro), showing where stock, documents and data change hands, and where the current record stops.
3. **A written scope.** A success plan that names the chain-of-custody model, the control points, what will be configured in the existing system, what stays a manual control, and what is out of scope. Both the operational lead and the management sponsor sign it.
4. **Design against real transactions.** Walk a few actual lots through the future process, including a split, a loss, a return and a sale, and check that each one produces an evidence record a auditor could follow.
5. **Pilot, then write the SOP.** One site or one product family first. The SOP and the training notes are written from the pilot, so they match the system the team will keep after handover.

Where a step exists only in someone’s head, it goes on the map as an uncodified step, with an owner and a decision: standardise it, or leave it and record the risk. I would rather show RSB and the client an honest gap in week two than discover it in the audit sample.

---

### 4. Timeline, budget, hours, scope creep, and client-side delays

**Example.** The Nespresso coffee traceability implementation in the Democratic Republic of Congo, delivered while I was Lead then Senior Implementation Manager at OpenSC.

We ran it against a success plan agreed with the client’s sustainability leadership, and we reviewed that plan in quarterly business reviews. The outcomes the plan was built around were met: data-collection success above 90 percent, and data-issue detection brought from 3 days to under 24 hours. The client renewed the project. On the capture redesign, a simpler mobile flow reduced onboarding cost fourfold and halved onboarding staffing, which kept the roll-out inside a cost level the cooperatives could sustain. A separate scoping engagement with a major coffee trader, where I was the advisor to three of their teams, took five days out of discovery because the delivery plan was explicit about what we needed from them and why.

I do not have a published budget-variance figure for that programme in my records, so I am not claiming a percentage under budget. **CONFIRM** if you have the commercial numbers and want them stated.

**Hours.** I log time against the work breakdown in the Terms of Reference, in the client’s Jira when the project uses it, otherwise in a simple time log tied to the same task list. The client and RSB see days used, days remaining, and what the days were spent on, in a short written status at an agreed rhythm (weekly on an active build, at the QBR when the project is in run mode).

**Scope creep.** The success plan is the baseline. A request that adds a site, a legal entity, a chain-of-custody model, a system, or a report is a change: I write the impact on days, date and price, and I start the extra work only after the client (and RSB, where RSB owns the engagement) accepts it. Smaller clarifications that stay inside an agreed deliverable are absorbed and noted, so the change process is used for real scope and not for every question.

**Client-side delays.** I flag a dependency as soon as it is late, not at the milestone it breaks. Work that does not need the client continues. Work that does is re-sequenced, and I re-baseline the date in writing with the reason attached. Waiting time is visible in the status, so a delay on master data, a system owner, or a sign-off is a shared fact rather than a surprise at the end of the month. I keep one operational counterpart and one management sponsor named, so a stalled question has a person who can unblock it.

---

### 5. Client-facing advisory, with operational staff and management at the same time

Most of my work sits between people who ship product and people who own the sustainability or commercial outcome.

At Nespresso I ran the quarterly business reviews with senior sustainability leaders against the joint success plan, and in the same programme I specified the mobile capture used by workers at two cooperatives in the Democratic Republic of Congo. The management conversation was about results, renewal and where data was failing. The operational conversation was about whether a worker could complete the step during a real intake. Both were the same project. The success plan was what kept them aligned: leaders saw the measure, operators saw a flow that had been cut down until they could run it.

With a major coffee trader I was the advisor to three teams at once. The practical effect of being trusted with how they actually worked was that they shared data they had been holding, and discovery shortened by five days. I prepared the delivery plan so each team could see what was being asked of them and what they would get back.

At Oracle Utilities I sat with the buyer and with the buyer’s engineers in the same scoping effort, and turned that into a solution definition the sales lead could negotiate. That was pre-sales rather than a multi-year implementation, and it is where I learned to keep a commercial scope and a technical scope as one document.

In the current independent practice I advise, through Dialectica, on the choice of supply-chain risk platforms against a client’s ESG use cases. Those are short, senior advisory conversations. The long-form client management I would bring to RSB is the OpenSC model: one written plan, a regular review with the sponsor, and working sessions with the people who have to live with the process after I leave.

Expectations stay manageable when each group hears the same scope, the same date and the same open risks, in language that matches their job. Operators get procedures, screen-level data fields and time to practise. Sponsors get a status, a decision list and a clear statement when a decision of theirs is now on the critical path. I do not carry a different version of the timeline for each audience.

---

### 6. Languages, and countries or regions where I have delivered

**Languages.** English, native. French, native. German, B2. Spanish, B2. Project delivery, documentation and audit-facing material I produce in English. I can run working sessions in French, and in German or Spanish when the session is prepared and the written record stays in English.

**Implementation delivery.** Democratic Republic of Congo: on-the-ground design and roll-out of the coffee chain-of-custody capture at two cooperatives, as part of a supply chain that runs through to export. Germany: my base since the OpenSC years, and the place I deliver remote client work from.

**Related delivery, different kind of project.** United States: two years in San Francisco scoping Oracle Utilities solutions with utility clients (commercial and technical scoping, not an industrial ERP implementation). Bangladesh: while I was Research and Project Manager at WEConnect International, I led implementation of a funded programme that included launching the organisation there, and I used purchasing-category analysis for Walmart and Johnson & Johnson to build supplier-diversity plans. That was programme and procurement-category work, not an ERP or chain-of-custody system.

I have not delivered an implementation project in Latin America or in industrial Asia. I am eligible to work in the European Union and the United States.

---

### 7. Relationships that could create a conflict of interest

I do not currently advise, audit, or hold a contract with RSB, any other certification scheme, any certification body, or any operator certified against RSB. I am not an accredited auditor. I have no financial interest in a certification body.

Relationships I am disclosing so RSB can judge perception as well as fact:

- **Dialectica (April 2026 to present).** I am an expert advisor on the Dialectica network. I advise institutional clients, on a call-by-call basis, on the selection of supply-chain risk management platforms for ESG use cases. This is not a scheme, a certification body, or an operator relationship. If a named RSB assignment involved a company I had already advised, or a platform selection I had already opined on, I would say so before accepting and step back if the overlap affected independence.
- **OpenSC (October 2021 to September 2023) and IntegrityNext (July 2024 to October 2024).** Former employer relationships, both ended. OpenSC is a supply-chain traceability platform. IntegrityNext is a supply-chain sustainability compliance platform. I have no ongoing commercial tie to either firm. If a future RSB client already used one of those platforms, I would disclose the prior employment before the assignment. I would not review, as an advisor, a design I had myself implemented.
- **AstroFinance (February 2025 to June 2026).** Fractional Head of Product for a fintech startup. That engagement has ended. It is unrelated to certification.

I will disclose any new relationship of this kind during the roster period, as the call requires.

---

### 8. ERP systems in procurement or supply chain management

I have not configured SAP, Oracle ERP (E-Business Suite or Fusion SCM) or Microsoft Dynamics as an implementer inside a mill, refinery or blender. My systems work is integration scoping on enterprise SaaS, and the design of traceability and supplier-data flows on dedicated platforms that sit on top of a physical supply chain. I am describing it at that level so the partial-coverage boundary is clear.

**Oracle Utilities, San Francisco, October 2015 to December 2017. Pre-Sales Business Analyst.**
The operation was electricity, water and gas utilities: customer operations, billing and grid management, on Oracle’s cloud software for those processes. I partnered with sales executives to scope, negotiate and close more than USD 65 million in SaaS agreements. My part was the solution definition: business and technical requirements from the buyer and from the buyer’s engineers, and the professional-services scope that went with the licence, including API integrations, data workflows and web-portal customisation. One joint negotiation that I worked in this way was a USD 23 million agreement. This was utility operational software, scoped in pre-sales. It was not a manufacturing or commodity-trading ERP, and I was not the implementation consultant after signature.

**OpenSC, Berlin, October 2021 to September 2023. Senior, then Lead Implementation Manager.**
The operation was agricultural supply and export trading: green coffee collected and processed at cooperatives in the Democratic Republic of Congo and sold onward through a trader to Nespresso. I led solution design and implementation of the track-and-trace system, defined the chain-of-custody events and data elements, and specified the mobile data-capture flow used at two cooperatives. I led a team of three on the traceability solution and on a performance dashboard. The system of record for traceability was OpenSC’s platform, connected to the way the cooperatives and the trader already moved product, with the data model agreed with their teams. I did not implement this inside SAP, Oracle or Dynamics.

**IntegrityNext, Berlin, July 2024 to October 2024. Product Manager.**
The operation was a SaaS platform used by manufacturers and brands to collect sustainability information from suppliers. I improved a multi-tier supplier outreach tool used by more than 1,000 enterprises across tier-1, tier-2 and tier-3 suppliers, from requirements gathered with sustainability and procurement practitioners, and I wrote the product flow and specification for a third-party API integration used by more than 500 enterprise customers. This is procurement-linked supplier data, not inventory or production ERP.

**What I would do on an RSB assignment, inside that boundary.** Map procurement, production, inventory and sales as they run today. Define the chain-of-custody events, the stock separation or mass-balance accounts, the reconciliation points and the evidence at each one. Specify the ERP data fields, statuses and controls the client’s own system owner needs to configure, and test them by walking real transactions through. Write the SOP and train the team. I would work beside the client’s ERP owner or integration partner for the configuration itself, and I would say so in the proposal if the Terms of Reference assumed hands-on SAP, Oracle or Dynamics configuration.

---

### 9. Time zone and typical working hours

I am based in Berlin. My time zone is Central European Time (UTC+1), and Central European Summer Time (UTC+2) from the last Sunday in March to the last Sunday in October.

Typical hours are 09:00 to 18:00 CET, Monday to Friday. That covers the full CET working day, well beyond the four-hour overlap this call requires.

For an active assignment I can move earlier or later inside roughly 08:00 to 19:00 CET, which reaches US Eastern morning and US Pacific start of day, and reaches East and Southeast Asian late afternoon. A regular standing call outside that window is something I would agree in the Terms of Reference, not assume.

---

### 10. Legal name and registration address, if applying for an organisation

I am submitting as an individual consultant. I am not submitting on behalf of an organisation. **CONFIRM** if you invoice through a registered sole proprietorship or company and want that legal name and address stated here instead.

---

### 11. Part-time and full-time employees

I am an individual consultant. I have no part-time or full-time employees.

For context, and so this is not confused with a firm: at OpenSC I led a team of three as an employee of OpenSC, and at AstroFinance I managed one financial analyst as the startup’s fractional head of product. Neither group was employed by me.

---

### 12. Years operating as a consultant

I have operated as an independent consultant since February 2025, about one year and nine months at the time of this expression of interest.

Client-facing delivery of the kind this roster uses is longer than the independent practice. From 2015 to 2017 I scoped enterprise solutions with utility clients at Oracle Utilities. From 2018 to 2021 I wrote proposals and scopes of work and led programme delivery at WEConnect International, including a USD 500,000 programme. From 2021 to 2023 I led traceability implementations at OpenSC. I am PMP certified (Project Management Institute, 2019).

---

### 13. Affiliation with another entity, and lawsuits

I am not a subsidiary, branch, partner or member of another entity. My practice is my own. The Dialectica relationship in section 7 is a client engagement on an expert network. It is not an ownership, partnership or membership tie.

I have no current or pending lawsuits filed against me. **CONFIRM** before submitting.

---

### 14. Individuals with signatory authority

Nicolas Picard. As an individual consultant I am the only person authorised to sign a non-disclosure agreement, a framework agreement or a consultant agreement for this practice.

---

### 15. Post-sales support I typically offer

The support I build in is the handover itself, because the assignment should leave a process the client can run.

On a project of this kind the closing package is:

- the as-is and to-be process maps, and the chain-of-custody data-flow diagram
- the requirements-to-system mapping (fields, statuses, control points, reconciliation steps)
- an evidence checklist an internal owner can use before an audit
- standard operating procedures written from the piloted process
- one training session for the people who execute the process, and one for the process owner who will maintain it
- a short list of open items, each with an owner on the client side

After the final deliverable I include a handover window of 10 business days for clarification, correction of the documents, and one refresher session. Questions in that window are part of the project, not a new invoice.

Anything after that window — a new site, a new product, a standard revision, support through an audit — is further work at the same day rate, scoped in writing before it starts. I do not leave an open-ended support retainer in place by default. Where a Terms of Reference asks for one, I will quote a fixed number of days per quarter.

---

### 16. The commercial service, response times, and scaling

**Service.** Remote advisory and implementation support on RSB Advisory Services projects: process and system mapping, chain-of-custody data-flow and control design, translation of certification requirements into ERP data fields and reconciliation routines, SOPs, training and handover. Delivery is in English. On-site days, if a project needs them, are agreed in the Terms of Reference.

**During an active assignment, on CET working days:**

- acknowledgement of a message within 4 working hours
- a substantive reply within 1 business day
- in the 10 business days before an agreed milestone or a client audit, a same-day reply on questions that are blocking the milestone

**Outside an active assignment** (roster member, no open Terms of Reference): I reply to an RSB enquiry within 2 business days, and I confirm whether I can take the work within 5 business days of receiving the draft scope.

**Scale.** I am one person, and I would not subcontract an RSB assignment without written agreement. Capacity scales by changing how many of my own days are reserved:

- scale up, from the standing 10 days per month toward 15, with 10 working days’ notice
- scale down, or pause, with 10 working days’ notice, so the client and RSB can re-plan
- planned leave is stated at the start of an assignment, with the handover notes prepared before I am away

I cannot add a second consultant to cover an absence. If an assignment needs uninterrupted cover, a firm is the better vehicle, and I would rather say that when the Terms of Reference arrives than imply bench capacity I do not have.

---

### 17. Work example

**Coffee chain-of-custody traceability, Democratic Republic of Congo. Client: Nespresso. My role: Lead Implementation Manager, OpenSC, within the period October 2021 to September 2023.**

Nespresso needed a reliable record of how coffee moved from two cooperatives in the Democratic Republic of Congo through processing and into the export chain. The data that existed was late, incomplete, and slow to correct: issues in the traceability data took about three days to surface, which is too slow to fix a lot that is already moving.

I led the solution design and the implementation. The first job was to define the chain of custody in operational terms: the critical tracking events, the key data elements at each event, and the parties who could actually capture them. In parallel I was the advisor to three teams at the trader. Once they could see a delivery plan that respected how they worked, they shared data that discovery had been missing, and that phase shortened by five days.

The capture tool was where implementations of this kind usually fail. Supply-chain workers at the cooperatives had to record the events during real intake and processing. I specified the mobile flow and then cut it back until onboarding cost fell by a factor of four and the staffing needed to onboard people fell by half. A heavy process would have looked complete in a design workshop and then stopped being used.

I then led a team of three to improve the traceability solution and to put a performance dashboard on it, so data issues were visible in under 24 hours rather than after three days. Each quarter I reviewed results with Nespresso’s senior sustainability leaders against the success plan we had agreed together. Data-collection success held above 90 percent, and the client renewed the project.

What this shows for the RSB roster is the part of the role I have already done at length: turning a sustainability commitment into events, data, controls and evidence inside a live physical supply chain; writing the process so the people on the ground can run it; and keeping a management sponsor aligned with a written plan, a regular review, and a result they were willing to extend. The part I would learn on RSB’s onboarding, and not claim as already delivered, is mass-balance bookkeeping inside SAP, Oracle or Dynamics, and the RSB standard itself.

---

## Before you send

| Item | Draft I used | Why you must confirm |
| --- | --- | --- |
| Day rate | EUR 950 | Not on the CV. A band of EUR 850–1,100 is plausible for this roster; 950 is a middle figure a standards body can accept from an individual on partial coverage. |
| Availability | 10 days/month, up to 15 | Check this against Dialectica and any other live commitments. |
| Notice | 10 working days | Shorten only if you can truly start faster. |
| Certification-body audit | None recorded | Add it if the Nespresso system, or any other, was audited. Do not add it if you are unsure. |
| Lawsuits | None | Your statement, not something the CV can prove. |
| Legal entity | Individual, no organisation | Replace section 10 if you invoice through a registered firm, and then align sections 11 to 14. |
| Response times | 4 hours / 1 business day | These are commitments. Loosen them if you do not want them in a framework agreement. |
