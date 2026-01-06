#!/usr/bin/env python3
"""
Create a polished Preventli business case PDF in The Economist style
Combines strategic analysis with marketing positioning
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
import os
from datetime import datetime

class EconomistCanvas(canvas.Canvas):
    """Custom canvas with The Economist styling"""

    def draw_page_number(self, page_num, total_pages):
        """Add page numbers in Economist style"""
        if page_num > 1:  # Skip page number on cover
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor('#666666'))
            self.drawRightString(A4[0] - 0.75*inch, 0.5*inch, f"{page_num}")

    def draw_header(self, page_num):
        """Add subtle header line"""
        if page_num > 1:
            self.setStrokeColor(colors.HexColor('#DC143C'))  # Economist red
            self.setLineWidth(1)
            self.line(0.75*inch, A4[1] - 0.75*inch, A4[0] - 0.75*inch, A4[1] - 0.75*inch)

def create_preventli_business_case():
    """Create comprehensive Preventli business case PDF"""

    filename = "Preventli_Business_Case_Updated.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=1*inch,
        canvasmaker=EconomistCanvas
    )

    # The Economist color palette
    economist_red = colors.HexColor('#DC143C')
    economist_blue = colors.HexColor('#1E3A8A')
    dark_gray = colors.HexColor('#333333')
    medium_gray = colors.HexColor('#666666')
    light_gray = colors.HexColor('#F5F5F5')

    # Create custom styles inspired by The Economist
    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        'EconomistTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=32,
        spaceAfter=0.3*inch,
        textColor=dark_gray,
        alignment=TA_LEFT
    )

    # Subtitle style
    subtitle_style = ParagraphStyle(
        'EconomistSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        spaceAfter=0.4*inch,
        textColor=economist_red,
        alignment=TA_LEFT
    )

    # Section heading
    section_style = ParagraphStyle(
        'EconomistSection',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        spaceAfter=0.2*inch,
        spaceBefore=0.3*inch,
        textColor=economist_blue,
        alignment=TA_LEFT
    )

    # Subsection heading
    subsection_style = ParagraphStyle(
        'EconomistSubsection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceAfter=0.15*inch,
        spaceBefore=0.2*inch,
        textColor=dark_gray,
        alignment=TA_LEFT
    )

    # Body text
    body_style = ParagraphStyle(
        'EconomistBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        spaceAfter=0.15*inch,
        leading=14,
        textColor=dark_gray,
        alignment=TA_JUSTIFY
    )

    # Quote style
    quote_style = ParagraphStyle(
        'EconomistQuote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        spaceAfter=0.2*inch,
        spaceBefore=0.2*inch,
        leftIndent=0.5*inch,
        rightIndent=0.5*inch,
        textColor=economist_blue,
        alignment=TA_LEFT
    )

    # Caption style
    caption_style = ParagraphStyle(
        'EconomistCaption',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        spaceAfter=0.1*inch,
        textColor=medium_gray,
        alignment=TA_CENTER
    )

    # Build document content
    story = []

    # Cover page
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("Preventli", title_style))
    story.append(Paragraph("GPNet + Whistleblower Compliance = Complete Risk Platform", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Extending GPNet's proven workplace risk platform to meet new legislative requirements", body_style))
    story.append(Spacer(1, 1*inch))

    # Key metrics box
    metrics_data = [
        ['GPNet Foundation', 'Legislative Opportunity'],
        ['Proven platform with existing customers', 'New whistleblower protection laws'],
        ['Established workplace risk workflows', 'SMB compliance gap in market'],
        ['Trusted by Australian SMBs', 'Immediate upgrade revenue potential'],
    ]

    metrics_table = Table(metrics_data, colWidths=[3*inch, 3*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), light_gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), dark_gray),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray]),
    ]))

    story.append(metrics_table)
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"Prepared: {datetime.now().strftime('%B %Y')}", caption_style))
    story.append(PageBreak())

    # Executive Summary
    story.append(Paragraph("Executive Summary", section_style))
    story.append(Paragraph(
        "<b>GPNet is an established workplace injury and claims management platform</b> serving Australian SMBs. "
        "New legislative requirements for whistleblower protection create an immediate opportunity to extend "
        "GPNet's proven risk engine with anonymous reporting functionality.",
        body_style
    ))
    story.append(Paragraph(
        "Preventli represents this natural evolution—transforming GPNet from reactive claims processing "
        "to a complete 'signal-to-prevention' platform. The technical integration is straightforward: "
        "anonymous workplace concerns become new case types processed through GPNet's existing workflows.",
        body_style
    ))
    story.append(Paragraph(
        "This upgrade path serves existing customers first, provides clear compliance value, and positions "
        "GPNet uniquely in a market where competitors treat whistleblower reporting as an afterthought.",
        quote_style
    ))

    # Market Analysis
    story.append(Paragraph("Market Analysis", section_style))
    story.append(Paragraph("Legislative Driver & Market Opportunity", subsection_style))
    story.append(Paragraph(
        "New Australian whistleblower protection laws require businesses to provide safe reporting mechanisms. "
        "While large enterprises have compliance resources, <b>SMBs face a capability gap</b> that GPNet is uniquely positioned to fill.",
        body_style
    ))
    story.append(Paragraph(
        "The current market exhibits a problematic structure:",
        body_style
    ))

    market_data = [
        ['Layer', 'Characteristics', 'SMB Accessibility'],
        ['Saturated Layer', 'Anonymous hotlines, basic ethics portals', 'Commoditised, low value'],
        ['Empty Layer', 'Signal-to-prevention with audit trails', 'OPPORTUNITY'],
        ['Expensive Layer', 'Big 4 advisory services', 'Inaccessible to SMBs'],
    ]

    market_table = Table(market_data, colWidths=[1.5*inch, 2.5*inch, 2*inch])
    market_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), economist_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#FFF3CD')),  # Highlight opportunity
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    story.append(market_table)
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph(
        "<b>GPNet's existing customers already trust the platform</b> for workplace injury management. "
        "Adding whistleblower functionality leverages this established relationship and proven infrastructure, "
        "creating immediate upgrade revenue while ensuring SMBs can meet new compliance obligations.",
        body_style
    ))

    # The Preventli Solution
    story.append(Paragraph("The Preventli Solution", section_style))
    story.append(Paragraph("Extending GPNet's Proven Architecture", subsection_style))
    story.append(Paragraph(
        "GPNet already processes workplace injuries as structured cases with evidence, timelines, and audit trails. "
        "<b>Preventli simply adds anonymous intake</b> as a new case type, leveraging the existing risk engine:",
        body_style
    ))

    solution_data = [
        ['Stage', 'Process', 'Outcome'],
        ['1. Intake', 'Anonymous portal/app submission', 'Structured signal capture'],
        ['2. Classification', 'AI-assisted categorisation', 'Risk-rated case creation'],
        ['3. Triage', 'Severity assessment & action planning', 'Guided prevention workflow'],
        ['4. Action', 'Task assignment with timelines', 'Accountable execution'],
        ['5. Evidence', 'Timestamped action logging', 'Defensible audit trail'],
        ['6. Integration', 'Case history preservation', 'Full context if escalated'],
    ]

    solution_table = Table(solution_data, colWidths=[1*inch, 2.5*inch, 2.5*inch])
    solution_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), economist_red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray]),
    ]))

    story.append(solution_table)
    story.append(PageBreak())

    # Strategic Advantages
    story.append(Paragraph("Strategic Advantages", section_style))

    advantages_data = [
        ['Advantage', 'Description', 'Competitive Impact'],
        ['Proven Platform', 'GPNet already operational with existing customers', 'Lower risk, faster deployment'],
        ['Legislative Compliance', 'Meets new whistleblower protection requirements', 'Regulatory necessity drives sales'],
        ['Existing Customer Base', 'Upgrade existing GPNet customers first', 'Higher conversion, predictable revenue'],
        ['Minimal Development', 'Anonymous intake added to existing workflows', 'Fast time-to-market, low cost'],
        ['Single System', 'Whistleblower and injury cases managed together', 'No data silos, unified platform'],
    ]

    advantages_table = Table(advantages_data, colWidths=[1.5*inch, 2.5*inch, 2*inch])
    advantages_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), economist_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray]),
    ]))

    story.append(advantages_table)

    # Competitive Positioning
    story.append(Paragraph("Competitive Positioning", section_style))
    story.append(Paragraph(
        "While competitors scramble to build whistleblower solutions from scratch, <b>GPNet already has the foundation</b>:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Competitors:</b> Building new systems to meet compliance<br/>"
        "• <b>GPNet:</b> Adding anonymous intake to proven risk platform",
        quote_style
    ))
    story.append(Paragraph(
        "This creates a fundamental advantage: existing customers trust GPNet, the platform is operational, "
        "and anonymous reporting becomes a natural workflow extension rather than a bolt-on compliance tool.",
        body_style
    ))

    # What Preventli Delivers
    story.append(Paragraph("What Preventli Delivers", section_style))
    story.append(Paragraph("Core Functionality", subsection_style))

    features = [
        "Anonymous & confidential reporting via mobile-friendly portal",
        "AI-assisted triage and risk assessment (advisory only)",
        "Prevention case engine with structured workflows",
        "Anti-retaliation monitoring and protection",
        "Owner & board defensibility dashboard",
        "Complete audit trail generation"
    ]

    for feature in features:
        story.append(Paragraph(f"• {feature}", body_style))

    story.append(Paragraph("What Preventli is NOT", subsection_style))
    story.append(Paragraph(
        "Preventli is not a call centre, legal advice, HR chatbot, policy generator, or Big-4 consulting engagement. "
        "Preventli is <b>infrastructure</b>—the system that ensures action happens and is provable.",
        body_style
    ))

    # Target Market
    story.append(Paragraph("Target Market & Pricing", section_style))
    story.append(Paragraph("Ideal Customer Profile", subsection_style))
    story.append(Paragraph(
        "Primary targets: 30-500 employee businesses including franchises, multi-site operators, "
        "labour hire, transport, NDIS/aged care, clinics, hospitality groups, construction and trades.",
        body_style
    ))

    pricing_data = [
        ['Tier', 'Employee Range', 'Monthly Price (AUD)', 'Target Vertical'],
        ['Starter', '≤50 staff', 'From $299', 'Single-site SMBs'],
        ['Growth', '50-250 staff', 'From $699', 'Multi-department businesses'],
        ['Multi-site', '250+ staff', 'From $1,500', 'Franchises, enterprise'],
    ]

    pricing_table = Table(pricing_data, colWidths=[1.2*inch, 1.3*inch, 1.5*inch, 2*inch])
    pricing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), economist_red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray]),
    ]))

    story.append(pricing_table)
    story.append(PageBreak())

    # Go-to-Market Strategy
    story.append(Paragraph("Go-to-Market Strategy", section_style))
    story.append(Paragraph("Positioning Guidelines", subsection_style))

    positioning_points = [
        "Do NOT position as 'whistleblower software'—that's the saturated commodity layer",
        "Lead with psychosocial risk compliance and owner defensibility",
        "Target high-exposure SMB verticals: construction, healthcare, aged care, hospitality",
        "Message: 'Workplace risk prevention with proof'—not 'anonymous reporting'"
    ]

    for point in positioning_points:
        story.append(Paragraph(f"• {point}", body_style))

    # Implementation Roadmap
    story.append(Paragraph("Implementation Roadmap", section_style))

    roadmap_data = [
        ['Phase', 'Timeline', 'Key Deliverables', 'Success Metrics'],
        ['MVP Development', 'Q1 2026', 'Core reporting & case management', 'Pilot customer deployment'],
        ['AI Integration', 'Q2 2026', 'Intelligent triage & risk scoring', '10 paying customers'],
        ['Dashboard & Analytics', 'Q3 2026', 'Leadership visibility tools', '$50K MRR'],
        ['Scale & Expansion', 'Q4 2026', 'Multi-tenant, API integration', '100+ customers'],
    ]

    roadmap_table = Table(roadmap_data, colWidths=[1.2*inch, 1*inch, 2.3*inch, 1.5*inch])
    roadmap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), economist_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray]),
    ]))

    story.append(roadmap_table)

    # Risk Analysis
    story.append(Paragraph("Risk Analysis", section_style))
    story.append(Paragraph("The Cost of Doing Nothing", subsection_style))
    story.append(Paragraph(
        "If businesses continue to rely on emails, verbal conversations, informal notes, and memory, "
        "they are betting the business that no one escalates, screenshots, records, or connects patterns later. "
        "<b>That's not a strategy. That's hope.</b>",
        quote_style
    ))

    # Bottom Line
    story.append(Paragraph("Bottom Line", section_style))
    story.append(Paragraph(
        "<b>GPNet is already operational with paying customers</b> who trust the platform for workplace risk management. "
        "New legislative requirements create immediate demand for whistleblower functionality that can be added "
        "with minimal development effort.",
        body_style
    ))
    story.append(Paragraph(
        "This is not a startup risk—it's a proven platform extension. Existing customers provide immediate "
        "upgrade revenue, legislative compliance drives market urgency, and the technical integration leverages "
        "GPNet's established architecture. This represents execution opportunity, not demand validation.",
        body_style
    ))

    # Build PDF
    doc.build(story)
    print(f"Created comprehensive business case: {filename}")
    print(f"Document combines strategic analysis with marketing positioning")
    print(f"Styled in The Economist format with professional typography")
    print(f"Includes market analysis, competitive positioning, and implementation roadmap")

    return filename

if __name__ == "__main__":
    create_preventli_business_case()