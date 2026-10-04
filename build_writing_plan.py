#!/usr/bin/env python3
"""Build a 4-page domain-writing income plan for Nicolas Picard."""

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Twips

GREEN = RGBColor(0x1B, 0x3A, 0x2F)
GREEN_MID = RGBColor(0x2D, 0x6A, 0x4F)
INK = RGBColor(0x1A, 0x1A, 0x1A)
MUTED = RGBColor(0x3D, 0x4A, 0x45)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RULE = "1B3A2F"
ZEBRA = "F3F6F4"
HEAD_FILL = "1B3A2F"


def shade(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = tcPr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tcPr.append(shd)
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")


def set_cell_margins(cell, top=40, bottom=40, left=70, right=70):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.find(qn("w:tcMar"))
    if tcMar is None:
        tcMar = OxmlElement("w:tcMar")
        tcPr.append(tcMar)
    for m, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = tcMar.find(qn(f"w:{m}"))
        if node is None:
            node = OxmlElement(f"w:{m}")
            tcMar.append(node)
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")


def set_table_widths(table, widths_cm):
    table.autofit = False
    table.allow_autofit = False
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement("w:tblPr")
    tblW = tblPr.find(qn("w:tblW"))
    if tblW is None:
        tblW = OxmlElement("w:tblW")
        tblPr.append(tblW)
    total = int(sum(widths_cm) * 567)
    tblW.set(qn("w:w"), str(total))
    tblW.set(qn("w:type"), "dxa")
    grid = tbl.find(qn("w:tblGrid"))
    if grid is not None:
        for child in list(grid):
            grid.remove(child)
    else:
        grid = OxmlElement("w:tblGrid")
        tblPr.addnext(grid)
    for w in widths_cm:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(int(w * 567)))
        grid.append(gc)
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcW = tcPr.find(qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW")
                tcPr.append(tcW)
            tcW.set(qn("w:w"), str(int(widths_cm[i] * 567)))
            tcW.set(qn("w:type"), "dxa")


def prevent_row_split(row):
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    cant = OxmlElement("w:cantSplit")
    trPr.append(cant)


def set_run_font(run, name="Calibri", size=10, bold=False, color=INK, italic=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def add_text(p, text, **kwargs):
    r = p.add_run(text)
    set_run_font(r, **kwargs)
    return r


def para(doc, text="", size=10, bold=False, color=INK, space_before=0, space_after=4,
         italic=False, align="left"):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.02
    if align == "justify":
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if text:
        add_text(p, text, size=size, bold=bold, color=color, italic=italic)
    return p


def rich(doc, runs, space_before=0, space_after=4, align="left"):
    """runs: list of (text, kwargs)"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.02
    if align == "justify":
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for text, kwargs in runs:
        add_text(p, text, **kwargs)
    return p


def heading(doc, text):
    p = para(doc, text, size=12, bold=True, color=GREEN, space_before=8, space_after=2)
    pPr = p._p.get_or_add_pPr()
    pPr.append(OxmlElement("w:keepNext"))
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), RULE)
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def bullet(doc, lead, rest, space_after=2):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.02
    pf.left_indent = Cm(0.35)
    pf.first_line_indent = Cm(-0.35)
    add_text(p, "•  ", size=10, color=GREEN_MID, bold=True)
    if lead:
        add_text(p, lead, size=10, bold=True, color=INK)
    add_text(p, rest, size=10, color=INK)
    return p


def fill_cell(cell, text, bold=False, size=8.5, color=INK, fill=None, center=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_text(p, text, size=size, bold=bold, color=color)
    set_cell_margins(cell)
    if fill:
        shade(cell, fill)
    # vertical align
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    vAlign = tcPr.find(qn("w:vAlign"))
    if vAlign is None:
        vAlign = OxmlElement("w:vAlign")
        tcPr.append(vAlign)
    vAlign.set(qn("w:val"), "center")


def fill_cell_runs(cell, runs, fill=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    for text, kwargs in runs:
        add_text(p, text, **kwargs)
    set_cell_margins(cell)
    if fill:
        shade(cell, fill)
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    vAlign = tcPr.find(qn("w:vAlign"))
    if vAlign is None:
        vAlign = OxmlElement("w:vAlign")
        tcPr.append(vAlign)
    vAlign.set(qn("w:val"), "center")


def make_table(doc, headers, rows, widths):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    set_table_widths(table, widths)
    for i, h in enumerate(headers):
        fill_cell(table.rows[0].cells[i], h, bold=True, size=8, color=WHITE, fill=HEAD_FILL)
    prevent_row_split(table.rows[0])
    for r_i, row in enumerate(rows):
        fill = ZEBRA if r_i % 2 == 0 else "FFFFFF"
        for c_i, val in enumerate(row):
            fill_cell(table.rows[r_i + 1].cells[c_i], val, size=8, color=INK, fill=fill)
        prevent_row_split(table.rows[r_i + 1])
    # tighten borders
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "D5DDD8")
        borders.append(el)
    tblPr.append(borders)
    return table


def add_footer(doc):
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(2)
    add_text(
        p,
        "Domain writing plan  ·  Nicolas Picard  ·  Berlin  ·  October 2026     ",
        size=8,
        color=MUTED,
    )
    # page number field
    run = p.add_run()
    set_run_font(run, size=8, color=MUTED)
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1)
    run._r.append(instr)
    run._r.append(fldChar2)
    add_text(p, " / ", size=8, color=MUTED)
    run2 = p.add_run()
    set_run_font(run2, size=8, color=MUTED)
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr2 = OxmlElement("w:instrText")
    instr2.set(qn("xml:space"), "preserve")
    instr2.text = " NUMPAGES "
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    run2._r.append(fld1)
    run2._r.append(instr2)
    run2._r.append(fld2)


def build():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.35)
    section.right_margin = Cm(1.35)
    section.top_margin = Cm(1.15)
    section.bottom_margin = Cm(1.2)
    section.header_distance = Cm(0.4)
    section.footer_distance = Cm(0.4)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10)
    normal.font.color.rgb = INK
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    # Title
    para(doc, "Domain writing as income", size=18, bold=True, color=GREEN, space_after=0)
    para(
        doc,
        "A one-year test before the psychotherapy master’s  ·  Nicolas Picard  ·  Berlin  ·  October 2026 – September 2027",
        size=9,
        color=MUTED,
        space_before=1,
        space_after=4,
    )

    heading(doc, "1.  The number you are actually chasing")
    rich(
        doc,
        [
            (
                "€2,500 net is about €5,200 invoiced per month",
                {"size": 10, "bold": True},
            ),
            (
                " (€62,000 a year). For a single filer in Berlin with no church tax and ordinary expenses, that is the level at which income tax plus health and care insurance leave roughly €2,500 in pocket. The Künstlersozialkasse, if it accepts you as a writer, charges about half the insurance rate and also builds a pension, so take-home stays similar and the coverage is better. A Steuerberater confirms this in week one, including whether 2025 fractional invoices already pushed you over the Kleinunternehmer line (prior-year turnover under €25,000, and this year under €100,000). Above that line, invoices carry VAT.",
                {"size": 10},
            ),
        ],
        space_after=3,
        align="justify",
    )
    rich(
        doc,
        [
            (
                "How a €5,200 month is built: ",
                {"size": 10, "bold": True},
            ),
            (
                "two monthly retainers inside one niche. A blueprint is a single document, and the job ends. A retainer is the same client, the same fee, every month. Ten to twelve writing days a month is the cap. AstroFinance and Dialectica can pay while the niche is forming. Judge the year on whether two supply-chain climate clients have hired you more than once. Pull the calendar forward if the master’s starts before October 2027.",
                {"size": 10},
            ),
        ],
        space_after=2,
        align="justify",
    )

    heading(doc, "2.  One offer, from seven CVs")
    rich(
        doc,
        [
            (
                "The overlap is specific. ",
                {"size": 10, "bold": True},
            ),
            (
                "You turn complex B2B products in climate, supply chain, and real-asset finance into documents a buyer, an investor, or an implementation team can use. That is already how you have been paid: Opower recognized you as the team’s best writer on large SaaS scopes; The Asia Foundation proposals; OpenSC playbooks and the Nespresso ESG business case; the IntegrityNext carbon-accounting flow, including upstream data gaps; the AstroFinance litepaper (product, strategy, three offerings, and the financial models), plus the exit memo and deal blueprints; a FIBE talk; the Carbon Accounting Alliance roundtable you are about to moderate; and Dialectica, which already pays for your judgment on supply-chain risk platforms.",
                {"size": 10},
            ),
        ],
        space_after=3,
        align="justify",
    )
    rich(
        doc,
        [
            (
                "Public sentence, on LinkedIn and on the offer sheet: ",
                {"size": 10, "bold": True},
            ),
            (
                "“I write the explainers and implementation pieces that supply-chain climate software teams use to sell and roll out their products.” The seven CV variants stay in the job-search folder. Clients hire the sentence, and they will check it on nicolaspicard.carrd.co.",
                {"size": 10},
            ),
        ],
        space_after=2,
        align="justify",
    )

    heading(doc, "3.  One niche, and what sits beside it")
    bullet(
        doc,
        "The niche is supply-chain climate software. ",
        "This is the repeat business. Vendors that sell supplier compliance, traceability, and carbon data need a new explainer whenever the rule or the product moves, which is often. Your long proof is here: Nespresso traceability in DR Congo, OpenSC playbooks, IntegrityNext’s supplier tool and carbon feature, and Dialectica calls on which ESG platform fits which use case. Buyers are those vendors and the sustainability leads who explain them to procurement. Berlin examples include Plan A, Cozero, Climatiq, Vaayu, and carbmee.",
    )
    bullet(
        doc,
        "Carbon accounting is the front door of that niche. ",
        "Lead with it. The roundtable, the search demand, and the IntegrityNext feature make it the topic a content lead already understands. The pieces you can repeat are workflow pieces: missing supplier data, CBAM upstream gaps, what the screen has to show, how a rollout goes. A practice that explains GHG Protocol chapters for a living is a weaker fit, because those clients will ask you to be the accountant. Emissions factors, audits, and legal conclusions stay with their specialists.",
    )
    bullet(
        doc,
        "Real-asset finance is a client. ",
        "Take the AstroFinance package. It pays, and it becomes a sample. Have the one conversation with Tesseract Academy, since Stylianos and Linas Stankevicius already know the litepaper. Then stop hunting that market. A company buys a litepaper once, the buyer pool is small, and the work follows crypto sentiment. If a second real-asset project would crowd out a supply-chain climate retainer, decline it. Counsel reviews anything on token structure, and the footer says the piece is a product explanation.",
    )
    bullet(
        doc,
        "English and French are the craft inside the niche. ",
        "Oracle scoping, RFP responses, onboarding playbooks, QBRs, a RACI rollout. Sell the document an account executive sends, or the playbook an implementation lead runs. French is its own delivery, at about 25% above the English fee, when an EU vendor asks. German is for coffees in Berlin.",
        space_after=2,
    )
    para(
        doc,
        "AI is the roundtable subject inside carbon accounting, and the tool you draft with. A general AI-writing offer stays closed.",
        size=10,
        space_before=1,
        space_after=2,
        align="justify",
    )

    heading(doc, "4.  Three formats, and what to charge in year one")
    para(
        doc,
        "Published specialists already charge about €85 an hour and about €3,000 for a researched 1,500-word sustainability essay; clean-energy white papers often start near $6,000. Your year-one prices sit under those, so the first yes is reachable, and well above mill rates, which cannot fund €5,200 months.",
        size=10,
        space_after=3,
        align="justify",
    )

    make_table(
        doc,
        ["Format", "What the client gets", "Year-1 fee", "Your time"],
        [
            [
                "Expert brief",
                "1,200–1,800 words: a regulatory explainer, a rollout story, or one SEO piece with a single search intent. Two revision rounds.",
                "€900–1,400",
                "1–1.5 days",
            ],
            [
                "Blueprint",
                "6–12 pages: solution brief, implementation or deal blueprint, or the product and strategy half of a litepaper. Client supplies experts, data, and legal review.",
                "€2,500–4,500",
                "4–7 days",
            ],
            [
                "Retainer",
                "Three-month minimum. Monthly interview, then one blueprint or two briefs, plus four LinkedIn posts from the same material.",
                "€2,400–3,000 / month",
                "About 4 days",
            ],
        ],
        [2.6, 8.6, 3.5, 2.6],
    )
    para(doc, "", size=4, space_after=2)
    rich(
        doc,
        [
            (
                "What the words mean. ",
                {"size": 10, "bold": True},
            ),
            (
                "A blueprint is one document, then the engagement ends: 6–12 pages on how a product solves a problem or how a rollout works. Your litepaper sections and deal blueprints are this format. It wins a first yes and leaves a sample. A retainer is the practice you are trying to build: the same client pays the same fee every month, for three months at a minimum, for an agreed set of pieces. You interview them once a month and write from that. Two retainers in the niche are the stable shape. Sell a retainer after one paid project with that client. The AstroFinance package is ramp income, and it does not get a standing claim on the calendar.",
                {"size": 10},
            ),
        ],
        space_before=2,
        space_after=2,
        align="justify",
    )
    rich(
        doc,
        [
            (
                "AstroFinance, priced on purpose. ",
                {"size": 10, "bold": True},
            ),
            (
                "Propose three explainers for €2,100 total (€700 each), half up front, topics you choose: how the asset hub works, what an aerospace asset needs before it can be offered, and the security-token versus utility-token brief you have already had to write for a live prospect. Friendly, and still a real invoice. The public rate card keeps the same brief at €900–1,400, so the favor stays a favor.",
                {"size": 10},
            ),
        ],
        space_after=2,
        align="justify",
    )
    para(
        doc,
        "Leave on the shelf for this year: blog posts under €800, social-only ghostwriting under €1,500 a month, and full sustainability reports (a real market at €7,000 and up, and only sane once a client arrives with the data). Two trade-press bylines in the year, pitched from the roundtable essay, are marketing. They are part of the pipeline, and they are not the business.",
        size=10,
        space_after=2,
        align="justify",
    )

    heading(doc, "5.  The year, step by step")
    make_table(
        doc,
        ["When", "Do this", "Finished when"],
        [
            [
                "Week 1\nby 11 Oct",
                "Steuerberater: Freiberufler, KSK application, Kleinunternehmer, invoice line. Rewrite LinkedIn and the Carrd to the same sentence (section 6). One-page offer. One-page contract: scope, two revisions, 50% to start, kill fee, confidentiality, right to show a redacted sample.",
                "Carrd, LinkedIn, an offer, and an invoice all match.",
            ],
            [
                "Weeks 2–4",
                "Three samples, live as links. (1) A 1,400-word essay drafted before you moderate: what AI can and cannot do inside carbon-accounting software, from the product side. (2) A public solution brief on where supplier-carbon or traceability rollouts break, using your method and public facts only. (3) A redacted AstroFinance product-and-strategy excerpt, after written permission. If permission lags, a clearly labeled sample blueprint stands in.",
                "Featured section on LinkedIn holds all three.",
            ],
            [
                "Roundtable week",
                "Moderate. Within 72 hours publish a short point-of-view recap, with quotes from others only where you have a yes. Send it to each speaker and to 15 climate founders, with one line on what you write and the fee range.",
                "The essay is public and 15 people have it.",
            ],
            [
                "Weeks 3–8",
                "Two warm asks, then the niche list. AstroFinance: the €2,100 package, topics and price in the same note. Tesseract: one note about subcontracted litepaper sections, then stop. The list of 40 is supply-chain climate and compliance firms only: content leads and founders. Eight personal notes a week. Each note names a page on their site and proposes one title.",
                "AstroFinance has said yes or no. Two niche intro calls are booked.",
            ],
            [
                "Month 3\nearly Jan 2027",
                "Checkpoint. One paid delivery, or a signed AstroFinance package. If neither has happened, change the sample or the price. Another lane will not fix an offer that is not landing.",
                "A written yes, or a revised offer.",
            ],
            [
                "Months 4–6\nJan–Mar",
                "Convert the first niche client into a three-month retainer. A second real-asset project waits if it would fill days you need for that pursuit. The paid piece, with permission, becomes sample four. Lift the brief floor to €1,100 once two paid clips exist. Decline work under €800.",
                "One supply-chain climate retainer is signed.",
            ],
            [
                "Months 7–12",
                "Hold two niche retainers. One public piece a quarter, on supplier carbon, traceability, or compliance rollout. In month 9, write the degree-time offer on a single page: one retainer, about four days a month, €2,200–2,500, calendar told to the client in advance. Therapy marketing is a separate name and a separate site. This practice stays on supply-chain climate software, and it is the one you reopen after the degree.",
                "The lighter offer is signed, or ready to sign, before classes start.",
            ],
        ],
        [2.7, 11.5, 3.1],
    )

    heading(doc, "6.  The Carrd, before the first email")
    rich(
        doc,
        [
            (
                "nicolaspicard.carrd.co is the right container. ",
                {"size": 10, "bold": True},
            ),
            (
                "It is one page, it already has a Calendly (calendly.com/nicolas-m-picard/30min), and it already says you work part-time, on flexible hours, from Berlin. Keep that line. The page is aimed at a different buyer. The headline is “Product Manager & Startup Builder | Climate & Web3,” and the menu is product-market fit, MVPs, startup operations, and applied AI. The About still pairs community work at an LGBT+ social enterprise with a current fractional Head of Product seat. This autumn the product role is advisory, and the live proof is Dialectica plus the roundtable. A content lead who clicks through meets a product consultant whose About still describes last year’s roles.",
                {"size": 10},
            ),
        ],
        space_after=2,
        align="justify",
    )
    para(
        doc,
        "Rewrite that same URL in week 1. A new site can wait.",
        size=10,
        bold=True,
        space_before=1,
        space_after=2,
    )
    bullet(
        doc,
        "First screen. ",
        "The one sentence, the three writing products with the fees in section 4, and Schedule a chat. Proof you can link today: the AstroFinance Loom and the asset-hub page already on the site, plus the Nespresso supply-chain note you already cite. FIBE and the roundtable join as soon as you can name them in one line. The litepaper excerpt joins when AstroFinance agrees.",
    )
    bullet(
        doc,
        "About, five lines. ",
        "Supply-chain climate software, French and English as the languages you write in, part-time from Berlin. AstroFinance can appear as proof. It does not lead the page. Set German and Spanish to the level on your CVs, and keep them off the list of delivery languages. If the community role is still active, one clause is enough, and it does not lead.",
    )
    bullet(
        doc,
        "An “Also” line, with its own fees. ",
        "Product consulting, dashboards, lead scoring, and clickable prototypes stay available, because you have shipped them. They sit below the writing menu. The custom GPT that drafts funding proposals comes off this page: beside a writing offer, it tells the buyer the writing can be a prompt.",
    )
    bullet(
        doc,
        "Two cleanups. ",
        "The therapy-access hackathon comes off this URL. It is a real build, and it belongs later, with the master’s, under its own name. The footer icon labeled Substack currently points at github.com. Point it at the roundtable essay once that essay has a home, or remove the icon until then.",
        space_after=1,
    )

    heading(doc, "7.  What to have in hand before you pitch")
    bullet(doc, "Samples on the Carrd. ", "The roundtable essay, the public solution brief, and the permitted AstroFinance excerpt, each as a link on the page. The Loom and the asset-hub demo stay next to them, so a buyer sees that you have shipped the thing you are explaining.")
    bullet(doc, "The offer sheet and the contract. ", "Three products, the ranges above, two revisions, half to start, and a portfolio clause. A lawyer-drafted novel is unnecessary; a clear one-pager your Steuerberater has seen is enough.")
    bullet(doc, "A source rule and a claims footer. ", "Every number comes from a public source or the client’s file. The footer on technical pieces: practitioner explanation; carbon-accounting, legal, and investment advice remain with the client’s specialists.")
    bullet(doc, "Written permission. ", "Nespresso, the coffee trader, IntegrityNext, Walmart, J&J, and AstroFinance details appear only when already public or cleared in writing. Role, method, and results you already state on LinkedIn are the safe set.")
    bullet(doc, "A swipe file. ", "Five pieces you wish you had written, one folder per lane. Match their structure. The sentences stay yours.", space_after=1)

    heading(doc, "8.  Where the commissions come from")
    bullet(doc, "1. People who already trust you. ", "AstroFinance, Tesseract, the roundtable speakers, FIBE contacts, Dialectica’s team, and former colleagues now at climate startups. This is the whole first quarter.")
    bullet(doc, "2. Direct notes, then a coffee. ", "Heads of content, product marketing, and founders. Berlin’s climate and supply-chain scene is dense enough that a 30-minute coffee is a normal next step. Lead with a title you would write for their site.")
    bullet(doc, "3. Expert networks, as bridge cash. ", "Stay active on Dialectica. Apply to GLG, AlphaSights, and Guidepoint. A few calls in a thin month cover rent pressure and hand you anonymized problems you can later turn into briefs. The calls support the writing practice. They do not replace the retainer.")
    bullet(doc, "4. Studios that already sell the format. ", "Tesseract is the model: they win the client, you write the specialist sections, you know your minimum before you accept their rate. Ask them who else they respect.")
    bullet(doc, "5. Talent lists, only after two public clips. ", "A niche roster, Contently if the door opens, and one Upwork profile that lists only the three products and a high minimum. General freelance boards pull the rate card down. Use them late, or leave them.", space_after=1)

    heading(doc, "9.  What is worth learning")
    bullet(doc, "Carbon vocabulary, two weeks of evenings. ", "GHG Protocol scopes, spend-based versus activity-based factors, and what CBAM and CSRD actually ask of supplier data. You have specified this product. The goal is a draft a sustainability lead can trust.")
    bullet(doc, "B2B search intent, one week. ", "How a content manager writes a brief, what a single keyword is for, how internal links work. Enough to deliver the AstroFinance pieces and to talk fees with a head of content.")
    bullet(doc, "The practice itself. ", "KSK application, what you can deduct, invoice wording, and the difference between Freiberufler and a trade. That afternoon with a Steuerberater returns more than another certificate.", space_after=2)
    para(
        doc,
        "Skip a further product-management certificate, a generic copywriting course, and anything about growing a web3 audience. The gap is packaging and a pipeline, and the samples close it.",
        size=10,
        space_after=2,
        align="justify",
    )

    heading(doc, "10.  Rules that keep the year intact")
    bullet(doc, "One sentence in public. ", "If another lane appears before a supply-chain climate retainer is signed, it waits.")
    bullet(doc, "Price floor €800, and €900 is the real brief. ", "Under that, the month becomes a volume job and the master’s year gets harder, not easier.")
    bullet(doc, "Your name stays clean. ", "No client numbers without permission. No technical piece without the footer. No litepaper that reads like an offer of securities.")
    bullet(doc, "Shrink on purpose. ", "Month 9 is when you design the four-day retainer and tell clients the calendar. That same offer is what you pick back up after the degree, while the therapy roster is still small. The two practices stay separate: different name, different site, different promise.", space_after=3)

    para(
        doc,
        "Planning note. Specialist rates cited from public pages as of early 2026: The EcoWriter (€85/hour; €3,000 for a 1,500–2,000 word sustainability article) and Renewable Writing (white papers from $6,000). German thresholds used here: Kleinunternehmer prior-year turnover under €25,000 and current-year under €100,000; KSK health-insurance contributions assessed from a 2026 minimum income of €7,910 a year, with the insured paying roughly half. The €5,200 figure is a planning estimate, not tax advice.",
        size=8,
        italic=True,
        color=MUTED,
        space_before=2,
        space_after=0,
    )

    add_footer(doc)
    out = "/workspace/Nicolas-Picard-Domain-Writing-Plan.docx"
    doc.save(out)
    print(out)


if __name__ == "__main__":
    build()
