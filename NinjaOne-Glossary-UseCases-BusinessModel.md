# NinjaOne Glossary, Use Cases & Business Model

Quick answers first, then a full glossary. **Acronyms are spelled out on first use.**

---

## Quick answers

### Is AEM done via AI?

**Short answer:** Autonomous Endpoint Management (**AEM**) is *intelligence-driven automation*. It **often includes Artificial Intelligence (AI) / Machine Learning (ML)**, but it is **not only AI**.

Think of a spectrum:

| Level | What it means | Example |
|-------|----------------|---------|
| **Manual** | Human does every step | Tech remotely installs a patch by hand |
| **Automation** | Pre-written “if X, then Y” rules/scripts | If disk > 90%, run cleanup script |
| **AEM (autonomous)** | System uses telemetry + policies + (often) AI/ML to **detect → decide → act → verify** with less human babysitting | Patch Intelligence scores a Windows update as risky → delay broad rollout → patch pilot ring first → monitor Digital Employee Experience (**DEX**) impact → expand |

**Gartner’s framing:** AEM uses configuration, compliance, risk, performance, and experience data to intelligently perform common endpoint management and DEX tasks. It combines ring-based deployments with **AI/ML**, DEX signals, and intelligence-driven automation tuned to risk appetite.

**So for interviews:**
- Don’t say “AEM = AI.”
- Do say: “AEM is autonomous ops — closed-loop detect/decide/remediate. AI can power the decisioning (like patch risk scoring), but policy, automation, and telemetry are equally core.”
- NinjaOne example: **Patch Intelligence AI** helps score/safety of patches; policies + automation still execute the workflow.

---

### What is RMM?

**Remote Monitoring and Management (**RMM**)** is software that lets IT teams (especially Managed Service Providers / **MSPs**) continuously **monitor** devices and **manage** them remotely.

Typical RMM jobs:
- See device health in real time (online/offline, CPU, disk, services)
- Alert when something breaks
- Remotely access/fix devices
- Push scripts and automations
- Patch and deploy software
- Maintain inventory across many machines (and for MSPs: many client companies)

**Plain analogy:** RMM is the “mission control + remote hands” system for endpoints.

**NinjaOne note:** People still call NinjaOne an RMM; NinjaOne increasingly markets a broader **Unified IT Operations Platform** (RMM + patching + backup + remote + more).

---

### What is EDR?

**Endpoint Detection and Response (**EDR**)** is security software focused on **finding and responding to threats** on devices (malware, ransomware behavior, suspicious process activity).

Typical EDR jobs:
- Continuously watch endpoint behavior
- Detect attacks / anomalies
- Alert security teams
- Isolate a compromised device
- Help investigate (“what happened on this laptop?”)

**RMM vs EDR (important distinction):**

| | **RMM** | **EDR** |
|--|---------|---------|
| Primary job | Operate & maintain devices | Detect & respond to threats |
| Owner vibe | IT operations / MSP technicians | Security / SecOps |
| Example actions | Patch Chrome, restart print spooler, disk cleanup | Quarantine malware, isolate host, threat hunt |
| Relationship | Often **integrates with** EDR | Often **integrates with** RMM/UEM |

NinjaOne is **not** primarily an EDR product. It commonly **integrates** with EDRs like CrowdStrike, SentinelOne, Microsoft Defender, Bitdefender, etc., so ops + security can work together.

---

### What is DEX?

**Digital Employee Experience (**DEX**)** is about how good (or bad) technology feels for employees at work.

DEX asks:
- Are laptops slow?
- Do apps crash?
- Is VPN flaky?
- Did that patch make Zoom unusable?
- Are people productive or frustrated?

**Why it matters now:** Classic IT measured “device is patched / online.” Modern IT also measures “employee can actually work.” AEM often uses DEX signals so automation doesn’t “win security” while destroying usability.

---

## Top 3 NinjaOne user use cases (in detail)

These are the three workloads that most consistently show up in NinjaOne’s own messaging, customer stories, reviews, and analyst positioning.

---

### 1) Autonomous / automated patch management (OS + third-party apps)

**What users are trying to do**  
Keep Windows, macOS, and Linux devices (and common third-party apps like browsers/productivity tools) up to date — reliably, across remote fleets — without drowning technicians in manual patch work.

**Why it matters**
- Unpatched devices are a top ransomware / breach path
- Audits and cyber insurance increasingly demand patch compliance evidence
- Manual patching doesn’t scale for hybrid/remote workforces
- Bad patches can break production — so blind auto-approve is risky

**How NinjaOne is used**
- Policy-based patching (maintenance windows, reboot behavior, approvals)
- Separate handling for **Operating System (**OS**)** vs third-party apps
- Staged rollouts / rings (pilot group → broader deployment)
- Dashboards for patch compliance and failures
- AI-assisted insight via **Patch Intelligence** (safety/risk style scoring) to support smarter approve/delay decisions
- Alerts + remediation when patches fail

**Who cares**
- Internal IT: security posture, audit readiness, fewer fire drills
- MSPs: standardized service delivery across many clients + QBR reporting

**Business outcome language**
- Higher patch compliance %
- Less technician time on patch Tuesdays
- Lower vulnerability exposure window
- Fewer “forgot to patch the CEO laptop” incidents

**Real-world flavor:** Customer stories (e.g., public-sector examples) often start with “our old patching was painful/manual” and expand into full platform adoption.

---

### 2) Unified endpoint monitoring, management & remote support (classic RMM / endpoint ops)

**What users are trying to do**  
See all endpoints in one console, catch problems early, and fix them remotely — preferably before users file tickets.

**Why it matters**
- Hybrid work = devices everywhere, not on the office LAN
- Tool sprawl (separate monitoring + remote + inventory + scripting tools) creates cost and context-switching
- MSPs need multi-tenant visibility across dozens/hundreds of client orgs
- Mean Time To Resolve (**MTTR**) and ticket volume drive IT cost and MSP margins

**How NinjaOne is used**
- Deploy one agent for telemetry + actions
- Monitor health/performance/online status
- Condition-based alerting (disk full, service down, etc.)
- Automation/self-healing for repetitive L1 issues
- One-click remote access/control for attended or unattended support
- Software deployment + scripting library
- Asset inventory / reporting
- For MSPs: organization/tenant separation + inherited policies

**Who cares**
- Service desk / technicians: faster fixes, less swivel-chair
- IT managers: fewer tools, better visibility
- MSP owners: more endpoints per technician

**Business outcome language**
- Replace 4+ tools with one platform (NinjaOne often cites consolidation stats)
- Lower MTTR
- Less alert noise via tuned conditions + auto-remediation
- Faster onboarding of devices/clients

---

### 3) Endpoint (and increasingly SaaS) backup & recovery for resilience

**What users are trying to do**  
Protect business data on endpoints/servers (and often Microsoft 365 / Google Workspace) so ransomware, deletion, or device loss doesn’t become a business outage.

**Why it matters**
- Ransomware encrypts endpoints and can target backups
- Laptops hold critical local files even in “cloud-first” companies
- SaaS apps (Exchange/OneDrive/SharePoint/Gmail/Drive) are not automatically “forever recoverable” to the retention/granularity companies assume
- Recovery testing is what makes backup real

**How NinjaOne is used**
- Policy-driven backup for workstations/servers
- Cloud backup management from the same console as monitoring/patching
- Restore files/systems when something fails
- Pair with broader resilience story (patching + security integrations + backup)
- MSPs package backup as a billable managed service add-on

**Who cares**
- IT leadership: business continuity
- Security: ransomware readiness
- MSP commercial teams: attach-rate / margin on backup services

**Business outcome language**
- Faster recovery (Recovery Time Objective / **RTO**)
- Less data loss (Recovery Point Objective / **RPO**)
- Proof of restore drills for audits/clients
- One vendor for protect + manage instead of a separate backup silo

---

### Honorable mentions (often #4/#5)
- **Mobile Device Management (**MDM**)** for iOS/Android fleets  
- **Ticketing / documentation** for lighter IT Service Management (**ITSM**) / Professional Services Automation (**PSA**)-adjacent workflows  
- **Security stack orchestration** (manage/integrate antivirus/EDR from the console)

---

## NinjaOne business model: how they make money

### Model in one sentence
NinjaOne is a **Business-to-Business (**B2B**) Software-as-a-Service (**SaaS**)** company that sells **recurring subscriptions** to MSPs and internal IT organizations, primarily priced **per managed endpoint (device) per month**, with optional paid modules on top.

### How money comes in

1. **Core platform subscription (main engine)**  
   Customers pay recurring fees to manage endpoints in NinjaOne (monitoring, patching, automation, remote capabilities, etc.).  
   Official public range (commercial instance): about **$1.50 per endpoint/month at ~10,000 endpoints** up to about **$3.75 per endpoint/month at ≤50 endpoints**, varying by region and products. Volume discounts apply.

2. **Module / add-on expansion (upsell land-and-expand)**  
   After adopting core endpoint management, customers often add:
   - Backup
   - MDM
   - Documentation / other adjacent capabilities  
   These are typically also subscription-priced (often per device), increasing Average Revenue Per Account.

3. **Contracted recurring revenue**  
   Monthly or annual billing (annual/commit terms common for better rates). This creates **Annual Recurring Revenue (**ARR**)**.

4. **Go-to-market motion**  
   Sales-led + partner/channel-aware (important for MSP margins). Pricing is often quote-based rather than fully self-serve list pricing, partly to avoid undercutting MSP service packaging.

### What they do *not* primarily monetize
- Not ads
- Not a pure per-technician seat model (that’s more Atera-style)
- Not primarily professional-services-led (they emphasize product + free onboarding/training/support as a customer-success differentiator; services aren’t the main P&L engine)

### Scale snapshot (public company claims / press)
- Surpassed **~$500M ARR** (announced early 2026), with very high YoY growth claims (~70% range in that announcement cycle)
- Tens of thousands of customers (company messaging has cited ~35k–40k depending on date/source)
- Private company with large venture funding / multi-billion valuation reports in press
- Sells to **two segments**: MSPs and internal IT

### Strategy behind the model
- **Land:** win on ease-of-use + patching/RMM core  
- **Expand:** attach backup/MDM/etc.  
- **Retain:** high switching costs once agents/policies/automations are embedded + strong CSAT/support narrative  
- **Why per-endpoint works:** aligns with customer value (more devices managed = more value) and with MSP packaging (MSPs often bill clients per device too)

### Interview-ready summary
> “NinjaOne makes money as a B2B SaaS vendor: recurring subscription revenue, mostly per endpoint per month, sold to MSPs and internal IT. The core RMM/endpoint platform is the land; backup, MDM, and other modules are the expand. Their growth story is replacing multiple point tools with one unified IT operations platform and monetizing that consolidation through subscriptions.”

---

## Glossary (terms to know)

Spellings below include the full phrase first.

### A–C
| Term | Definition |
|------|------------|
| **AEM — Autonomous Endpoint Management** | Next-gen endpoint ops that uses telemetry + policies + intelligence-driven automation (often AI/ML) to detect, decide, remediate, and verify with less human effort |
| **AI — Artificial Intelligence** | Computer systems that perform tasks associated with human intelligence (pattern recognition, prediction, decision support) |
| **Agent** | Small software installed on a device that reports data to the platform and runs actions (patch, script, monitor) |
| **Alert / Condition** | A rule that fires when something is wrong (e.g., disk full, patch failed, device offline) |
| **API — Application Programming Interface** | A documented way for software systems to talk to each other programmatically |
| **ARR — Annual Recurring Revenue** | Yearly value of ongoing subscription revenue |
| **Automation** | Predefined workflows/scripts that run without a human doing each step |
| **AV — Antivirus** | Traditional malware protection software |
| **B2B — Business-to-Business** | Selling to organizations, not consumers |
| **BCDR — Business Continuity / Disaster Recovery** | Planning and tech to keep operating and recover after major disruption |
| **BYOD — Bring Your Own Device** | Employees use personal devices for work |

### D–I
| Term | Definition |
|------|------------|
| **DEX — Digital Employee Experience** | Quality of the technology experience for employees (performance, reliability, usability) |
| **EDR — Endpoint Detection and Response** | Security tooling that detects/investigates/responds to threats on endpoints |
| **Endpoint** | Managed device: laptop, desktop, server, VM, phone, tablet, etc. |
| **Endpoint management** | Practice/tools for inventorying, configuring, patching, monitoring, securing, supporting endpoints |
| **IAM — Identity and Access Management** | Controlling who can access what (accounts, roles, permissions) |
| **IdP — Identity Provider** | System that authenticates users (e.g., Microsoft Entra ID, Okta) |
| **ITOps / I&O — IT Operations / Infrastructure & Operations** | Teams/processes that keep IT services running |
| **ITSM — IT Service Management** | Framework/tools for incidents, requests, changes (often ServiceNow, Jira Service Management) |

### M–P
| Term | Definition |
|------|------------|
| **MAM — Mobile Application Management** | Managing/securing apps on mobile devices without always fully managing the whole device |
| **MDM — Mobile Device Management** | Enrolling/configuring/securing phones and tablets |
| **MFA — Multi-Factor Authentication** | Login requiring more than just a password |
| **ML — Machine Learning** | AI subset where systems learn patterns from data |
| **MSP — Managed Service Provider** | Company that remotely manages IT for multiple client organizations |
| **MSSP — Managed Security Service Provider** | MSP-like provider focused on security services |
| **MTTR — Mean Time To Resolve** | Average time to fix an incident |
| **Multi-tenancy** | One software platform serving many separate customer organizations securely |
| **OS — Operating System** | Windows, macOS, Linux, iOS, Android, etc. |
| **Patch / Patch management** | Finding, approving, deploying, and verifying software updates |
| **Patch compliance** | Percentage of devices that meet required update standards |
| **PoC / PoV — Proof of Concept / Proof of Value** | Trial engagement to prove the product works / delivers value |
| **Policy** | Baseline settings/automations applied to a group of devices |
| **PSA — Professional Services Automation** | MSP platform for ticketing, time tracking, contracts, billing, documentation |
| **Parent/child policy** | Shared baseline policy with inherited child policies and controlled overrides |

### Q–Z
| Term | Definition |
|------|------------|
| **QBR — Quarterly Business Review** | Periodic business/ops review, common between MSP and client |
| **RBAC — Role-Based Access Control** | Permissions based on job role |
| **Remediation** | The fix action after a problem is detected |
| **Remote access / remote control** | Taking control of a device over the internet to support or maintain it |
| **RMM — Remote Monitoring and Management** | Platform to monitor and manage endpoints remotely (core MSP/IT ops tool category) |
| **RPO — Recovery Point Objective** | How much data you can afford to lose (time since last good backup) |
| **RTO — Recovery Time Objective** | How quickly you need to be restored after failure |
| **SaaS — Software-as-a-Service** | Cloud software delivered by subscription, vendor-hosted |
| **SAML — Security Assertion Markup Language** | Common standard used for Single Sign-On |
| **SIEM — Security Information and Event Management** | Central platform for security logs/alerts/analytics |
| **SLA / SLO — Service Level Agreement / Objective** | Commitments/targets for response and resolution performance |
| **SSO — Single Sign-On** | One login grants access to multiple systems |
| **TCO — Total Cost of Ownership** | Full cost beyond sticker price (admin time, add-ons, training, etc.) |
| **Third-party patching** | Updating apps that are not the OS (Chrome, Zoom, Adobe, etc.) |
| **Ticket / Service desk** | Tracked user/IT request or incident |
| **Tool sprawl** | Too many overlapping tools causing cost and complexity |
| **UEM — Unified Endpoint Management** | Manage computers and mobile devices from one control plane |
| **VM — Virtual Machine** | Software-based computer running on a hypervisor/host |
| **VPN — Virtual Private Network** | Encrypted network tunnel, often used for remote access to company resources |
| **Vulnerability management** | Finding and prioritizing software weaknesses (often Qualys/Tenable/Rapid7) |
| **XDR — Extended Detection and Response** | Security detection/response across endpoint + broader signals (identity, email, cloud, etc.) |
| **Zero-touch provisioning** | Devices autoconfigure on setup with minimal hands-on IT work |

---

## Tiny memory aids

- **RMM** = run the fleet  
- **EDR** = hunt the bad guys on the device  
- **DEX** = how happy/productive the human feels  
- **AEM** = fleet mostly runs itself (rules + data + often AI), humans supervise exceptions  
- **NinjaOne money** = SaaS subscriptions, mostly **per endpoint**, then module upsells
