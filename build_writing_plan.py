#!/usr/bin/env python3
"""Build the domain-writing income plan for Nicolas Picard."""

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
    p = para(doc, text, size=12, bold=True, color=GREEN, space_before=4, space_after=1)
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


def bullet(doc, lead, rest, space_after=1):
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


def add_hyperlink(paragraph, text, url, size=10):
    r_id = paragraph.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), "Calibri")
    rFonts.set(qn("w:hAnsi"), "Calibri")
    rPr.append(rFonts)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size * 2)))
    rPr.append(sz)
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "2D6A4F")
    rPr.append(color)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rPr.append(underline)
    run.append(rPr)
    text_el = OxmlElement("w:t")
    text_el.set(qn("xml:space"), "preserve")
    text_el.text = text
    run.append(text_el)
    hyperlink.append(run)
    paragraph._p.append(hyperlink)


def link_bullet(doc, lead, parts, space_after=1):
    """parts is a list of strings or (label, url) tuples."""
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
    for part in parts:
        if isinstance(part, tuple):
            add_hyperlink(p, part[0], part[1])
        else:
            add_text(p, part, size=10, color=INK)
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
    section.top_margin = Cm(1.05)
    section.bottom_margin = Cm(1.05)
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

    heading(doc, "1.  Target revenue")
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
                "two paper retainers inside one niche. A white paper is a single sales asset, and that project ends. A paper retainer is the same client, the same monthly fee, funding one paper a quarter plus one case study or regulatory briefing each month. Ten to twelve writing days a month is the cap. AstroFinance and Dialectica can pay while the niche is forming. Judge the year on whether two supply-chain climate clients have hired you for a second paper. If the master’s starts before October 2027, move to the lighter workload before classes begin. Do not wait until month 9.",
                {"size": 10},
            ),
        ],
        space_after=2,
        align="justify",
    )

    heading(doc, "2.  What I bring to the table")
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
                "“I write practitioner white papers and case studies for supply-chain climate software teams.” Use that sentence on LinkedIn and on the site. Decline other topics until a supply-chain climate client has signed a retainer. The seven CV variants stay in the job-search folder. Clients hire the sentence, and they will check it on nicolaspicard.carrd.co.",
                {"size": 10},
            ),
        ],
        space_after=2,
        align="justify",
    )

    heading(doc, "3.  Domain concentration")
    bullet(
        doc,
        "The niche is supply-chain climate software. ",
        "Vendors that sell supplier compliance, traceability, and carbon data are the buyers. Your long proof is here: Nespresso traceability in DR Congo, OpenSC playbooks, IntegrityNext’s supplier tool and carbon feature, and Dialectica calls on which ESG platform fits which use case. The person who hires you is product marketing or the founder, not the implementation team. Berlin examples include Plan A, Cozero, Climatiq, Vaayu, and carbmee.",
    )
    bullet(
        doc,
        "Carbon accounting goes in the title. ",
        "The roundtable, the search demand, and the IntegrityNext feature make it the topic a marketing lead already understands. The paper explains missing supplier data, the upstream numbers CBAM asks for, and what the software has to show a buyer. Do not write chapters that teach the GHG Protocol. Clients who want that will ask you to be the accountant. Emission factors, audits, and legal conclusions stay with their specialists.",
    )
    bullet(
        doc,
        "Real-asset finance is a client. ",
        "Take the AstroFinance package. It pays, and a redacted excerpt can become a sample once they agree in writing. Skip Tesseract unless you specifically want that one conversation. Then stop hunting that market. A company buys a litepaper once, the buyer pool is small, and the work follows crypto sentiment. If a second real-asset project would crowd out a supply-chain climate retainer, decline it. Counsel reviews anything on token structure, and the footer says the piece is a product explanation.",
    )
    bullet(
        doc,
        "English and French are the craft inside the niche. ",
        "The paper an account executive can send. French is its own delivery, at about 25% above the English fee, when an EU vendor asks. German is for coffees in Berlin.",
        space_after=2,
    )
    para(
        doc,
        "Help-center articles, release notes, onboarding emails, and internal implementation docs are written by marketing, product, or customer success. Leave that work to them. The document they pay an outsider for is the white paper: long enough that a generalist marketer will not draft it, and specific enough that the founder will not sit down for it. Your litepaper sections are the proof. AI is the roundtable subject inside the paper, and the tool you draft with. A general AI-writing offer stays closed.",
        size=10,
        space_before=1,
        space_after=2,
        align="justify",
    )

    heading(doc, "Target client")
    para(
        doc,
        "Sell to the team that has to explain the product, and does not already employ someone whose full-time job is the paper, the case study, and the regulatory note.",
        size=10,
        space_after=2,
        align="justify",
    )
    bullet(
        doc,
        "What they sell. ",
        "Supplier compliance, traceability, or carbon-data software. The person who reads the piece works in English or French.",
    )
    bullet(
        doc,
        "Who is already on the marketing team. ",
        "A founder, a head of marketing, or one to three generalists. The best note goes to a content lead who is the only person doing the job. Skip the company when a full-time content person already publishes white papers, case studies, and regulatory notes in your languages and is keeping up. IntegrityNext is that case, and you used to work there.",
    )
    bullet(
        doc,
        "Headcount is a clue. ",
        "Many of the better buyers have fewer than about 80 people. Fifty is a useful first sort, and it is wrong often enough to ignore as a rule: Climatiq is about 40–50 and already has a content manager. Plan A is larger, and its head of content left in 2025. Under about 30 people, and anywhere the team is shrinking, a €3,500 paper is a hard sale.",
    )
    bullet(
        doc,
        "The public content is thin or old. ",
        "No case studies, no paper a salesperson can send, a blog that has gone quiet, or an English-only library when they also sell in France. Name that gap in the email. Do not write “you need a writer.”",
    )
    bullet(
        doc,
        "They still spend on marketing. ",
        "A recent round, an open marketing role, or a marketing lead with no writer under them. After an acquisition, the budget may sit with the parent. Apave owns Aktio, and SGS owns Sami.",
        space_after=2,
    )

    heading(doc, "4.  Product mix and potential rates")
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
                "White paper",
                "2,500–4,000 words, one argument, one or two interviews with their expert. A sales asset, not a help article. They supply the expert and the legal review. Two revision rounds.",
                "€3,500–6,000",
                "5–8 days",
            ],
            [
                "Case study",
                "800–1,200 words from one customer interview. Sales uses it for a year. Same buyer as the paper. A French version is a second delivery, about 25% above the English fee.",
                "€1,000–1,800",
                "1.5–2 days",
            ],
            [
                "Regulatory briefing",
                "One to two pages on what a CBAM, CSRD, or supplier-data change means for the product and the buyer. Written to be forwarded by sales. Their counsel owns the legal reading.",
                "€700–1,100",
                "About 1 day",
            ],
            [
                "Paper retainer",
                "Billed monthly. One white paper a quarter, plus one case study or one regulatory briefing a month. Six-month start is ideal; three months is the minimum.",
                "€2,200–2,800 / month",
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
                "The white paper is the offer you are known for. The case study and the regulatory briefing are parallel offers for the same product-marketing buyer, in English or French, in Berlin or elsewhere. They are the work you sell in the months between papers. A paper-only practice stays lumpy, because most companies want one or two papers a year. The retainer bundles the next paper with one of those short pieces each month. Sell it after the first paid piece with that client. The AstroFinance package is ramp income, and it does not get a standing claim on the calendar.",
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
                "Propose three short pieces for €2,100 total (€700 each), half up front, topics you choose: how the asset hub works, what an aerospace asset needs before it can be offered, and the security-token versus utility-token brief you have already had to write for a live prospect. That price is the floor of the public briefing rate, on purpose.",
                {"size": 10},
            ),
        ],
        space_after=2,
        align="justify",
    )
    para(
        doc,
        "Leave on the shelf for this year: SEO calendars, configuration and onboarding guides (customer success owns those), social-only ghostwriting under €1,500 a month, and full sustainability reports (a real market at €7,000 and up, and only sane once a client arrives with the data). Two trade-press bylines in the year, pitched from the roundtable essay, are marketing for the pipeline.",
        size=10,
        space_after=2,
        align="justify",
    )

    heading(doc, "5.  Timeline")
    make_table(
        doc,
        ["When", "Do this", "Finished when"],
        [
            [
                "Week 1\nby 11 Oct",
                "Steuerberater: Freiberufler, KSK application, Kleinunternehmer, and what the invoice must say. Rewrite LinkedIn and the Carrd to the same sentence (section 6). A one-page price sheet. A one-page contract: what you will deliver, two rounds of edits, half the fee before you start, a fee if they cancel, confidentiality, and permission to show a version with private details removed.",
                "Carrd, LinkedIn, an offer, and an invoice all match.",
            ],
            [
                "Weeks 2–4",
                "Three samples, live as links. (1) The regulatory-briefing sample: a 1,400-word essay, drafted before you moderate, on what AI can and cannot do inside carbon-accounting software. (2) A short public white paper, about six pages, on where supplier-carbon programs break, from public facts only. (3) A redacted AstroFinance excerpt, after written permission. The case-study sample is the first paid one, published only with the customer’s yes.",
                "Featured section on LinkedIn holds all three.",
            ],
            [
                "Roundtable week",
                "Moderate. Within 72 hours, publish a short article that states your own conclusion. Do not quote anyone without their consent. Email it to the speakers and to 15 founders, with one line on what you write and what you charge.",
                "The essay is public and 15 people have it.",
            ],
            [
                "Weeks 3–8",
                "Email AstroFinance the €2,100 package, with the topics and the price in the same note. Skip Tesseract unless you specifically want that one conversation. Then work the company list: supply-chain climate and compliance firms only. Eight personal emails a week. Each email names one page on their site and proposes one title.",
                "AstroFinance has said yes or no. Two niche intro calls are booked.",
            ],
            [
                "Month 3\nearly Jan 2027",
                "Checkpoint. One paid delivery, or a signed AstroFinance package. If neither has happened, change the sample or the price. Another lane will not fix an offer that is not landing.",
                "A written yes, or a revised offer.",
            ],
            [
                "Months 4–6\nJan–Mar",
                "Convert the first niche piece, paper or case study, into a paper retainer. A second real-asset project waits if it would fill days you need for that pursuit. The paid paper, with permission, becomes a sample. After two paid papers, the next one starts at €4,500. Decline case studies under €1,000, briefings under €700, and papers under €3,500.",
                "One supply-chain climate client is on a paper retainer.",
            ],
            [
                "Months 7–12",
                "Hold two niche retainers. One public piece a quarter, on supplier carbon, traceability, or compliance rollout. In month 9, write the degree-time offer on a single page: one retainer, about four days a month, €2,200–2,500, calendar told to the client in advance. Therapy marketing is a separate name and a separate site. This practice stays on supply-chain climate software, and it is the one you reopen after the degree.",
                "The lighter offer is signed, or ready to sign, before classes start.",
            ],
        ],
        [2.7, 11.5, 3.1],
    )

    heading(doc, "6.  Professional Website Update")
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
        "Edit the words on this same URL in week 1. You do not need a new website.",
        size=10,
        bold=True,
        space_before=1,
        space_after=2,
    )
    bullet(
        doc,
        "First screen. ",
        "The one sentence, then the white paper, the case study, and the regulatory briefing, with the fees in section 4, and Schedule a chat. Proof you can link today: the AstroFinance Loom and the asset-hub page already on the site, plus the Nespresso supply-chain note you already cite. FIBE and the roundtable join as soon as you can name them in one line. The litepaper excerpt joins when AstroFinance agrees.",
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
    bullet(doc, "Samples on the Carrd. ", "The regulatory briefing, the short white paper, and the permitted AstroFinance excerpt, each as a link. The first paid case study joins when the customer agrees. The Loom and the asset-hub demo stay next to them.")
    bullet(doc, "The offer sheet and the contract. ", "The white paper, the case study, the regulatory briefing, and the retainer, with the ranges above. Two revisions, half to start, and a portfolio clause. A clear one-pager your Steuerberater has seen is enough.")
    bullet(doc, "A source rule and a claims footer. ", "Do not invent statistics. Every number comes from a public source or from the client’s own file. On any technical piece, add one line: this is an explanation of the product, not emissions advice, legal advice, or investment advice.")
    bullet(doc, "Written permission. ", "Do not publish a client’s private figures without written consent. Nespresso, the coffee trader, IntegrityNext, Walmart, J&J, and AstroFinance details appear only when already public or cleared in writing. Role, method, and results you already state on LinkedIn are the safe set.")
    bullet(doc, "A folder of models. ", "Keep five pieces you admire in one folder. Copy how they are built. Do not copy their sentences.", space_after=1)

    heading(doc, "8.  Business development")
    bullet(doc, "1. People who already trust you. ", "AstroFinance, the roundtable speakers, FIBE contacts, Dialectica’s team, and former colleagues now at climate startups. This is the whole first quarter. Skip Tesseract unless you specifically want that one conversation.")
    bullet(doc, "2. Direct notes, in English and French. ", "Start with the high-probability companies on the list: a thin marketing team, or no content person, and a page you can name. Then write the content lead at a staffed firm only when you can name one gap, such as a French version or a missing case study. A 30-minute call is the next step.")
    bullet(doc, "3. Expert networks, as bridge cash. ", "Stay active on Dialectica. Apply to GLG, AlphaSights, and Guidepoint. A few calls in a thin month cover rent pressure and hand you anonymized problems you can later turn into briefs. The calls support the writing practice. They do not replace the retainer.")
    bullet(doc, "4. Consultancies and the new owners. ", "EcoAct, South Pole, and the groups that acquired these tools already pay outside writers for supplier-carbon and CBAM work. Skip crypto agencies.")
    bullet(doc, "5. Talent lists, only after two public pieces. ", "Open Malt, Contently, or one Upwork profile only after the roundtable essay and the short public paper exist. List only the three services, and list the minimum prices.", space_after=1)

    heading(doc, "9.  Learning Plan")
    bullet(doc, "Carbon vocabulary, two weeks of evenings. ", "GHG Protocol scopes, spend-based versus activity-based factors, and what CBAM and CSRD actually ask of supplier data. You have specified this product. The goal is a draft a sustainability lead can trust. The pages are under What to read.")
    bullet(doc, "B2B search intent, one week. ", "How a content manager writes a brief. A keyword is the phrase someone types into Google. An internal link is a link from one page on their site to another page on the same site. Enough to deliver the AstroFinance pieces and to talk fees with a head of content.")
    bullet(doc, "The practice itself. ", "The KSK application, what you can deduct, invoice wording, and the difference between a Freiberufler and a trade. That afternoon with a Steuerberater returns more than another certificate.", space_after=2)
    para(
        doc,
        "Skip a further product-management certificate, a generic copywriting course, and anything about growing a web3 audience. The gap is packaging and a pipeline, and the samples close it.",
        size=10,
        space_after=2,
        align="justify",
    )

    heading(doc, "What to read")
    link_bullet(
        doc,
        "Carbon and supplier data. ",
        [
            ("GHG Protocol Corporate Standard", "https://ghgprotocol.org/corporate-standard"),
            ", ",
            ("Scope 2 Guidance", "https://ghgprotocol.org/scope-2-guidance"),
            ", ",
            ("Scope 3 Standard", "https://ghgprotocol.org/standards/scope-3-standard"),
            ", ",
            ("Scope 3 Calculation Guidance", "https://ghgprotocol.org/scope-3-calculation-guidance-2"),
            ", and the French emission-factor library ",
            ("ADEME Base Empreinte", "https://base-empreinte.ademe.fr/"),
            ".",
        ],
    )
    link_bullet(
        doc,
        "The rules buyers ask about. ",
        [
            ("CBAM, English", "https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en"),
            " and ",
            ("French", "https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_fr"),
            ", the ",
            ("CSRD page", "https://finance.ec.europa.eu/capital-markets-union-and-financial-markets/company-reporting-and-auditing/company-reporting/corporate-sustainability-reporting_en"),
            ", and the ",
            ("ESRS standards", "https://www.efrag.org/en/sustainability-reporting"),
            ".",
        ],
    )
    link_bullet(
        doc,
        "Search, one week. ",
        [
            ("Google’s SEO Starter Guide", "https://developers.google.com/search/docs/fundamentals/seo-starter-guide"),
            ", ",
            ("how links work", "https://developers.google.com/search/docs/crawling-indexing/links-crawlable"),
            ", and ",
            ("Ahrefs on keyword research", "https://ahrefs.com/blog/keyword-research/"),
            ".",
        ],
    )
    link_bullet(
        doc,
        "The German practice. ",
        [
            ("Künstlersozialkasse, for writers", "https://www.kuenstlersozialkasse.de/kuenstler-und-publizisten"),
            ", ",
            ("Kleinunternehmerregelung, §19 UStG", "https://www.gesetze-im-internet.de/ustg_1980/__19.html"),
            ", and ",
            ("Freiberufler, §18 EStG", "https://www.gesetze-im-internet.de/estg/__18.html"),
            ".",
        ],
        space_after=3,
    )

    para(
        doc,
        "Planning note, not tax advice. Public rates used above, early 2026: The EcoWriter (€85/hour; €3,000 for a sustainability article) and Renewable Writing (white papers from $6,000). Kleinunternehmer: prior year under €25,000 and this year under €100,000. KSK’s 2026 health minimum is €7,910, and the insured pays about half.",
        size=8,
        italic=True,
        color=MUTED,
        space_before=1,
        space_after=0,
    )

    add_footer(doc)
    out = "/workspace/Nicolas-Picard-Domain-Writing-Plan.docx"
    doc.save(out)
    print(out)


if __name__ == "__main__":
    build()
