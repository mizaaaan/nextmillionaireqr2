#!/usr/bin/env python3
"""Generate sample PDF documents for the member portal.

Usage:
    python3 scripts/generate-pdfs.py

This will regenerate all 4 PDFs in the docs/ folder:
  - docs/financial-report-2025.pdf
  - docs/meeting-minutes-q2-2026.pdf
  - docs/announcements.pdf
  - docs/member-guide.pdf

Requires: reportlab (pip install reportlab)
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
BRAND_BLUE = HexColor("#54C2FE")
BRAND_DARK = HexColor("#1a4f6e")
LIGHT_GRAY = HexColor("#f5f5f5")

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    "CoverTitle", fontSize=28, leading=34, fontName="Helvetica-Bold",
    textColor=BRAND_DARK, spaceAfter=12, alignment=TA_CENTER
))
styles.add(ParagraphStyle(
    "CoverSub", fontSize=14, leading=18, fontName="Helvetica",
    textColor=HexColor("#666666"), spaceAfter=6, alignment=TA_CENTER
))
styles.add(ParagraphStyle(
    "MyH1", fontSize=20, leading=26, fontName="Helvetica-Bold",
    textColor=BRAND_DARK, spaceAfter=14, spaceBefore=20
))
styles.add(ParagraphStyle(
    "MyH2", fontSize=14, leading=18, fontName="Helvetica-Bold",
    textColor=black, spaceAfter=8, spaceBefore=14
))
styles.add(ParagraphStyle(
    "MyBody", fontSize=11, leading=16, fontName="Helvetica",
    textColor=black, spaceAfter=8, alignment=TA_JUSTIFY
))
styles.add(ParagraphStyle(
    "MyMeta", fontSize=9, leading=12, fontName="Helvetica",
    textColor=HexColor("#999999"), spaceAfter=4, alignment=TA_CENTER
))


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BRAND_BLUE)
    canvas.rect(0, A4[1] - 8, A4[0], 8, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 7)
    canvas.drawString(20, A4[1] - 6.5, "Next Millionaire Co-operative")
    canvas.drawRightString(A4[0] - 20, A4[1] - 6.5, "CONFIDENTIAL - MEMBERS ONLY")
    canvas.setFillColor(HexColor("#bbbbbb"))
    canvas.setFont("Helvetica", 7)
    canvas.drawCentredString(A4[0] / 2, 12, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def add_divider():
    return HRFlowable(width="100%", thickness=0.5, color=HexColor("#dddddd"),
                       spaceBefore=10, spaceAfter=10)


# ── Financial Report ──
def generate_financial_report():
    path = os.path.join(OUT_DIR, "financial-report-2025.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4,
                            topMargin=20*mm, bottomMargin=18*mm,
                            leftMargin=22*mm, rightMargin=22*mm)
    story = []

    story.append(Spacer(1, 60))
    story.append(Paragraph("NEXT MILLIONAIRE", ParagraphStyle(
        "CoverBrand", fontSize=12, leading=14, fontName="Helvetica-Bold",
        textColor=BRAND_BLUE, spaceAfter=30, alignment=TA_CENTER)))
    story.append(Paragraph("Annual Financial Report 2025", styles["CoverTitle"]))
    story.append(Paragraph("For the Year Ended December 31, 2025", styles["CoverSub"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Registration No. CO-4471/2010", styles["MyMeta"]))
    story.append(Paragraph("Prepared: February 28, 2026", styles["MyMeta"]))
    story.append(Spacer(1, 50))
    story.append(HRFlowable(width="40%", thickness=2, color=BRAND_BLUE,
                              spaceBefore=0, spaceAfter=20))
    story.append(Paragraph(
        "This report contains confidential financial information for members only. "
        "Please do not distribute outside the co-operative.",
        ParagraphStyle("Disclaimer", fontSize=9, leading=13, fontName="Helvetica-Oblique",
                       textColor=HexColor("#888888"), alignment=TA_CENTER, spaceAfter=20)))
    story.append(PageBreak())

    story.append(Paragraph("1. Executive Summary", styles["MyH1"]))
    story.append(Paragraph(
        "The Next Millionaire Co-operative Society Limited completed its fifteenth year of "
        "operations in 2025 with strong financial performance across all business segments. "
        "Total revenue increased by 18.7% compared to the previous year, driven primarily by "
        "the expansion of our commercial fleet and increased member contributions.",
        styles["MyBody"]))
    story.append(Paragraph(
        "Net surplus for the year was BDT 4,280,000 (2024: BDT 3,620,000), representing a "
        "growth of 18.2%. The board recommends a dividend of 12% on member share capital, "
        "subject to approval at the Annual General Meeting.",
        styles["MyBody"]))
    story.append(add_divider())

    story.append(Paragraph("2. Revenue Breakdown", styles["MyH1"]))
    rev_data = [
        ["Segment", "2025 (BDT)", "2024 (BDT)", "Change"],
        ["Fleet Rental Income", "3,850,000", "3,120,000", "+23.4%"],
        ["Member Subscription Fees", "890,000", "840,000", "+6.0%"],
        ["Investment Income", "420,000", "380,000", "+10.5%"],
        ["Other Income", "180,000", "160,000", "+12.5%"],
        ["Total Revenue", "5,340,000", "4,500,000", "+18.7%"],
    ]
    t = Table(rev_data, colWidths=[200, 120, 120, 80])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("BACKGROUND", (0, -1), (-1, -1), HexColor("#e8f4fd")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [white, LIGHT_GRAY]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    story.append(Paragraph("3. Operating Expenses", styles["MyH1"]))
    exp_data = [
        ["Expense Category", "2025 (BDT)", "% of Revenue"],
        ["Vehicle Maintenance", "320,000", "6.0%"],
        ["Fuel & Lubricants", "280,000", "5.2%"],
        ["Salaries & Benefits", "180,000", "3.4%"],
        ["Office & Administration", "95,000", "1.8%"],
        ["Insurance", "75,000", "1.4%"],
        ["Depreciation", "110,000", "2.1%"],
        ["Total Expenses", "1,060,000", "19.9%"],
    ]
    t2 = Table(exp_data, colWidths=[200, 120, 120])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("BACKGROUND", (0, -1), (-1, -1), HexColor("#e8f4fd")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [white, LIGHT_GRAY]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t2)
    story.append(Spacer(1, 20))

    story.append(Paragraph("4. Balance Sheet Highlights (as at Dec 31, 2025)", styles["MyH1"]))
    bs_data = [
        ["Item", "Amount (BDT)"],
        ["Total Assets", "8,750,000"],
        ["Total Liabilities", "1,920,000"],
        ["Member Share Capital", "4,550,000"],
        ["Retained Earnings", "2,280,000"],
        ["Net Worth", "6,830,000"],
    ]
    t3 = Table(bs_data, colWidths=[250, 150])
    t3.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t3)
    story.append(Spacer(1, 16))

    story.append(Paragraph(
        "The financial position remains strong with a debt-to-equity ratio of 0.28 and "
        "current ratio of 2.4. The board is satisfied with the financial health of the "
        "co-operative and recommends continued investment in fleet expansion.",
        styles["MyBody"]))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"  Created: {os.path.basename(path)}")


# ── Meeting Minutes ──
def generate_meeting_minutes():
    path = os.path.join(OUT_DIR, "meeting-minutes-q2-2026.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4,
                            topMargin=20*mm, bottomMargin=18*mm,
                            leftMargin=22*mm, rightMargin=22*mm)
    story = []

    story.append(Spacer(1, 30))
    story.append(Paragraph("NEXT MILLIONAIRE CO-OPERATIVE", ParagraphStyle(
        "Brand", fontSize=11, leading=14, fontName="Helvetica-Bold",
        textColor=BRAND_BLUE, spaceAfter=4, alignment=TA_CENTER)))
    story.append(Paragraph("Minutes of the Quarterly General Meeting", styles["CoverTitle"]))
    story.append(Paragraph("Second Quarter 2026", styles["CoverSub"]))
    story.append(Spacer(1, 8))
    story.append(add_divider())
    story.append(Paragraph(
        "<b>Date:</b> July 12, 2026 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Time:</b> 10:00 AM "
        "&nbsp;&nbsp;|&nbsp;&nbsp; <b>Venue:</b> Co-operative Hall, Dhaka",
        styles["MyBody"]))
    story.append(Paragraph(
        "<b>Chairperson:</b> Md. Rafiqul Islam &nbsp;&nbsp;|&nbsp;&nbsp; "
        "<b>Secretary:</b> Fatima Begum",
        styles["MyBody"]))
    story.append(Paragraph(
        "<b>Members Present:</b> 47 out of 52 registered members (90.4% attendance)",
        styles["MyBody"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Agenda", styles["MyH1"]))
    for i, item in enumerate([
        "Call to order and welcome remarks",
        "Approval of minutes from the previous meeting (Q1 2026)",
        "Review of Q2 financial performance",
        "Fleet expansion update — 3 new vehicles acquired",
        "Proposed member dividend for 2025",
        "Election of audit committee for FY 2026-27",
        "Any other business",
        "Adjournment",
    ], 1):
        story.append(Paragraph(f"{i}. {item}", styles["MyBody"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Proceedings", styles["MyH1"]))

    proceedings = [
        ("1. Call to Order",
         "The Chairperson called the meeting to order at 10:15 AM. A welcome address was "
         "delivered thanking members for their continued support and participation."),
        ("2. Approval of Previous Minutes",
         "The minutes of the Q1 2026 meeting held on April 10, 2026 were read and approved "
         "unanimously. No corrections were proposed."),
        ("3. Financial Performance Review",
         "The Treasurer presented the Q2 financial summary. Total revenue for the quarter was "
         "BDT 1,420,000 (16% above budget). Fleet rental income remained the largest contributor "
         "at BDT 980,000. Operating expenses were within budget at BDT 265,000. The net surplus "
         "for Q2 was BDT 1,155,000."),
        ("4. Fleet Expansion Update",
         "The Fleet Manager reported that three new Toyota Axio vehicles were acquired in May "
         "2026 at a total cost of BDT 2,850,000. All three vehicles have already been leased to "
         "members under the driver program. The fleet now stands at 15 vehicles with plans to "
         "add 3 more by December 2026."),
        ("5. Member Dividend Proposal",
         "The board proposed a 12% dividend on member share capital for FY 2025, amounting to "
         "BDT 546,000. The proposal was discussed and will be put to vote at the Annual General "
         "Meeting in August 2026. Members expressed satisfaction with the proposed rate."),
        ("6. Audit Committee Election",
         "The following members were elected to the Audit Committee for FY 2026-27: "
         "1) Md. Kamal Hossain (Chair), 2) Sharmin Akhter, 3) Abdul Karim. "
         "The committee will serve a one-year term."),
        ("7. Any Other Business",
         "A member raised the possibility of introducing a health insurance scheme for members. "
         "The board agreed to form a sub-committee to study the feasibility and report back at "
         "the next meeting."),
        ("8. Adjournment",
         "The meeting was adjourned at 12:30 PM. The next quarterly meeting is scheduled for "
         "October 11, 2026."),
    ]
    for title, body in proceedings:
        story.append(Paragraph(title, styles["MyH2"]))
        story.append(Paragraph(body, styles["MyBody"]))

    story.append(Spacer(1, 30))
    story.append(add_divider())
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "_________________________<br/>Md. Rafiqul Islam<br/>Chairperson",
        ParagraphStyle("Sig1", fontSize=11, leading=16, fontName="Helvetica",
                       textColor=black, spaceAfter=20)))
    story.append(Paragraph(
        "_________________________<br/>Fatima Begum<br/>Secretary",
        ParagraphStyle("Sig2", fontSize=11, leading=16, fontName="Helvetica",
                       textColor=black)))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"  Created: {os.path.basename(path)}")


# ── Announcements ──
def generate_announcements():
    path = os.path.join(OUT_DIR, "announcements.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4,
                            topMargin=20*mm, bottomMargin=18*mm,
                            leftMargin=22*mm, rightMargin=22*mm)
    story = []

    story.append(Spacer(1, 20))
    story.append(Paragraph("NEXT MILLIONAIRE", ParagraphStyle(
        "Brand", fontSize=11, leading=14, fontName="Helvetica-Bold",
        textColor=BRAND_BLUE, spaceAfter=4, alignment=TA_CENTER)))
    story.append(Paragraph("Member Announcements", styles["CoverTitle"]))
    story.append(Paragraph("July 2026", styles["CoverSub"]))
    story.append(add_divider())

    announcements = [
        ("📌 AGM Notice", "July 28, 2026",
         "The 15th Annual General Meeting of Next Millionaire Co-operative Society Limited "
         "will be held on <b>Sunday, August 15, 2026 at 10:00 AM</b> at the Co-operative Hall, "
         "42/B Segunbagicha, Dhaka. All members are cordially invited. Agenda: approval of "
         "annual accounts, dividend declaration, and board election. "
         "Please confirm attendance by August 5."),
        ("🚗 Fleet Update: 3 New Cars Added", "July 15, 2026",
         "We are pleased to announce the addition of three new Toyota Axio vehicles to our "
         "commercial fleet. These vehicles are now available for lease under our driver program. "
         "Interested members may apply through the Fleet page or contact the office directly. "
         "Our fleet now totals 15 vehicles."),
        ("🎓 Member Training Program", "July 10, 2026",
         "A two-day training workshop on <b>\"Financial Literacy for Co-operative Members\"</b> "
         "will be conducted on August 5-6, 2026. Topics include savings planning, loan management, "
         "and understanding financial statements. Lunch and materials will be provided. "
         "Please register at the office by July 30. Limited to 30 participants."),
        ("📋 Audit Committee Election Results", "July 12, 2026",
         "The following members were elected to the Audit Committee for FY 2026-27 at the "
         "Q2 General Meeting: <b>Md. Kamal Hossain</b> (Chair), <b>Sharmin Akhter</b>, "
         "and <b>Abdul Karim</b>. We extend our gratitude to the outgoing committee for "
         "their dedicated service."),
        ("🏆 Member Spotlight: Success Story", "July 5, 2026",
         "Member <b>Md. Shahidul Islam</b> joined the driver program in January 2025 and has "
         "since generated a steady monthly income of BDT 45,000-55,000 through our fleet rental "
         "program. \"This program changed my life,\" says Shahidul. If you'd like to share your "
         "story, please contact the communications team."),
        ("📢 Office Holiday Notice", "June 28, 2026",
         "The co-operative office will remain closed on <b>July 7, 2026 (Eid-ul-Azha)</b>. "
         "Regular operations will resume on July 8. For urgent matters, please contact "
         "the duty officer at +880 1700-000000."),
    ]

    for title, date, body in announcements:
        story.append(Spacer(1, 8))
        story.append(Paragraph(title, styles["MyH2"]))
        story.append(Paragraph(f"<i>{date}</i>", ParagraphStyle(
            "Date", fontSize=9, leading=12, fontName="Helvetica-Oblique",
            textColor=HexColor("#999999"), spaceAfter=6)))
        story.append(Paragraph(body, styles["MyBody"]))
        story.append(add_divider())

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"  Created: {os.path.basename(path)}")


# ── Member Guide ──
def generate_member_guide():
    path = os.path.join(OUT_DIR, "member-guide.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4,
                            topMargin=20*mm, bottomMargin=18*mm,
                            leftMargin=22*mm, rightMargin=22*mm)
    story = []

    story.append(Spacer(1, 50))
    story.append(Paragraph("NEXT MILLIONAIRE", ParagraphStyle(
        "Brand", fontSize=12, leading=14, fontName="Helvetica-Bold",
        textColor=BRAND_BLUE, spaceAfter=20, alignment=TA_CENTER)))
    story.append(Paragraph("Member Guide<br/>and<br/>Co-operative By-Laws", styles["CoverTitle"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("2026 Edition", styles["CoverSub"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Registration No. CO-4471/2010", styles["MyMeta"]))
    story.append(Spacer(1, 40))
    story.append(add_divider())
    story.append(PageBreak())

    toc_items = [
        "1. About Next Millionaire Co-operative",
        "2. Membership Eligibility & Application",
        "3. Member Rights & Responsibilities",
        "4. Share Capital & Dividends",
        "5. Fleet Rental Program",
        "6. Loan & Credit Facilities",
        "7. Meetings & Voting",
        "8. Code of Conduct",
        "9. Grievance Redressal",
        "10. Contact Information",
    ]
    story.append(Paragraph("Table of Contents", styles["MyH1"]))
    for item in toc_items:
        story.append(Paragraph(item, styles["MyBody"]))
    story.append(PageBreak())

    sections = [
        ("1. About Next Millionaire Co-operative",
         "Next Millionaire Co-operative Society Limited was registered in 2010 under the "
         "Co-operative Societies Act, 2001 (Registration No. CO-4471/2010). We are a member-owned "
         "organization committed to building community wealth through shared ownership and "
         "collective enterprise. Our primary activities include commercial fleet management, "
         "member savings and credit services, and community development initiatives."),
        ("2. Membership Eligibility & Application",
         "Any individual aged 18 or above, residing in the co-operative's operational area, "
         "and subscribing to the principles of co-operation may apply for membership. "
         "Application process: (a) Submit a completed membership application form, (b) Provide "
         "two passport-sized photographs and valid ID proof, (c) Pay the membership fee of "
         "BDT 500 and purchase at least one share (BDT 1,000 per share), (d) Attend an "
         "orientation session. Admission is subject to board approval."),
        ("3. Member Rights & Responsibilities",
         "<b>Rights:</b> Vote in general meetings, stand for election, access co-operative "
         "services, share in surplus (dividend), inspect books of accounts (with notice).<br/><br/>"
         "<b>Responsibilities:</b> Adhere to by-laws, attend meetings regularly, "
         "use co-operative services responsibly, maintain confidentiality of member information, "
         "promote the co-operative spirit."),
        ("4. Share Capital & Dividends",
         "Each member must hold a minimum of one share (face value BDT 1,000). Members may "
         "purchase up to 20% of the total share capital. Dividends are declared annually based "
         "on surplus and are subject to board recommendation and AGM approval. The co-operative "
         "also maintains a reserve fund as per legal requirements."),
        ("5. Fleet Rental Program",
         "The fleet rental program allows members to lease commercial vehicles on a monthly basis "
         "to generate income. Key terms: (a) Monthly lease rate: BDT 25,000-35,000 depending on "
         "vehicle, (b) Security deposit: BDT 50,000 (refundable), (c) Minimum lease period: "
         "6 months, (d) Vehicle maintenance: co-operative covers major repairs, driver covers "
         "routine maintenance. Eligibility: must be a member in good standing for at least 3 months."),
        ("6. Loan & Credit Facilities",
         "Members may access the following credit facilities: (a) Emergency Loan: up to BDT 50,000 "
         "at 8% interest, (b) Vehicle Purchase Loan: up to 70% of vehicle value at 10% interest, "
         "(c) Education Loan: up to BDT 100,000 at 6% interest. All loans require a guarantor "
         "and are subject to the co-operative's credit assessment."),
        ("7. Meetings & Voting",
         "The co-operative holds quarterly general meetings and one Annual General Meeting each "
         "year. Each member has one vote regardless of shareholding. Voting may be conducted by "
         "show of hands or secret ballot. A quorum of 30% of members is required for any general "
         "meeting. Special general meetings may be called by the board or upon requisition by "
         "20% of members."),
        ("8. Code of Conduct",
         "Members are expected to: (a) Act in good faith and in the best interest of the "
         "co-operative, (b) Avoid conflicts of interest, (c) Treat fellow members with respect, "
         "(d) Use co-operative assets responsibly, (e) Maintain confidentiality, (f) Comply with "
         "all applicable laws and regulations. Violation may result in suspension or termination "
         "of membership after due process."),
        ("9. Grievance Redressal",
         "Any member with a grievance may: (a) Raise the issue with their respective committee, "
         "(b) Submit a written complaint to the board secretary, (c) Request mediation by the "
         "Grievance Redressal Committee. The committee will respond within 15 working days. "
         "If unsatisfied, the member may appeal to the board, whose decision shall be final."),
        ("10. Contact Information",
         "<b>Office Address:</b> 42/B Segunbagicha, Dhaka 1000, Bangladesh<br/>"
         "<b>Phone:</b> +880 1700-000000<br/>"
         "<b>Email:</b> info@nextmillionaire.com<br/>"
         "<b>Office Hours:</b> Sunday-Thursday, 9:00 AM - 5:00 PM<br/>"
         "<b>Website:</b> https://mizaaaan.github.io/nextmillionaireqr2/<br/><br/>"
         "<i>\"Building community wealth through shared ownership.\"</i>"),
    ]

    for i, (title, body) in enumerate(sections):
        story.append(Paragraph(title, styles["MyH1"]))
        story.append(Paragraph(body, styles["MyBody"]))
        story.append(Spacer(1, 8))
        if i < len(sections) - 1:
            story.append(add_divider())
        story.append(Spacer(1, 4))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"  Created: {os.path.basename(path)}")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    print("Generating portal PDFs...")
    generate_financial_report()
    generate_meeting_minutes()
    generate_announcements()
    generate_member_guide()
    print("Done! All PDFs saved in docs/")
