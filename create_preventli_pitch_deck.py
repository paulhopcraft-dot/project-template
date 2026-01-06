#!/usr/bin/env python3
"""
Create a stylish Preventli pitch deck PDF in modern presentation format
Clean, professional design suitable for investor meetings and strategic discussions
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Frame, PageTemplate, BaseDocTemplate
)
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from datetime import datetime

class ModernPitchCanvas(canvas.Canvas):
    """Modern pitch deck canvas with clean styling"""

    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        self.page_num = 0

    def draw_slide_number(self):
        """Add subtle slide numbers"""
        if self.page_num > 1:  # Skip number on title slide
            self.setFont("Helvetica", 10)
            self.setFillColor(colors.HexColor('#999999'))
            self.drawRightString(A4[0] - 0.5*inch, 0.3*inch, f"{self.page_num}")

    def draw_footer_line(self):
        """Add subtle footer accent"""
        self.setStrokeColor(colors.HexColor('#E8E8E8'))
        self.setLineWidth(1)
        self.line(0.5*inch, 0.5*inch, A4[0] - 0.5*inch, 0.5*inch)

    def showPage(self):
        self.page_num += 1
        self.draw_slide_number()
        self.draw_footer_line()
        super().showPage()

def create_preventli_pitch_deck():
    """Create stylish Preventli pitch deck PDF"""

    filename = "Preventli_Pitch_Deck.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=0.8*inch,
        leftMargin=0.8*inch,
        topMargin=1*inch,
        bottomMargin=1*inch,
        canvasmaker=ModernPitchCanvas
    )

    # Modern color palette
    primary_blue = colors.HexColor('#1E40AF')    # Strong blue
    accent_orange = colors.HexColor('#F59E0B')   # Vibrant orange
    dark_text = colors.HexColor('#111827')       # Near black
    medium_gray = colors.HexColor('#6B7280')     # Medium gray
    light_gray = colors.HexColor('#F3F4F6')     # Light background
    success_green = colors.HexColor('#10B981')   # Success accent
    warning_red = colors.HexColor('#EF4444')     # Warning accent

    # Create modern styles
    styles = getSampleStyleSheet()

    # Title slide style
    title_style = ParagraphStyle(
        'ModernTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=42,
        spaceAfter=0.2*inch,
        textColor=primary_blue,
        alignment=TA_LEFT
    )

    # Subtitle style
    subtitle_style = ParagraphStyle(
        'ModernSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=18,
        spaceAfter=0.3*inch,
        textColor=dark_text,
        alignment=TA_LEFT
    )

    # Slide title
    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=28,
        spaceAfter=0.4*inch,
        spaceBefore=0.2*inch,
        textColor=primary_blue,
        alignment=TA_LEFT
    )

    # Section heading
    section_style = ParagraphStyle(
        'SectionHead',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        spaceAfter=0.2*inch,
        spaceBefore=0.3*inch,
        textColor=dark_text,
        alignment=TA_LEFT
    )

    # Body text - larger for presentations
    body_style = ParagraphStyle(
        'ModernBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        spaceAfter=0.15*inch,
        leading=18,
        textColor=dark_text,
        alignment=TA_LEFT
    )

    # Large body for key points
    large_body_style = ParagraphStyle(
        'LargeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        spaceAfter=0.2*inch,
        leading=20,
        textColor=dark_text,
        alignment=TA_LEFT
    )

    # Bullet point style
    bullet_style = ParagraphStyle(
        'ModernBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        spaceAfter=0.1*inch,
        leading=18,
        textColor=dark_text,
        leftIndent=0.3*inch,
        bulletIndent=0.1*inch,
        alignment=TA_LEFT
    )

    # Quote/highlight style
    highlight_style = ParagraphStyle(
        'ModernHighlight',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        spaceAfter=0.3*inch,
        spaceBefore=0.3*inch,
        textColor=accent_orange,
        alignment=TA_CENTER
    )

    # Build presentation content
    story = []

    # === SLIDE 1: TITLE ===
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("Preventli", title_style))
    story.append(Paragraph("The Workplace Risk & Early Intervention Platform", subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Signals → Prevention → Recovery → Proof", large_body_style))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("<i>Preventli isn't 'whistleblower software'. It's the system that prevents issues becoming claims—and proves what you did.</i>",
                 ParagraphStyle('Italic', parent=body_style, fontName='Helvetica-Oblique', textColor=medium_gray)))
    story.append(PageBreak())

    # === SLIDE 2: WHY NOW ===
    story.append(Paragraph('The "Why Now" Shift', slide_title_style))
    story.append(Paragraph("The standard has changed: <b>'What did you do when you knew?'</b>", highlight_style))
    story.append(Paragraph("Businesses are increasingly judged on:", section_style))

    why_now_points = [
        "Early psychosocial hazard signals",
        "Bullying/harassment concerns",
        "Early discomfort / reduced capacity",
        "How consistently action was taken and recorded"
    ]

    for point in why_now_points:
        story.append(Paragraph(f"• {point}", bullet_style))

    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("<i>Timeline: Early signal → Incident → Claim → Dispute</i>",
                 ParagraphStyle('Caption', parent=body_style, fontSize=12, textColor=medium_gray, alignment=TA_CENTER)))
    story.append(PageBreak())

    # === SLIDE 3: THE REAL PROBLEM ===
    story.append(Paragraph("The Real Problem: Fragmentation", slide_title_style))
    story.append(Paragraph("Most employers run people-risk through <b>4 broken channels</b>:", large_body_style))

    channels_data = [
        ['Channel', 'Problem'],
        ['HR inboxes + manager notes', 'Invisible, inconsistent'],
        ['Hotline/reporting portals', 'Intake only'],
        ['WHS hazard registers', 'Static'],
        ['Injury/claims systems', 'Reactive']
    ]

    channels_table = Table(channels_data, colWidths=[3*inch, 2.5*inch])
    channels_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray]),
    ]))

    story.append(channels_table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Result:</b> Signals don't connect → Patterns are missed → Response is late → Proof is weak", highlight_style))
    story.append(PageBreak())

    # === SLIDE 4: MARKET OPPORTUNITY ===
    story.append(Paragraph("The Opportunity (Market Structure)", slide_title_style))
    story.append(Paragraph("The market is mis-shaped:", large_body_style))

    market_structure_data = [
        ['Layer', 'Description', 'SMB Access'],
        ['Saturated', 'Anonymous portals + hotlines', 'Commodity, intake-only'],
        ['MISSING', 'Signal → prevention → recovery with proof', 'OPPORTUNITY'],
        ['Expensive', 'Advisory services', 'Human-heavy, unaffordable']
    ]

    market_table = Table(market_structure_data, colWidths=[1.5*inch, 2.5*inch, 2*inch])
    market_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 2), (-1, 2), accent_orange),  # Highlight opportunity row
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    story.append(market_table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Preventli lives in the missing middle.</b>", highlight_style))
    story.append(PageBreak())

    # === SLIDE 5: CORE THESIS ===
    story.append(Paragraph("Preventli's Core Thesis", slide_title_style))
    story.append(Paragraph("<b>Everything is an early workplace risk signal.</b>", highlight_style))
    story.append(Paragraph("Different entry points, same underlying need:", large_body_style))

    signal_types = [
        "<b>Speak-up/whistleblower</b> = anonymous signals",
        "<b>Psychosocial hazards</b> = stressors + patterns",
        "<b>Injury management</b> = physical outcomes + recovery",
        "<b>Age-related complexity</b> = gradual capacity drift + sensitivity + risk"
    ]

    for signal in signal_types:
        story.append(Paragraph(f"• {signal}", bullet_style))

    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph("<b>Preventli's job:</b> Connect signals to structured action—with evidence.", highlight_style))
    story.append(PageBreak())

    # === SLIDE 6: ONE PLATFORM, MULTIPLE ENTRY POINTS ===
    story.append(Paragraph("One Platform, Multiple Entry Points", slide_title_style))
    story.append(Paragraph("<b>Preventli Case Engine</b> (single workflow model)", large_body_style))
    story.append(Paragraph("A case can start as:", section_style))

    entry_points_data = [
        ['1', 'Anonymous speak-up'],
        ['2', 'Psychosocial hazard indicator (trend, hotspot, event)'],
        ['3', 'Early concern (pain, fatigue, absence pattern, performance shift)'],
        ['4', 'Injury / recovery-at-work / claim'],
        ['5', 'Complex/age-related capacity concern']
    ]

    entry_table = Table(entry_points_data, colWidths=[0.5*inch, 5*inch])
    entry_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), primary_blue),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, light_gray] * 3),
    ]))

    story.append(entry_table)
    story.append(PageBreak())

    # === SLIDE 7: WORKFLOW ===
    story.append(Paragraph("Preventli Workflow (End-to-End)", slide_title_style))

    workflow_data = [
        ['Step', 'Action', 'Outcome'],
        ['1. Capture', 'Anonymous or named intake', 'Structured signal recorded'],
        ['2. Classify', 'Case type + risk assessment', 'Appropriate workflow triggered'],
        ['3. Triage', 'Severity + urgency + controls', 'Priority and resources assigned'],
        ['4. Act', 'Tasks + timelines + owners', 'Accountable execution'],
        ['5. Evidence', 'Timestamped actions + rationale', 'Defensible audit trail'],
        ['6. Monitor', 'Anti-retaliation + progress', 'Protection and recovery tracking'],
        ['7. Learn', 'Controls effectiveness + trends', 'Continuous improvement']
    ]

    workflow_table = Table(workflow_data, colWidths=[1.2*inch, 2.4*inch, 2.4*inch])
    workflow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray] * 4),
    ]))

    story.append(workflow_table)
    story.append(PageBreak())

    # === SLIDE 8: SPEAK-UP MODULE ===
    story.append(Paragraph("Module 1: Speak-Up / Whistleblower", slide_title_style))
    story.append(Paragraph("<b>SafeSpeak (Preventli)</b> — speak-up channels with defensible handling:", section_style))

    safespeak_features = [
        "Anonymous, confidential reporting (mobile-first + QR)",
        "Structured intake (not free-text chaos)",
        "Eligible recipient routing (role-based access)",
        "Secure two-way messaging (optional)",
        "Audit trail by default"
    ]

    for feature in safespeak_features:
        story.append(Paragraph(f"• {feature}", bullet_style))

    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph('"Not a hotline. A safe entry into a prevention workflow."', highlight_style))
    story.append(PageBreak())

    # === SLIDE 9: PSYCHOSOCIAL MODULE ===
    story.append(Paragraph("Module 2: Psychosocial Hazard Management", slide_title_style))
    story.append(Paragraph("Psychosocial hazards require management, not PDFs. <b>Preventli operationalises it:</b>", large_body_style))

    psych_features = [
        "Hazard identification (categories, locations, teams, roles)",
        "Risk assessment (likelihood/impact, triggers, contributing factors)",
        "Controls library (elimination → substitution → admin → training/support)",
        "Consultation + action plans (owners, due dates)",
        "Monitoring (signals, recurrence, effectiveness)"
    ]

    for feature in psych_features:
        story.append(Paragraph(f"• {feature}", bullet_style))

    story.append(PageBreak())

    # === SLIDE 10: CONNECTION ===
    story.append(Paragraph("How Psychosocial + Speak-Up Connect", slide_title_style))
    story.append(Paragraph("<b>Speak-up reports become psychosocial hazard inputs.</b>", highlight_style))
    story.append(Paragraph("Example flows:", section_style))

    connection_examples = [
        'Multiple "work pressure" signals → hazard hotspot flagged',
        "Bullying signals in one crew → targeted controls + leadership intervention",
        '"Unsafe behaviour" reports → procedural control + supervision change'
    ]

    for example in connection_examples:
        story.append(Paragraph(f"• {example}", bullet_style))

    story.append(PageBreak())

    # === SLIDE 11: INJURY MODULE ===
    story.append(Paragraph("Module 3: Injury Management + Early Intervention", slide_title_style))
    story.append(Paragraph("<b>Preventli doesn't wait for claims.</b>", highlight_style))

    injury_features = [
        'Early discomfort / early reporting ("yellow flags")',
        "Case-based injury management",
        "Recovery-at-work plans (duties, schedule, restrictions)",
        "Medical/cert tracking + milestones",
        "Escalation management when complexity increases"
    ]

    for feature in injury_features:
        story.append(Paragraph(f"• {feature}", bullet_style))

    story.append(PageBreak())

    # === SLIDE 12: COMPLEX CASES ===
    story.append(Paragraph("Age-Related / Complex Cases", slide_title_style))
    story.append(Paragraph("<b>Complexity isn't rare—it's normal:</b>", large_body_style))

    complexity_challenges = [
        "Gradual decline, chronic conditions, mixed physical/psychosocial factors",
        "Legal sensitivity (privacy, discrimination risk)",
        "Fear-driven underreporting"
    ]

    for challenge in complexity_challenges:
        story.append(Paragraph(f"• {challenge}", bullet_style))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Preventli approach:</b>", section_style))

    approach_points = [
        "Supportive adjustments workflow (documented, reversible)",
        "Capability + risk conversations guided (not medical decisions)",
        "Evidence-based fairness (consistent actions, rationale logged)"
    ]

    for point in approach_points:
        story.append(Paragraph(f"• {point}", bullet_style))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph('<b>Important boundary:</b> "No diagnosis. No medical determination. Structured support + documented action."',
                 ParagraphStyle('Boundary', parent=body_style, textColor=warning_red, fontName='Helvetica-Bold')))
    story.append(PageBreak())

    # === SLIDE 13: SYSTEM MOAT ===
    story.append(Paragraph("The System Moat: Cases Can Evolve", slide_title_style))
    story.append(Paragraph("Real life isn't linear:", large_body_style))
    story.append(Paragraph("• Stress → conflict → complaint → injury → claim<br/>• Physical pain → anxiety → absenteeism → performance → dispute", body_style))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Preventli keeps one timeline and one truth:</b>", highlight_style))

    moat_benefits = [
        "Case type can evolve",
        "Evidence and actions persist",
        "Patterns connect across time"
    ]

    for benefit in moat_benefits:
        story.append(Paragraph(f"• {benefit}", bullet_style))

    story.append(PageBreak())

    # === SLIDE 14: AI ASSISTANCE ===
    story.append(Paragraph("AI Where It Actually Helps", slide_title_style))
    story.append(Paragraph("<b>AI = copilot, not judge.</b>", highlight_style))

    ai_used_for = [
        "Summarisation (clean, consistent briefs)",
        "Categorisation prompts",
        "Risk factor highlighting (psychosocial + injury flags)",
        "Suggested next-step checklists"
    ]

    ai_never_used = [
        "Findings, guilt, discipline, closure decisions",
        "Diagnosing conditions",
        "Replacing investigations"
    ]

    story.append(Paragraph("<b>Used for:</b>", section_style))
    for item in ai_used_for:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Paragraph("<b>Never used for:</b>", section_style))
    for item in ai_never_used:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(PageBreak())

    # === SLIDE 15: DASHBOARD ===
    story.append(Paragraph("Leadership Dashboard", slide_title_style))
    story.append(Paragraph("<b>Defensibility + early warning without exposure</b>", highlight_style))

    dashboard_features = [
        "Leading indicators: speak-up volume, hotspots, recurrence",
        "Response metrics: time-to-triage, time-to-first-action",
        "Control effectiveness: repeated signals after interventions",
        "Injury outcomes: recovery progress, recurrence, cost drivers",
        "Board-ready export packs (de-identified options)"
    ]

    for feature in dashboard_features:
        story.append(Paragraph(f"• {feature}", bullet_style))

    story.append(PageBreak())

    # === SLIDE 16: SALES WEDGE ===
    story.append(Paragraph("The Sales Wedge", slide_title_style))
    story.append(Paragraph("<b>Wedge</b> = existing injury/early intervention pain (easy ROI story)<br/><b>Expansion</b> = psychosocial compliance + speak-up defensibility (urgency story)", large_body_style))

    story.append(Paragraph("Land and expand narrative:", section_style))

    land_expand_data = [
        ['1', 'Fix your early intervention + injury complexity'],
        ['2', 'Add psychosocial hazard management'],
        ['3', 'Add SafeSpeak (whistleblower/speak-up)']
    ]

    land_expand_table = Table(land_expand_data, colWidths=[0.5*inch, 5*inch])
    land_expand_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), success_green),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
    ]))

    story.append(land_expand_table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>This makes Preventli a platform, not a point tool.</b>", highlight_style))
    story.append(PageBreak())

    # === SLIDE 17: PRICING ===
    story.append(Paragraph("Packaging & Pricing", slide_title_style))

    pricing_data = [
        ['Tier', 'Features', 'Price (AUD/month)'],
        ['Starter', 'Early intervention + core case engine', 'From $299'],
        ['Growth', '+ injury management depth + dashboards', 'From $699'],
        ['Multi-site', '+ psychosocial controls at scale + advanced reporting', 'From $1,500']
    ]

    pricing_table = Table(pricing_data, colWidths=[1.2*inch, 3*inch, 1.8*inch])
    pricing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray] * 2),
    ]))

    story.append(pricing_table)
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Add-ons:</b> External intake/hotline partner, advanced analytics/insurer packs", body_style))
    story.append(PageBreak())

    # === SLIDE 18: COMPETITIVE POSITIONING ===
    story.append(Paragraph("Competitive Positioning", slide_title_style))

    competitive_data = [
        ['Competitors typically:', 'Preventli is different:'],
        ['Capture a report and stop', 'Built around execution + evidence'],
        ['Sell "compliance optics"', 'Unifies signals, hazards, injuries, complexity'],
        ['Create a second system leaders don\'t use', 'Makes action easy—and omission obvious'],
        ['Leave action and proof to humans', 'Turns reporting into prevention']
    ]

    competitive_table = Table(competitive_data, colWidths=[3*inch, 3*inch])
    competitive_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), warning_red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (1, 0), (1, 0), success_green),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray] * 2),
    ]))

    story.append(competitive_table)
    story.append(Spacer(1, 0.4*inch))
    story.append(Paragraph('"Preventli turns reporting into prevention."', highlight_style))
    story.append(PageBreak())

    # === STRESS TEST SECTION ===
    story.append(Paragraph("STRESS TEST", ParagraphStyle('StressTitle', parent=slide_title_style, textColor=warning_red)))
    story.append(Paragraph("Baking credibility into the pitch", section_style))
    story.append(PageBreak())

    # === STRESS TEST 1 ===
    story.append(Paragraph('Stress Test: "Is This Too Broad?"', slide_title_style))
    story.append(Paragraph('<b>Objection:</b> "Whistleblowing + psychosocial + injury = 3 products."', large_body_style))
    story.append(Paragraph('<b>Answer:</b> It\'s <b>one case engine</b> with <b>multiple entry points</b>.', highlight_style))
    story.append(Paragraph("Same owners, tasks, evidence, audit, escalation.", body_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Proof point:</b> A bullying complaint, psychosocial hazard, and injury often become <i>one</i> dispute later. Preventli keeps it coherent from day one.", body_style))
    story.append(PageBreak())

    # === STRESS TEST 2 ===
    story.append(Paragraph('Stress Test: "Won\'t This Create More Liability?"', slide_title_style))
    story.append(Paragraph('<b>Objection:</b> "If we record everything, we\'ll be exposed."', large_body_style))
    story.append(Paragraph("<b>Answer:</b> You're exposed either way. The difference is:", section_style))

    liability_points = [
        "Without records = you look negligent or inconsistent",
        "With records = you demonstrate reasonable steps and fairness"
    ]

    for point in liability_points:
        story.append(Paragraph(f"• {point}", bullet_style))

    story.append(Paragraph("Mitigations:", section_style))
    mitigations = [
        "Clear governance + role-based access",
        "Confidentiality by design",
        "Consistent workflows reduce ad hoc mistakes",
        "De-identified leadership dashboards"
    ]

    for mitigation in mitigations:
        story.append(Paragraph(f"• {mitigation}", bullet_style))

    story.append(PageBreak())

    # === STRESS TEST 3 ===
    story.append(Paragraph('Stress Test: "What If We Get Flooded?"', slide_title_style))
    story.append(Paragraph('<b>Objection:</b> "Anonymous reports will explode."', large_body_style))
    story.append(Paragraph('<b>Answer:</b> If you\'re flooded, you had a real problem—Preventli helps you <b>triage + prioritise</b> and apply controls, not drown.', highlight_style))

    flood_mitigations = [
        "Structured intake reduces noise",
        "Severity triage lanes",
        "Templates for common actions",
        "Hotspot detection to treat root causes"
    ]

    story.append(Paragraph("Mitigations:", section_style))
    for mitigation in flood_mitigations:
        story.append(Paragraph(f"• {mitigation}", bullet_style))

    story.append(PageBreak())

    # === FINAL STRESS TEST: RISKS ===
    story.append(Paragraph("Risk & Mitigation", slide_title_style))
    story.append(Paragraph("Key risks (being honest):", section_style))

    risks_mitigations_data = [
        ['Risk', 'Mitigation'],
        ['Confidentiality breaches', 'Strict access controls + audit logs'],
        ['Retaliation mishandling', 'Built-in anti-retaliation monitoring'],
        ['Poor adoption ("back to email")', 'Mandatory task checklists for high-risk cases'],
        ['AI misinterpretation', 'AI advisory-only, human sign-off'],
        ['Inconsistent case handling', 'Rollout playbook + internal champion model']
    ]

    risks_table = Table(risks_mitigations_data, colWidths=[2.5*inch, 3.5*inch])
    risks_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), warning_red),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray] * 3),
    ]))

    story.append(risks_table)
    story.append(PageBreak())

    # === CLOSE ===
    story.append(Paragraph("Close", slide_title_style))
    story.append(Paragraph("<b>Preventli is not a new bet. It's a deepening of what already works.</b>", highlight_style))

    closing_points = [
        "Market urgency is rising (psychosocial + speak-up expectations)",
        "SMBs are under-tooled and over-exposed",
        "Preventli unifies what's currently fragmented",
        "The value is execution + proof, not intake"
    ]

    for point in closing_points:
        story.append(Paragraph(f"• {point}", bullet_style))

    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph('"Preventli turns weak signals into strong outcomes."',
                 ParagraphStyle('FinalLine', parent=highlight_style, fontSize=24, textColor=primary_blue)))

    # Build PDF
    doc.build(story)
    print(f"Created stylish pitch deck: {filename}")
    print(f"Modern presentation format with clean design")
    print(f"Includes full stress-test section for credibility")
    print(f"Ready for investor meetings and strategic discussions")

    return filename

if __name__ == "__main__":
    create_preventli_pitch_deck()