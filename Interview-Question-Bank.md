# Interview Question Bank

_A single, consolidated prep document merging “Interview questions” and “solutions consultant prep”. All question and answer text is reproduced verbatim from those two documents; only the section structure is new._

## Contents

- 1. General interview questions
- 2. Solutions consulting & solutions engineering questions
- 3. Product manager questions
- 4. Technical & engineering collaboration questions
- 5. B2B SaaS questions
- 6. Sustainability, ESG & value chain questions
- 7. Experience bank: examples and evidence
- Appendix: Questions still to answer

# 1. General interview questions

## 1.1 Background and experience

### What was your last set of performance feedback improvement areas?

_[No answer drafted yet]_

### What was your responsibility at AstroFinance with regards to the product?

_[No answer drafted yet]_

### What was your responsibility at OpenSC with regards to the product?

- I helped define the iteration and expansion strategy for the coffee supply chain transparency solution, which had successfully made it past pilot phase in DRC Congo
  - As part of the iteration, I improved the product back-end by improving the data collection mechanism and developed a product performance dashboard
  - I managed a remote team on the ground in DRC responsible for hardware roll-out and user training
  - I sped up the overall onboarding of users, implementation partners, and the client/executive user
  - I managed a designer, solution architect, and engineers to ideate and organize feature development and delivery
- As the team grew and we hired staff to roll out in other Nespresso markets, I became the Product lead for what we call ‘Tough Unlocks’ – coffee supply chains that are more complex and require a special set of tools
- I helped build the onboarding toolkit for OpenSC to roll out into different markets. I onboarded a large coffee company in Uganda
- I helped develop standardized supply chain analytics modules by running discovery with Nespresso sustainability team

### What is the OpenSC product?

- In short, it is a supply chain transparency solution that powers the verification of production claims made by large food & beverage companies like Nespresso. It verifies low-carbon and sustainable food production at the source
- It is a supply chain transparency solution made up of different products. OpenSC operates across different commodities but in coffee the products were:
  - **Chain of custody validation platform** – this verifies that coffee is organically sourced and that non-organic coffee does not infiltrate the supply chain
  - **Payment verification platform** – this verifies that coffee farmers have been paid the correct amount for the coffee they’ve produced and sold
- The platforms powered two external-facing products:
  - **Supply chain analytics modules** for Nespresso sustainability managers, providing insights into the coffee journey and whether the quality, production process, and sustainability standards have been met
  - **Coffee journey experience** for end consumers of Nespresso coffee – this was an experience where Nespresso consumers could scan a QR code on the back of a sleeve of DRC congo capsules and trace the journey of the coffee from the purchasing at the farms until arrival in the Nespresso facility
- As I left the company we were getting our first recurring revenue contract – we were trying to build a SaaS company

### What are the data steps/what is the data layer for the OpenSC product?

- Scans of supply chain documents are sent to Amazon S3 cloud storage through automatic sync of the Android app. 
- Transcription teams at a service provider access the files and transcribe the data into CSV files, which are uploaded back into the cloud folder
- Coffee app data inputted directly into the app generates CSV files that are also uploaded into the cloud
- A hash of each file is stored on Ethereum blockchain to provide tamper-proof records
- The chain of custody is constructed by our data scientist using Python scripts and Jupyter notebooks, and the analytics are surfaced on AmazonQuickSight

## 1.2 Teamwork

### How do you handle disagreements with your design or engineering counterparts?

- I like to address disagreements head on in a calm environment without being under pressure
- My high level approach is first to handle emotions – with no props or visual cue – just listening to where the person is coming from
  - Then bring in the output/piece of work in questions
  - Retrace steps together – as a team – to figure out the rationale for decision-making and how we arrived to the point of disagreement
- There was one instance where an engineer came up with a technical solution for a user story I submitted in a JIRA ticket – but I disagreed with this solution
  - I had a quick sync with the engineer in question – explained to him why I thought his solution wasn’t the best way to approach the problem holistically, and demonstrated to him how it would cause problems down the line
  - He went back to the drawing board and came back with a second solution – we checked it together and I signed off – it turns out that the way I wrote the JIRA ticket wasn’t completely clear, so I also had a think about how I could improve on that next time.

## 1.3 Project & stakeholder management

### Tell me about a time you used data to influence an important stakeholder?

- **Situation**: at OpenSC I was the senior product manager for the digital transparency solution rollout and scale-up in DRC. This particular incarnation of the project is very custom and the operating difficulties in DRC are particularly high. It was a month before the start of the harvest and we had to decide at which coffee cooperatives we would roll-out the solution 
- **Task**: We had conducted field research at three possible sites and the expectation was that we would roll out across all three sites. 
- **Action**: I looked back through the research we had available for each site, including the existence of predictable supply chain processes, stability in supply chain staff, quality of the supply chain documents available. One site in particular I saw did not do well on any of these fronts. Rolling out at this site would be significantly slower and more difficult 
- **Result**: I advised to the COO to roll out in only 2 of 3 sites for this harvest, and to run further research at the third site to prepare for a roll-out there next harvest.

### Describe a situation where you had to advocate for the user’s needs against business pressures?

- When building the myCXvision MVP, the CEO of the developer company insisted that the tool be marketed toward CX Directors
- While doing discovery I realized that companies with CX Directors and CX departments were already very mature when it came to understanding their CX capabilities and next steps
- Instead, I was finding that Senior Marketing Leaders trying to build a culture of CX in their companies were a better target
- I had to advocate their needs over the CXD’s – this was a tough sell to the CEO, who preferred to cater to the CXDs as they are the primary buyer of consulting services

# 2. Solutions consulting & solutions engineering questions

## 2.1 Discovery & building client relationships

### Building Client Relationships: "How do you establish trust and credibility with a prospect early in the pre-sales process? Can you give an example where this approach was critical to closing a deal?"

- Get to know them personally – ask them for a coffee or informal chat 
- Come to meetings ready – slides, ideas, requirements all tailored to the prospect’s needs
- Establish yourself as someone reliable – answer emails promptly and fully; check in to see if they have any other concerns
- Don’t paint a rosy picture always – acknowledge where there is a mismatch between the prospect’s needs and the platform’s offerings – this will show transparency and good intent
- Share insights from recent industry reports
- Share customer success stories
- Provide value **before** the sale (i.e. an ESG assessment, white paper, etc.)

### Strategic Customer Engagement: When engaging with a new enterprise prospect, how do you approach understanding their specific ESG challenges and ensuring that Pulsora’s solution aligns with their strategic goals?

- Publicly available ESG and sustainability reports, news monitoring (look at recent events), benchmarking against peers in their industry or ESG topic area
- Create a materiality matrix if they don’t have one
- Assess applicability of different ESG regulations
- Refresh by reading up on the ESG framework or topic area
- Before first meeting, map out which of our solutions check off more of their boxes
- In the first meetings, build rapport with the key POCs, make sure they’re the right roles to approach
- Ask them to articulate their ESG challenges and listen actively 
- Mention info that you know from publicly available sources to show you’ve done your homework
- Empathize with their problem and pain point, then build in Pulsora’s solution organically
- Tailor a demo

## 2.2 Demos & explaining complex concepts

### Tell me about a time you explained a complex product concept to a non-technical buyer

- Explained tokenization to financial people
- Explained blockchain to my team

### Tailored Demo Approach: "When preparing a product demo for a client, how would you tailor it to meet the needs of different personas, such as a sustainability manager versus a CFO?"

When preparing a product demo, I tailor the presentation to address the specific needs and objectives of each persona. For a Sustainability Manager, I delve into ESG compliance frameworks, demonstrating how our platform seamlessly integrates with their existing spreadsheets and systems. I also showcase the robust reporting functionalities that facilitate streamlined sustainability tracking. 

Conversely, for a CFO, I emphasize the platform's strategic advantages by illustrating clear ROI. This includes a walkthrough of modules that process financial data—such as double materiality analysis—and generate actionable insights. I highlight intuitive visualizations and forecasting models that account for key financial factors, aiding in informed decision-making.

### How do you tailor a demo differently for an engineer vs. a VP of Ops?

_[No answer drafted yet]_

### Give a 5-minute demo of a tool or product that you know well.

_[No answer drafted yet]_

## 2.3 Technical scoping, implementation & troubleshooting

### Enterprise Software Implementation: "Can you walk me through a specific enterprise software implementation project you led? How did you handle unexpected technical or operational challenges?"

I began by thoroughly understanding the business objectives and the data points available from D&B through collaborative meetings with their team and our solution architect. From there, I defined the feature goals, scoped out exclusions, and established key success metrics. I also mapped out a logical user flow and partnered with the designer to create mockups, which were approved by our CEO to align with the company's strategic vision.

To ensure technical feasibility, I conducted refinement sessions with engineers, identifying edge cases and prioritizing high-effort tasks. During the project, we faced an unexpected challenge regarding how to display D&B data to INX customers. This required careful negotiation with D&B to balance their formatting standards with our need for a simplified user experience. I facilitated discussions to reach a compromise, ultimately delivering data in a way that maintained clarity for customers while respecting D&B’s requirements.

The integration was successfully delivered on schedule, and it improved the platform’s value proposition by offering richer insights to customers, enhancing decision-making capabilities, and increasing customer satisfaction.

### Data Modeling and Analytics: "How do you approach translating business requirements into data models and workflows for POCs or pilots? Can you share an example?"

I begin by thoroughly understanding the customer's business needs, motivations, desired outcomes, and existing processes or systems. This helps ensure the solution is tailored to their unique context.

Next, I lead workshops with a cross-functional team, including designers, data scientists, and solution architects, to ideate and define the architecture of the POC or pilot. These sessions ensure alignment across technical and business stakeholders.

I then conduct in-depth research to define data collection strategies that ensure high-quality, consistent data inflow. This includes understanding edge cases by engaging with internal and external (customer) actors to capture potential exceptions and constraints, ensuring the data model accounts for real-world variability.

For instance, I created a prototype digital chain of custody for Nespresso to track the provenance of organic coffee. The key business requirements were to ensure there was no infiltration or exfiltration of coffee and to trace it from origin all the way to Nespresso's warehouse in Switzerland.

- With the help of local designers and researchers on the ground in DRC, we mapped the coffee’s journey by identifying critical tracking events (CTEs) at transformation, transportation, and documentation points.
- I defined Key Data Elements (KDEs) for each CTE, such as weight before and after processing, the number of coffee bags, and related documentation.
- Working closely with a data scientist, we coded and tested the chain of custody system, integrating calculations and validation checks at each CTE to flag inconsistencies.
This structured approach ensures the pilot addresses the customer’s core requirements while setting the foundation for scalable solutions. By deeply understanding their business and delivering actionable insights, I help build trust and demonstrate the value of our solutions during the pre-sales phase.               

### Technical Troubleshooting: "Imagine a customer faces integration issues with their existing ERP system while implementing Pulsora. How would you diagnose and resolve the problem efficiently?"

- First, I reassure the customer that resolving the issue is my top priority and that I’ll work collaboratively with them to address the problem quickly and effectively
- I start by analyzing available data and prioritizing diagnostic activities based on effort and impact. My first step is to confirm that the integration meets the required data standards and specifications, as many issues stem from mismatches in formats or requirements.
- Next, I review customer support logs and tickets to identify patterns or previously flagged issues. I also sit down with the customer (virtually or in person) to walk through the problem, understand the failure point, and gather insights on how they arrived at this situation.
- I then communicate a clear timeline for resolution and outline any support or resources needed from the customer, such as access to proprietary databases, specific technical details, or the involvement of their technical team.
- Finally, I assign a dedicated team to address the issue and provide them with a focused mandate to resolve it within the agreed timeframe. I ensure open communication between all stakeholders to keep the customer updated throughout the process, maintaining trust and transparency.
- **REMEMBER TO REPLICATE THE ISSUE**

## 2.4 Objections, pushback & saying no

### Handling Rejections or Objections: "During a demo or meeting, if a prospect raises significant objections to the platform, how would you handle the situation and guide the conversation to a positive outcome?"

- Listen actively to the prospect’s concerns
- Acknowledge and empathize with them and their statements to build rapport
- Ask clarifying questions and probe deeper; ask them for what their ideal solve would be
- Clarify any misunderstandings about how the platform or product works – using analogies if helpful
- Address the objection in smaller parts – start with addressing the part that has the biggest probability of tanking the deal
- Reframe the objection – i.e. go from customer focus on cost to highlighting value to them
- Success stories, testimonials, case studies
- Offer different alternatives, and end with a positive call to action
- Example

### How do you figure out whether a technical objection is a real blocker or a stalling tactic?

_[No answer drafted yet]_

### A prospect says they want feature X but it’s not on our roadmap – what do you do in the call?

- I understand why they want that feature – what problem are they trying to solve

### Tell me about a time you had to push back on a sales rep who wanted to overpromise to a customer.

_[No answer drafted yet]_

### A time that you had to say no to a client for something they requested

- Had to say no to Stephanie at Nespresso who wanted an additional feature added in (the stoplight feature for the coffee traceability solution) and delivered on the same date as the rest
- If we change the scope, then we need to push out the due date or ask for more money. As neither of these were possible to move, I had to say no
- I did keep the functionality high in the backlog though

## 2.5 Managing client expectations & complex requirements

### Managing Client Expectations: "What strategies do you use to manage client expectations when a project encounters delays or unforeseen technical limitations?"

- Proactive communication and regular updates – be conservative when providing a timeline for completion
- Align the client on the long-term strategy and value
- Collaborative approach (let’s solve this together)
- Depending on the nature of the delay or technical difficulty, assign a dedicated team to resolve the issue
- Listen actively, with empathy, find out where else you can deliver value
- If all other measures have been exhausted and delays significantly impact the client, consider offering goodwill gestures such as a complimentary workshop, added features, or credits to reinforce the partnership.

### Handling Complex Client Requirements: "When faced with a client who has a long list of complex and sometimes conflicting requirements, how do you prioritize their needs and ensure they feel heard while aligning their expectations with the product's capabilities?"

- **Understand Business Goals and Context:**
  - I begin by understanding the client’s high-level objectives and their business goals for partnering with us. Are they a new client looking for quick value, or a strategic partner with specific needs? This context helps prioritize efforts and frame the conversation.
- **Gather and Clarify Requirements:**
  - I ensure I have a comprehensive understanding of their requirements by asking clarifying questions and identifying key pain points. This allows me to uncover the root issues and align their expectations early on.
- **Prioritize and Deliver Quick Wins:**
  - I identify quick wins—features or solutions that can deliver immediate value. This builds trust and confidence while creating momentum for tackling more complex or longer-term needs.
- **Educate and Align Expectations:**
  - When requirements conflict or fall outside the product’s scope, I educate the client on the product’s current capabilities, roadmap, and constraints. I provide a rationale for prioritization, showing how it aligns with their goals and delivers the best value.
- **Structure the Engagement in Phases:**
  - I propose a phased approach, outlining clear milestones and timelines for each phase. This ensures the client sees continuous progress while managing expectations and dependencies effectively.

## 2.6 Cross-functional collaboration

### Cross-functional Collaboration: This role involves working closely with Engineering, Product, and Sales teams. Can you share an example where you successfully managed competing priorities between a customer request and internal technical constraints?

- Nespresso wanted to scale the solution to 3 new cooperatives
- After conducting on the ground research to evaluate each potential site’s readiness to integrate the solution, we established that one of the sites was not ready
- The supply chain specifics were too different, the workers were seasonal, and the documentation was not the same – it would have cost too many resources and too much custom dev to make this site work
- So we came back to the customer and suggested to expand at 2 sites and conduct preliminary research at the 3rd, so as to be ready to expand to this site next season
- My role in all this was to organize and lead the research, facilitate the design workshops after the research trip. I also constructed the slide deck with the proposed approach to the customer, as well as the budget for the expansion and research activities
- I spoke with engineering leads and understood that the supply chain structure at the 3rd site would require a vastly different chain of custody as well as standalone database structures

## 2.7 Supporting the sales cycle & competitive positioning

### Driving Sales through Technical Expertise: How do you balance technical depth with a sales-oriented approach when engaging with prospects who have varying levels of ESG and technical expertise?

- **Assess the Room & Adapt the Approach**
  - **Pre-meeting research**: Review participant backgrounds via LinkedIn, company reports, and past interactions.
  - **Gauge expertise upfront**: Begin with quick discovery questions or a live poll to assess ESG and technical proficiency levels.
  - **Ensure the right stakeholders**: Request a mix of ESG and tech decision-makers, but **be prepared to adjust on the fly** if the audience leans heavily toward one side.
- **Frame the Conversation Around Shared Pain Points**
  - **Start broad, then go deep**: Open with **industry-wide challenges** that resonate across roles, then drill down into function-specific concerns.
  - **Link ESG and tech challenges**: E.g., “Many companies struggle with fragmented ESG data and regulatory reporting—how does that impact your team specifically?”
  - **Address business impact**: Show how ESG misalignment leads to **compliance risks, reputational damage, and operational inefficiencies.**
- **Position Pulsora as a Business Enabler, Not Just a Tool**
  - **Tailor messaging based on audience type:** 
    - For ESG professionals → Focus on **regulatory alignment, audit-readiness, and sustainability leadership**.
    - For tech professionals → Highlight **integration, automation, and data security**.
  - **Demonstrate quick wins**: Show how **minimal setup efforts** can lead to **fast compliance wins and efficiency gains**.
  - **Address potential blockers early**: Be ready to explain **implementation dependencies, data requirements, and scaling potential**.
- **Prove Value with Competitive Positioning**
  - **Showcase ROI**: Use **before-and-after scenarios** with quantified impact (cost/time savings, risk reduction, etc.).
  - **Leverage credibility markers**: Cite **ESG reports, case studies, awards, and analyst recognition**.
  - **Differentiate from competitors**: Clearly outline **where Pulsora outperforms others**, whether it’s in **flexibility, automation, reporting accuracy, or compliance coverage**.
- **Close with a Clear Call-to-Action**
  - Align next steps based on the audience’s interest and concerns.
  - Offer a **custom proof of concept or trial** based on their specific ESG maturity level.
  - If pushback arises, pivot by **addressing concerns with tailored use cases and success stories**.

### Competitive Positioning: How would you position Pulsora against competitors when speaking to a prospect who already has a partial ESG solution in place but is considering switching?

- We built pulsora for adaptability – while you can select from a number of pre-configured ESG frameworks and data catalogs, you can also prepare customized reports to fit your specific needs
- Pulsora is like a command center for visualizing sustainability data – dashboards, live tracking, automatic notifications for lagging metrics
- Flexibility and speed of delivery due to our smaller company size

### Supporting the Sales Cycle: Can you walk us through a time when you played a critical role in closing a large enterprise deal? What was your role in the sales process, and what made it successful?

- Yes, I helped close a large contract of over $23M with a utility called SCE
- I was the contracting engagement manager for the deal, responsible for negotiating the terms of the SaaS contract together with the sales exec
- The sales exec and I were successful because we played as a team – building off of what the other person says, meeting strategically before and after each engagement with SCE
- I collected and organized business requirements from a difficult buyer – I gained her trust by showing off my knowledge of the contract terms
- I came up with a way to significantly simplify some of the contracting terms, which made everyone happy

## 2.8 Customer success, retention & scaling

### Customer Success & Retention: After a customer has successfully implemented Pulsora, how would you approach their ongoing engagement to ensure continued adoption and minimize churn?

#### 1. Immediate Post-Implementation Engagement

- First, I assess the customer’s **support tier/package** and proactively insert myself into check-ins to ensure a smooth transition.
- I track whether the originally intended users are logging in and engaging as expected. If there are deviations, I reach out to understand why—whether it’s a training gap, a misalignment of needs, or an adoption issue.

#### 2. Ongoing Monitoring & Proactive Intervention

- I analyze **usage and engagement metrics**, benchmarking against both expected lifecycle milestones and peer companies to detect early signs of low adoption.
- If I see red flags—such as declining logins, limited feature adoption, or repeated support tickets—I proactively engage the customer to **re-align on their goals and ensure they extract full value** from Pulsora.

#### 3. Strategic Engagement & Value-Driven Retention

- I facilitate **goal-oriented QBRs** that focus on their business priorities rather than just product updates.
- I gather customer feedback and **contextualize it** before passing it to the Product team, ensuring they understand not just the request but its strategic impact on the customer’s business.
- I advocate for their needs internally and help them see the **long-term value** Pulsora can bring, reinforcing their decision to stay.

### Scaling Implementations in EMEA: Pulsora is expanding rapidly. How would you ensure consistency in implementations and support across different countries, considering regulatory differences and local customer needs?

#### 1. Establish a Centralized Knowledge Hub

- Create **country-specific spaces** in the company wiki and dedicated CRM sections for each customer.
- Maintain a structured **repository of implementation templates**, FAQs, and regulatory guidelines to ensure **localization without duplication of effort**.

#### 2. Foster Cross-Regional Learning & Best Practices

- Establish **regular knowledge-sharing forums** (dedicated Slack channels, monthly syncs) where teams working in the same region can discuss challenges, lessons learned, and customer feedback.
- Encourage a **culture of transparency**, where both wins and failed approaches are shared for continuous improvement.

#### 3. Standardize Where Possible, Localize Where Necessary

- Conduct **quarterly reviews** of implementation processes to identify areas for standardization across regions.
- Align these processes with **existing systems** (e.g., onboarding workflows, support escalation paths) while allowing room for country-specific adjustments.

#### 4. Segment Customers for Tailored Support

- **Define clear customer tiers**:
  - **Low-touch, low-revenue**: Self-service resources, automated onboarding.
  - **High-touch, high-value**: Dedicated CSMs, tailored implementation plans.
- Ensure that regional teams understand the **ideal customer profile** for each country to set realistic expectations early in the sales cycle.

#### 5. Implement a System for Tracking Regulatory Changes

- Develop an **organized, automated system** (e.g., alerts, compliance dashboards) to monitor evolving ESG regulations by country.
- Work with **local legal and compliance experts** to proactively adapt implementation strategies.

# 3. Product manager questions

## 3.1 Motivation & ways of working

### What do you enjoy about product management?

- The scientific approach - finding, organizing, and analyzing data to reach conclusions and make decisions
- The creative aspect - ideating solutions to pain points, new product and feature ideas, fresh marketing ideas to reach users
- The strategy - prioritizing and making decisions in a complex environment that takes into account users, company strategy, and external market forces

### What do you dislike about product management?

- The continuous context switching - it could eventually impact the quality of your work where you might deliver many outputs of lower individual quality
- The reliance on buzzwords and the latest trends - to be an engaging PM you have to apply the latest frameworks and product trends (even if those are not worth utilizing for your particular product)

## 3.2 Strategy

### Can you describe how you build a product strategy?

- Review the business strategy 
- Conduct market and competitor research 
- Conduct user research – identify opportunities and prioritize them according to company goals, business strategy and market indicators
- Create product vision and guiding product principles
- Collaborate with cross-functional teams to develop a roadmap to address opportunities now, next, or later
- At OpenSC, I helped create the product strategy for the digital coffee transparency solution
  - Research into competitor supply chain traceability tools 
  - Gained a thorough understanding of Nespresso’s business goals for achieving transparency in their supply chain 
  - Created a vision for the digital coffee transparency solution to provide visibility and levers for action into the journey of the coffee and into supply chain logistics
  - Product principles: near-real-time detection, solution fits closely into existing supply chain workflows and processes, high quantity of data, high quality of data
  - The solution was in its second year of operation, struggled from low quality data inputted into the platform, and there was not yet any customer-facing modules or tangible tool – so all of the analytic findings were communicated via slides
  - At the start of the data collection period, I focused on improving the quantity and quality of data – with the team we created a solution performance monitoring dash – and put in place some simple fixes that had the largest impact on quantity and quality
  - On the customer-end, we did some discovery with different stakeholders at Nespresso to understand which data findings and modules would be most used by the customer – we focused the data scientist’s effort on the top 3 high-value analytics and created some prototypes for the client to react to
So in the end we had 90% data collection success and much fewer quality issues

On the customer side, we got 4 more stakeholders at Nespresso and implementing partners to actually consult the product and think about ways it can be useful for them. 

### What inputs do you use to build your roadmap?

- Company goals and OKRs provided by senior leadership
- Estimation of technical feasibility provided by engineers
- Assessment of customer need or appetite provided by design
- Market opportunity provided by sales/marketing
- Regulatory/policy environment
- Availability of company resources
Roadmap at OpenSC for DRC:

**Now:** data collection platform with high quantity and quality of data, functional and easily repeatable verification processes (i.e. process for verifying farmer payments), supply chain analytic module prototypes, near-real-time analytics, tamper-proof records on Ethereum blockchain

**Next:** closer and closer to real-time analytics, alerts for ongoing infiltrations, assisted resolution mechanism in case of infiltration or failure point in the chain, turning the AAA scorecard spreadsheet into a dynamic dashboard, 

**Later:** CoC verification across other commodities (i.e. cocoa), getting rid of paper in the supply chain entirely, site selection tool for transparency solution roll-out, analytics to reduce waste and increase efficiency of coffee production process 

### What was the hardest decision you had to make as a product manager? How did you handle it?

- Whether to get rid of a legacy product feature in place of a more simplistic feature that would get the job done but might be less attractive to the customer
- **Situation**: the opensc digital transparency solution works by collecting supply chain data including the location of coffee and quantity of coffee per bag. Historically this was done by users scanning a QR code on each bag. However this method proved difficult – each bag had to be tagged and scanned individually and this proved to be too much effort for supply chain workers who were incentivized by their bosses to process the bags as fast as possible
- **Task**: with my team we started thinking about an easier mechanism for tracking bag data – leveraging the existing Android app and adding data input functionality for supply chain workers to enter number of bags and weight. We had to weigh the pros and cons of the traditional method vs. the new simplified method
- **Action**: We thought a lot about the tamperability of the new system – whether any supply chain actor could create false data out of thin air. There was also the fact that the QR code method provided individual bag traceability and there had been several PR campaigns about this – making it a part of the OpenSC DNA. But we thought: ultimately, what is the purpose of continuing a solution that nobody is using?
- **Result**: In the end we opted for a hybrid system that worked best with the supply chain workers and their JTBD. One bag in a batch of 20 would be tagged with a QR code, but the supply chain worker would input bag quantity and weight in the app

## 3.3 Design

### How do you ensure a product’s design meets both user needs and business goals?

- First build an understanding of business goals to narrow the problem, then focus on solving very specific user problems that can help move the needle on those goals – the business has to be the driving factor	
- At OpenSC, one of our business goals was to provide reliable near-real-time supply chain analytics  one of the metrics that feeds into this goal is the quantity, timeliness, and quality of data that gets uploaded to the platform
- With our supply chain data collection Android app, we were not collecting enough data, and a lot of the data we had had quality issues or came to us late
- We did some user interviews and realized there were some obvious design issues with the app that could be solved to address user needs and business goals 

### What’s the most challenging design problem you’ve faced and how did you overcome it?

- With the data collection platform at OpenSC, we had an issue with access to electricity (this is an issue with the design of the data collection mechanism – by using smartphones)
- The absence of electrical infrastructure such as wall chargers meant that some users’ phones were running out of battery, and the user was unable to charge up in order to collect data in a timely fashion 
- We did some ideation workshops and thought of solar-powered charging stations – however these were difficult to set up, were prone to theft, and the solution did not scale when dozens of users had to recharge their phones at the same time
- We landed on some user process design changes in the end – using a prioritization framework that took into account the infrastructure realities as well as the users’ JTBD and existing workflows
  - Set times that the user uploads their data to the OpenSC platform – in a designated office with electricity and internet access
  - Showed users how to activate battery saver mode on their phones
  - Training emphasizing battery saving

### How do you stay user-focused?

- **Problem definition level**
  - Focusing on the problem from the user’s standpoint
  - Referring often to the JTBD for the user in question
- **User research**
  - Ensure that everyone on the team can speak to the user at some point
  - Create user personas and also JTBD
  - Using visual tools like user journeys and user flows to experience things from the user’s perspective
  - Going beyond user interviews to doing useability testing, prototype screen recordings, or have the user walk me through their actions
- **Develop**
  - Use agile methods and put new versions of the product in front of users early and often
  - Gather feedback
- **Example**
  - When we updated the OpenSC Android app to make it more user-friendly, we created a clickthrough prototype and recorded users’ screens as they used it; we also had our field specialist record audio of them explaining their actions in real time
    - Situation: updating the OpenSC Android app to make it more user friendly
    - Task: needed to verify whether users would respond well to our new design; if it was going to save them time and increase quantity and quality of data
    - Action: we recorded users’ screen during a prototype click-through and also recorded audio of them explaining their actions
    - Result: We had plenty of data to understand how the new design would be received by users; we went ahead with the changes and saw a 38% increase in number of users

### How do you know if a product is well designed?

- It is clear in each screen what the intended action to be taken is
- If I have a certain use case I want to accomplish, it’s fairly obvious where I should navigate/click to accomplish it
- I stay in the product and my session duration is quite long – vs. dropping off
- I feel good after using the product – it has met my needs and positively impacted my feeling
- The screen load times are good, there are not too many clicks for me to complete an action

## 3.4 Develop & deliver

### How do you manage the trade-offs between speed of product execution and quality?

- I also think about a third element and that’s impact that the product has for the customer or users
- In my experience as a team lead, I find that it’s best to keep people focused on one thing at a time
- So, I make an assessment on what is lagging the most – speed of execution, quality, or impact
- When I was consulting with CXB Hub, the CEO wanted a polished MVP (which in my mind goes against the concept of MVP) to wow potential clients. The core component of the product was a Customer Experience maturity questionnaire. I convinced the CEO to test run the questionnaire with a batch of clients, so as to increase the speed of execution and get something in front of users quickly. We were able to fine-tune the questionnaire ahead of the MVP release

### Tell me about a product launch that didn’t go as planned. What happened?

- When we launched a customer-facing coffee journey experience for Nespresso, there was a component displaying the coffee farmers payment status for the coffee beans delivered
- However by the time the coffee journey launched the payments had not all been verified, and this made it look like Nespresso were not paying their coffee farmers
- We sat down with the client, then brainstormed design ideas with the team
- We came up with a stoplight system that would show payments as pending rather than incomplete – we also added the date for the upcoming verification 
- Customer was satisfied with this and the launch went forward with a minor tweak

### How do you decide what to build and what not to build? How do you prioritize features in a product backlog?

- I use a process that includes members of my team, so that the decision is arrived from a multi-disciplinary angle and has buy-in from the people who will build the features
- I go back to the high level business strategy, and look at the product vision and principles to help understand which features are a better fit
- I use prioritization frameworks depending on what our goals are for the product
  - RICE framework if we want to work on initiatives most likely to impact a specific business goal
  - Value-effort matrix
  - Kano method if you want to hear from customers directly about what they value (breaking down features into basic needs, performance needs, and excitement needs)
  - For the first 2 frameworks, it’s important to get the engineering teams in the habit of estimating effort for the features in the backlog
- At OpenSC, we prioritized based on what would give us better quality data and more data, and we sequenced and prioritized builds according to when our users would need to use them based on coffee harvest dates

### What do you need to consider when deciding how and when to launch your product into the marketplace?

- The launch style (whether it's a soft launch, minimal launch, or full-scale launch) is decided by a number of factors including budget and resources available, whether the product is an MVP or it has already been through multiple iterations
- The decision of when to launch a product depends on whether the product's success is season-dependent (for example launching a new ice cream flavor makes more sense in the summer), the state of the economy (i.e. launching a premium priced product during a recession is not wise), and whether there are competing products launching or circulating at the same time

## 3.5 Product performance & analytics

### Explain your approach to monitoring performance and success

- Setting up a clear success and performance monitoring plan from the get-go
- Include clear KPIs aligned with product goals and objectives, and a plan for when and how to collect the necessary data
- Create an end-state product vision, with milestones for getting there and success parameters at each milestone
- Use data analytics tools to track usage statistics and identify trends, patterns, or recurring bugs and performance issues
- When relevant, create a quality management plan to ensure that you’re not only hitting the hard metrics, but also maintaining the quality of the product and user experience at the same time
- Incorporate feedback from customers through surveys, interviews, and user analytics

### Product analytics often involves working with cross-functional teams. Can you share an example of how you’ve collaborated cross-functionally to leverage data insights for product development and optimization? What was the outcome?

- Sure
- I helped package some supply chain data insights for one of the OpenSC customers we worked with
- Based on interviews with the customer, I defined a set of KPIs and insights that the customer would find interesting
- I worked with a solution architect to identify the data sources, methods of data extraction and transformation to arrive at the insights
- I worked with a data scientist to build the data logic linking the different steps of the supply chain together to enable more complex calculations of certain insights
- I built a set of dashboard prototypes with a product designer that we presented to the customer

### How do you determine which product metrics are most relevant to track for a particular feature or product enhancement?  Can you provide an example of how you’ve prioritized these metrics previously?

- What do we aim to achieve with the feature – what are the objectives?
- Identify KPIs that reflect progress toward achieving objectives as well – conversely, good to think of what the failure point is for a feature and track the path to that (to prevent it)
- User needs - Think about who is using the feature – then build your metrics around the user and their experience, feeling toward the feature
  - Think about functional, non-functional, and design requirements and metrics for each of these
- Evaluate technical feasibility of tracking and measuring metrics, then prioritize them based on their impact on achieving the feature/product objectives 
- **Example**:
  - At OpenSC we were thinking of product metrics for the supply chain data collection tool
  - We identified with a designer the current pain points with the tool
  - We went through a HMW exercise with a designer and SA
  - We ideated new features
  - For each feature, we thought of 1 or 2 metrics to 

## 3.6 How-would-you product questions

### What’s your favorite product and why?

Miro

- Miro has tapped into the remote work trend and made it very easy for teams to collaborate virtually
- Miro has a very intuitive onboarding process and a product-led growth strategy that ends up roping in entire tech teams
  - It helps that it is a first of its kind product in a new category, so there are no costs of switching from incumbents
- Miro can be used by any department and is intuitive for non-design users (I use it as a PM to create prototypes)
- Great selection of templates that lowers the barrier to entry and also allows for user-generated content
- It’s fun to use and feels like childhood somehow

### How would you improve your favorite product?

_[No answer drafted yet]_

### Imagine a product is underperforming in the market. What steps would you take to address the situation?

- Look at the product goals and success metrics if available – find out where the product is underperforming
- Assess any recent market changes or technological developments that could cause performance issue, look at other factors outside of your control like regulatory issues
- Come up with a list of hypotheses for what is going on, and potential solutions
- Test the hypotheses through research, validate the assumptions
- Once a solution has been chosen, set up some new success metrics, track progress, and then track the level of success


### Choose a software product you enjoy using and describe one way that it could be improved and how you would determine if that improvement was worth developing?

- I used Amazon QuickSight in my last job and it was a great tool for producing charts and graphs from datasets 
- Unfortunately, the onboarding onto the tool was very difficult due to the security features and the different levels of user permissions, the architecture of which was not clear at all
- The onboarding, user registration, and user login journeys could all be improved
- I would determine if this is worth developing by looking at user feedback and the time to initial registration (i.e. from the time a user receives an invite link until they have successfully created their account)

# 4. Technical & engineering collaboration questions

### What’s your take on Agile?

- It doesn’t work so well when you have a set deadline with functionality that must be released at all costs by a certain date
- It’s nice that you can borrow bits and pieces of agile to improve processes in your product development flow
- It’s great for getting dev teams in the habit of continuous delivery, and sales and designers (and customers) in the habit of continuous discovery 
- In the retros it’s not enough to make an observation about something that’s not working – people have to be held accountable to actually make the changes happen
- Estimations by engineers are important
- Working prototypes and testing those with customers are important

### What’s your experience with Agile?

- Kanban with dev teams at OpenSC
- Developing prototypes and MVPs (at OpenSC, CXB HUB)
- Delivering work in sprints with my pod and doing retrospectives at the end

### How do you integrate technical teams into the product vision effectively?

- Share product vision materials (i.e. product concept document, product vision statement, product values) regularly and ask for input
- Invite them to co-create with you
- Sell them on the current and future state of the technology and technical capabilities of the system – get them excited about delivering something entirely new
- If there is one particular technology team member with sway over the others, focus on getting them sold on the idea (find out about their interests and preferred ways of communicating)
- DO NOT tell the technical teams what to do – come to them with problems and tie it back to ongoing customer discussions (the take-aways from which you should share with them) and to the evolving product strategy
- After I kicked off a new season of the supply chain solution with Nespresso, I delivered the same presentation (giving the strategic highlights) to the technology teams – to get them on a level playing field with the customer

### How do you bridge the gap between market-oriented teams and technical challenges? (i.e. How do you reconcile the often differing perspectives and priorities of these two types of teams to ensure successful development and delivery?)

- When trying to scope a software project, understand the natural objectives of these two teams: market-oriented teams will try to scope a simple project that brings revenue in as soon as possible while delivering a cohesive product story; technical teams will prioritize a high quality software launch free of bugs and in alignment with the existing technical infrastructure
  - When dealing with market teams, craft a cohesive narrative that takes into account the technical needs of the project while also making it an appealing story for the customer
  - When dealing with technical teams, share the high-level project restrictions including timeline, client expectations, what was sold – get them to think about more than just the technical department and about the business imperatives
- It might make sense to invite technical team members to sit in on some customer calls to build empathy
- Bring a well-spoken technical team member to early scoping meetings with the customer’s technical point person – use the technical teams to provide reassurance and domain expertise 
- Put in place a process that market-oriented teams have to follow – technical checks to be made, requirements gathered from the customer, etc.  – throughout the sales cycle – make it a playbook and tell them that doing this little by little will result in a shorter sales cyle overall – rather than doing it all in one go
- At Opower I was working hand in hand with sales reps but I also interfaced with technical project managers, solution architects, and engineers on difficult software deals or professional services – I had to constantly mediate between these two teams

### How do you foster a culture of continuous delivery with your team?

- Keep the backlog updated and refreshed
- Communicate customer learnings back regularly; invite engineers and team members to customer meetings to spark new ideas
- Create a way for people to submit product ideas or product fixes; clean and structure the ideas and add them to the backlog 
- Get in the habit of doing continuous discovery with customers and users, and getting them to react to prototypes and MVPs so that your devs can continuously build and release – use agile methodologies
- Opt for shorter sprints and celebrate/officially close them to introduce a sense of accomplishment and momentum
- Use a roadmap to keep everyone aligned, focused and moving
- Prioritize automation for repetitive tasks to keep the focus on features and updates
- With one of the engineers we were working on updating database queries to produce more accurate insights. This was a constant effort and we got into the habit of continuous delivery – setting data hygiene objectives, running quick sprints, delivering the new functionality and assessing the positive impact on the data insights

### How do you optimize your interactions with engineers?

- I spend time to understand in depth their existing workflows, tooling, and practices
- I try to fit in as much as possible into their existing process – adding checkpoints or an additional meeting to bring a more strategic product management aspect into it
- I leave the delivery and product ownership to the engineers or to the product owner – my role is delivering value and viability
- I get out of the way of engineers by letting them do what they do best – DEVELOP and DELIVER
- I provide high-level frameworks and delivery timelines to keep them on task – **I involve them in decision-making processes**
- I try to understand the current state of software/product development and if there is a future state in mind (more agile? More scrum? Continuous delivery?)
- I bring in as much helpful structure and explanation to my JIRA tickets and other work products that I hand over (including specs, wireframes, acceptance criteria, etc.)
- I send agendas ahead of meetings and I explain objectives clearly
- I share customer and user’s reactions to their products and features – they need to experience full-circle what they have achieved
- **Regular stand-up meetings and sprint reviews**
- At OpenSC I created a standard format for user stories in collaboration with a few of the engineers – this way there was an expected and repeatable way to write them

### What are the key technical challenges in developing a new product?

- Choosing the right technology stack
- Finding efficient methods to utilize the current database architecture and integrate API calls within the existing code structure – i.e. how to minimize technical debt
- Mapping technical dependencies
- **Scalability as user load grows**
- **Integration with existing systems to enable interoperability**
- Fulfilling all of the requirements for external inputs, data, information necessary from customers, users or partners to ensure that the product functions properly
- Choosing a development approach and ceremonies
- Developing technical documentation! How much, when, who?
- Estimating dev effort required when prioritizing features
- Dealing with changing requirements on the go – i.e. Android app needs to be supported on a new type of phone
- Predicting what kind of bugs or malfunctions may surface once the product is live and coming up with resolution plans
- Think strategically about when to sunset the product and the technical needs around that

### What’s the toughest technical feature you’ve worked on?

- Figuring out the logic for calculating CoC validation at different steps in the supply chain map for the Nespresso coffee
- Collaborated with the data scientist and solution architect to define the calculations and correct data requests which have to be made in order to verify that the totality of the coffee is preserved at each supply chain step, despite transportation and transformation events
- Weight of the coffee bags, type of coffee in the bags, location of the coffee along the supply chain, batch number that the bag belongs to, etc.
- Then finding a visual way to display this to the customer (we ended up using bar graphs), including any discrepancies – and how these might be explained by missing data  

# 5. B2B SaaS questions

### What is your experience in B2B SaaS?

- I helped build an innovative supply chain transparency platform – when I left it had secured its first recurring revenue contract (for a different commodity). 
  - I built a strategy for handing over the solution to implementing partners, and got them to take on some of the implementation cost
  - Secured 2 contract renewals from Nespresso for the solution in DRC 
  - I helped assemble the onboarding toolkit and I cut onboarding costs 4x
  - I onboarded 2 coffee trading companies onto the OpenSC platform
- I helped manage contracting of SaaS software deals (and custom prof. services) for an established SaaS company
  - Assembled product and feature package for each client based on sale made by sales execs – defined customization for the customer over multiple year programs
  - Shared data standards, and products and technical briefs with customers – provided feedback to product marketing and knowledge management teams to update the briefs
  - Explained SaaS pricing model and subscription benefits to clients and scoped additional work or professional services for any non-standard customer requests
  - Assembled payment terms section in the contracts according to SaaS revenue recognition principles (in partnership with Finance team)
  - Negotiated contracts together with sales reps

### What are the key challenges associated with B2B SaaS products and how do you address them?

- Long sales cycle
  - **Address**: develop off-the-shelf sales materials/whitepapers/product briefs, create sales playbooks with repeatable processes, identify the champion within the buyer organization, identify budget pools quickly, look into high-value unlocks (i.e. addressing regulatory constraints in the buyer’s jurisdiction)
- Finding the balance between a custom solution for a few companies vs. building standardized to expand the customer base
  - **Address:** Build primarily for one company first, then identify similar companies who can benefit from a similar suite of products
- Customer onboarding can be timely and resource-intensive as the products can be more complex
  - **Address:** develop comprehensive onboarding materials, tutorials, offer personalized support as necessary
- Setting up robust data privacy and security expected by enterprise clients
  - **Address**: market research to understand the full operational challenges, rules and regulations that clients are subject to – develop tooling accordingly and use it as a USP where appropriate. Regularly assess, stress-test, and update security protocols to meet evolving threats
- Clients reluctant to change from legacy systems to new systems. There is a need to integrate with sometimes complex existing systems and workflows.
  - **Address**: prioritize integration capabilities and invest in robust APIs to ensure compatibility. prepare technical briefs detailing ETL processes, invite solution architects to meetings, prepare a thorough data migration plan as part of the sale/product packaging
- Scalability: B2B SaaS products need to scale effectively and accommodate the growth of customers
  - **Address**: build the architecture with scalability in mind, leveraging cloud infrastructure; create scalability performance metrics and monitor closely as user base grows

### How do you prioritize feature development for a B2B SaaS product?

- Features are usually prioritized according to 3 factors: impact, effort, and time
- Assessing impact of B2B SaaS features
  - Does the feature drive customer success and reduce churn? (good to prioritize recurring revenue streams)
  - Will it shorten the time to value? Make onboarding easier
  - Will the new feature enhance scalability, optimize resource utilization, and improve performance?
  - Does the new feature enhance integration capabilities, support customization, or facilitate interoperability with other software?
- Assessing effort required to build B2B SaaS features
  - Does it require a significant deviation from the roadmap or established product suite?
  - Will it require a lot of adjustment to fit in to the minimum set security and regulatory standards?
- Taking the component of time into account
  - Which features will enable you to jump past several stakeholders to make the sale faster? (i.e. goes directly to champion user?)

# 6. Sustainability, ESG & value chain questions

### Can you share your understanding of emerging value chain data ecosystems, especially in the context of Digital Product Passports and their relevance to the li-ion battery industry?

- There is a lot of data being generated and produced in today’s value chains
- There is less data upstream at the source of production, but as the product is refined along the value chain and moves downstream closer and closer to customers there is more data
  - Purchasing agreements, purchase receipts
  - Proof of delivery, stock keeping data
  - Shipping documents (bills of lading)
  - Quality and quantity data
  - Audit and conformance/compliance data
- Unlocking the value behind all of this data relies on the establishment of smart automated data collection, sanitization, and analysis. Paired with blockchain you can provide a tamper-proof record of supply chain activity 
- Value chain transparency and traceability can fulfill sustainability goals by reducing waste, verifying organic production and product purity. It can also fulfill business goals by identifying inefficiencies in logistics and value chain operations, points of failure, etc.
- Digital product passports are a regulatory mechanism but also a signifier to consumers, not unlike the grade on cereals for healthiness and nutrition. The demand for li-ion batteries is only growing, and the sourcing of the core material is tied up with a lot of conflict in the source countries/regions

### 2. Market Research and Analysis:

**How would you approach conducting market research and competitor analysis to inform the business case for a new product, particularly in an industry with evolving environmental and social considerations like ours?**

- I would make a research plan with well defined research objectives, questions, and criteria
- Political, Economic, Social, Technological
- I would start with the regulatory environment as this drives a lot of the decision-making around supply chains and ESG strategy – what are the recent developments in RCS Global’s target markets and industries?
- Market research – look at some of the big sustainability councils and supply chain management associations and their recommendations, latest research, etc. (start with the ones which our past and existing clients are part of)
- Competitor analysis – look at pure Climate and Supply Chain tech players as well as consultancies and advisory firms with tech products
- Look at the consumer angle – research studies with consumers and their tolerance or appetite for supply chain transparency insights and products
- Innovative tech – look at the latest developments in supply chain tech, AI, blockchain

### 3. Cross-functional Collaboration:

**Can you provide examples of how you've effectively collaborated with technical teams, internal stakeholders, and external partners to align product development with business goals and customer needs?**

- Iteration of the coffee transparency solution with Nespresso’s partners in DRC

### 4. Leadership and Team Collaboration:

**Describe a challenging situation where you had to lead a cross-functional team across different geographies. How did you ensure effective communication and collaboration to meet project deadlines and objectives?**

- Running discovery and user research at the start of the DRC coffee season
- Hiring design researcher in DRC
- Developing research and interview guides in Berlin
- Coaching and following our field team in DRC
- I made a research plan and timeline together with the strategic designer
- Weekly sync-up calls with our field team and with the researcher
- Setting up workspace with Miro boards, etc.

### 5. Stakeholder Engagement and User-Centric Design:

**How do you prioritize user and customer requirements while balancing the needs of various stakeholders, including sales, business leadership, and technical teams?**

- Already answered

### 6. Product Strategy and Roadmapping:

**Can you walk us through your approach to developing and maintaining a detailed product strategy and roadmap, ensuring alignment with the company's vision and strategic objectives?**

- Already answered 

### 7. Sales and Marketing Collaboration:

**How would you collaborate with sales teams to develop pricing and positioning strategies for a new product launch, particularly in the context of sustainability-focused solutions?**

- Develop a positioning statement explaining the target customers, their unmet needs, and the proposed solution 
- Understand from sales what is the existing sales cycle, customer base, etc. See if there is a natural overlap in customer base for the new product
- I would make a presentation for the GTM strategy including:
  - Early adopter segments
  - Branding 
  - Channel strategy – will need lots of input on this as there are maybe some established channels here
  - Results of any tests of marketing methods (beforehand I would run some A/B tests through Facebook ads or run a survey by our customers)
  - Targets for CLV and CAC

### 8. Adaptability and Innovation:

**Our industry is rapidly evolving. How do you stay informed about emerging trends and technologies, and how would you apply innovative approaches to product development and problem-solving within our organization?**

- Newsletters, blogs, meetups, conferences, webinars
- Dedicate some time each month to do this
- Summarize, write, share with the rest of the company in Slack and during team meetings – try to generate some discussion and ideas
- Bring the innovative approach or model into the product development cycle, as a consideration
- If it’s worth pursuing, develop a prototype and try a proof of concept with a sliver of the supply chain/product in question

### 9. Business Development and Revenue Generation:

**How would you contribute to business development efforts, ensuring clarity of the business case for new products and identifying potential new clients or partners for technical collaboration?**

- I would develop a Go-To-Market strategy, with a well researched business case. I would emphasize:
  - Product’s positioning versus competitors in the market
  - Early adopter segments
- Detail the product concept and business/value case in any proposals or pitches
- Share any knowledge I have regarding potential funders, ecosystem players, sources of funding
- Recommending partners for technical collaboration and implementation – doing the viability assessment and business planning around this

### 10. Sustainability and Impact:

**Given our commitment to sustainable practices, how would you ensure that the products you manage align with our company's vision of generating sustainable positive impacts on people and the planet?**

- Incorporate the company vision and product vision into my product principles
- Remind my team members of the product principles at the start of any ideation or prioritization workshop – use the principles as an important factor when prioritizing features
- Incorporate sustainable impact/outcome into my product success metrics. For example for the digital battery passport:
  - Adoption by key players in battery production space
  - Average carbon footprint measurement per battery
  - Average circularity & resource efficiency grade per battery

# 7. Experience bank: examples and evidence

## Best Solutions Engineering examples

- Demo-ing our latest insights and any dashboard builds to Nespresso
  - Latest insights including the new ‘below threshold’ coffee farmer payments, solution data coverage statistics, and close-to-real-time infiltration detection 
- Building the CoC validation product with our data scientist and a solutions architect
  - Understanding the chain of custody model that is at play in the supply chain
  - Mapping the critical tracking events along the supply chain (i.e. where the coffee changes hands, is transported, or is transformed)
  - For each event, mapping the key data elements including weight, number of bags, 
  - Coming up with reference ‘conversion rates’ explaining what is the expected conversion of volume of coffee at any one stage
  - Coming up with a data sanitization policy and flow, to identify which data are definitely user error and which need to be further investigated to rule out any infiltration or exfiltration
- Discovery interviews with Nespresso and with coffee traders
  - What are the points in the supply chain where you don’t have enough visibility
  - How well does the current reporting mechanism work for you – what features do you wish you could have
  - How robust and trustworthy do you need the verification of source origin or of payment delivery to be – what are the deciding factors
- Discovery with procurement professionals at WEConnect International	
  - What are the key KPIs of your supplier diversity & inclusion program?
  - Where are there existing diverse suppliers? In which markets or verticals?
  - What is your capacity/what are the resources you can use to 
- Flowing technical feedback from our users (agronomic workers) back to engineering team
  - Coming up with user feedback surveys and distributing to users
  - Sharing the feedback via a workshop with the engineers
    - Summary screen to enable users to see what data they have submitted, or to delete corrupt data
  - Quick fixes prioritized for the next version of the android app
- Coming up with human-centered design ways to boost adoption of android app by agronomists and other supply chain workers
  - Eliminating a very time-consuming step in the app, relying where possible on existing digital files containing supply chain data
  - Looking closely at the the user’s JTBD and the flow of their work in the supply chain
  - Limiting the number of times the user has to upload data
  - Increasing usability of the app
  - Relying more heavily on the agronomist supervisor and other supply chain supervisors to ensure the app is being used

## Technical experience

- My **STRONG SUITS**
  - The software development lifecycle, effective collaboration with engineers, agile sprints (sprint planning from backlog/define sprint goal, refine backlog, daily standup, sprint execution, sprint review [show completed work], sprint retro)
  - Interpreting data and fashioning/communicating insights to customers
    - Also: communicating implementation specifics and contract terms/technical implementation details to customers
  - Setting business goals and KPIs, creating a data pipeline to track progress against KPIs
  - SQL and Python pulls from databases
  - Playing around inside business intelligence tools like Amazon Quicksight
  - Designing dashboards
  - Designing integrations and working with structured data standards and processes
- Scoping and designing a third party integration with a data partner/working with a solution architect to design the user flow, authentication protocol, and specifications around data storage and retrieval 
- Writing a spec to enhance the supplier engagement tool – user stories and acceptance criteria for different parts of the webpage/website
- Understanding and following the testing and development process for a new AI feature for an INX carbon management product
- Building a digital chain of custody and improving the quality of a machine learning model
- Together with a designer and solution architect, designing a product performance dashboard including which data points to collect, how to collect them, and which metrics to calculate and show on the dashboard – we then demo’d the dashboard to our partners and made parts of them accessible
- Troubleshooting code and data pulls and transformation together with an engineer
- At Oracle Utilities – analyzed and pulled data from Salesforce to calculate statistics about the sales and contracting cycles

## Pre-sales and Sales experience

- **OpenSC: building a new solution delivery model and pitching it to Nespresso and implementation partners**
  - Crafting the current year and future year’s budget to show diminishing costs
  - Delineating the division of responsibilities between OpenSC, Nespresso, and the implementing partners
  - Spelling out the value at each phase of the partnership, and aligning the group on a long-term vision
  - Demo-ing supply chain insights dashboards to sustainability leaders and getting their feedback 
  - Onboarding a new customer (Volcafe) onto the OpenSC platform
  - Creation of POCs and prototypes 
- **WEConnect International:**
  - Facilitating strategic diversity & inclusion workshops with senior business stakeholders – using knowledge management and smart content generation to influence companies to sign up as paying members of WEConnect International
  - Writing proposals, program pitches, and budgets to our biggest funder
  - Bringing together a coalition of companies concerned with the topic of supplie diversity & inclusion – nurturing that community to encourage donation of time, effort, and other resources
  - Leading pitch meetings at the World Bank, in Bangladesh with prospective members/signatories
- **Oracle Utilities** 
  - Part of a pre-sales team, working hand in hand with sales execs to scope deals, and negotiate and sign contracts with utility companies
  - Analysis in salesforce of time spent in different sales and contracting stages
  - Streamlining the contracting process; educating sales counterparts; communicating with different teams to validate the deal specifics and ensure a good kickoff
- **The Asia Foundation**
  - Drafting proposals and program budgets
  - Responding to RFPs and RFIs
- Technical scoping expertise
  - Working with solution architect to scope 3rd party integration with D&B at INX
  - Functional requirements and refinining process with engineers at INX
  - Scoping and building a product performance dashboard at OpenSC
  - Building the digital chain of custody model with data scientist at OpenSC
  - Scoping the solution set for Volcafe with a designer at OpenSC, based on our onboarding SOP
  - Scoped professional services work, gathered requirements, gathered estimations at Oracle Utilities
    - ETL, data migration, API integration, web portal customizations, etc.
  - **Involves user flow, mapping the data model/data architecture with a solution architect or data engineer, gathering non-functional requirements from engineers, coming up with broad set of products and services necessary for an onboarding/rollout, gathering estimates for work from engineers, translating business into technical requirements.** 
    - **Explaining to business buyers why certain data standards and restrictions are present** 
- Experience with POCs and pilots
  - Built an MVP for CXB HUB
  - Managed preliminary research and design for a pilot in Uganda at OpenSC
  - Piloted the use of solar-powered chargers for smartphones in DRC at OpenSC
  - POC for crowdworking platform at TAF
  - Piloted new QR code labels for a traceability solution, as well as a new process for attaching the labels at OpenSC
  - Built a digital chain of custody prototype before building out customer-facing modules

# Appendix: Questions still to answer

- What was your last set of performance feedback improvement areas?
- What was your responsibility at AstroFinance with regards to the product?
- How would you improve your favorite product?
- How do you figure out whether a technical objection is a real blocker or a stalling tactic?
- Give a 5-minute demo of a tool or product that you know well.
- How do you tailor a demo differently for an engineer vs. a VP of Ops?
- Tell me about a time you had to push back on a sales rep who wanted to overpromise to a customer.
