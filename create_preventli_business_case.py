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

    filename = "Preventli_Business_Case_Comprehensive.pdf"
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
    story.append(Paragraph("Anonymous Signals → Early Action → Defensible Proof", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("A prevention-first workplace risk system for Australian SMBs", body_style))
    story.append(Spacer(1, 1*inch))

    # Key metrics box
    metrics_data = [
        ['Market Opportunity', 'Strategic Advantage'],
        ['Blue ocean in $2.3B compliance market', 'Signal-to-prevention vs compliance theatre'],
        ['30-500 employee SMBs underserved', 'GPNet risk engine integration ready'],
        ['Psychosocial hazard obligations', 'Defensible audit trails'],
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
        "Most businesses don't fail because people stayed silent. They fail because <b>nothing happened early enough</b>.",
        body_style
    ))
    story.append(Paragraph(
        "Preventli is a Workplace Risk Signal & Prevention System that transforms anonymous workplace concerns "
        "into structured prevention cases with defensible audit trails. Built on GPNet's proven risk engine, "
        "it positions businesses as prevention-first rather than compliance-reactive.",
        body_style
    ))
    story.append(Paragraph(
        "This represents a blue ocean opportunity within the saturated compliance market—moving from "
        "'How do we meet whistleblower law?' to 'How do we stop people getting hurt—and prove we tried?'",
        quote_style
    ))

    # Market Analysis
    story.append(Paragraph("Market Analysis", section_style))
    story.append(Paragraph("The Structural Gap", subsection_style))
    story.append(Paragraph(
        "The Australian workplace compliance market exhibits a three-layer structure with a critical gap:",
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
        "SMBs face increasing regulatory pressure from psychosocial hazard obligations, WorkCover exposure, "
        "and Fair Work escalation pathways—but lack affordable systems that prove they took reasonable steps "
        "to prevent harm. One incident can destroy a small business.",
        body_style
    ))

    # The Preventli Solution
    story.append(Paragraph("The Preventli Solution", section_style))
    story.append(Paragraph("Prevention-First Architecture", subsection_style))
    story.append(Paragraph(
        "Preventli transforms any workplace concern into a managed prevention case through six integrated stages:",
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
        ['Single System', 'Psychosocial hazards and physical injuries managed together', 'No data silos or duplication'],
        ['Prevention Loop', 'Early signal capture reduces downstream claims', 'Lower WorkCover and regulatory exposure'],
        ['Defensibility', 'Complete audit trail proves reasonable steps taken', 'Regulatory protection'],
        ['SMB Pricing', 'Big 4 outcomes at software pricing', 'Underserved market access'],
        ['Existing Architecture', 'GPNet risk engine integration ready', 'Minimal rebuild required'],
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
        "This approach inverts typical market positioning:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Competitors ask:</b> 'How do we meet whistleblower law?'<br/>"
        "• <b>Preventli asks:</b> 'How do we stop people getting hurt—and prove we tried?'",
        quote_style
    ))
    story.append(Paragraph(
        "Instead of bolting whistleblowing onto HR software, Preventli absorbs it into a prevention engine. "
        "This is rare—possibly unique—at SMB scale. The system closes the loop that every other vendor leaves open.",
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
        "This is a blue ocean inside a red ocean. The market for shallow reporting tools is saturated, "
        "but the market for signal-to-prevention systems is wide open. GPNet's existing architecture is "
        "structurally suited to capture this opportunity with minimal rebuild—it's a positioning and "
        "execution problem, not a demand problem.",
        body_style
    ))
    story.append(Paragraph(
        "Preventli gives businesses early warning, structured action, anti-retaliation protection, "
        "and defensible proof at an SMB-appropriate cost. It doesn't replace leadership—it protects leaders who act.",
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