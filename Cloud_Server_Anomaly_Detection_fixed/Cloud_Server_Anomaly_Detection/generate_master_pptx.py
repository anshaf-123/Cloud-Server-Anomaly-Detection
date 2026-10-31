import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# COLOR PALETTE & DESIGN TOKENS (Currex-inspired Tech / Navy Palette)
# ==============================================================================
COLOR_BG_LIGHT = RGBColor(248, 250, 252)       # Slate 50 (#F8FAFC)
COLOR_NAVY_DARK = RGBColor(15, 23, 42)          # Slate 900 (#0F172A)
COLOR_NAVY_CARD = RGBColor(30, 41, 59)          # Slate 800 (#1E293B)
COLOR_NAVY_BORDER = RGBColor(51, 65, 85)        # Slate 700 (#334155)

COLOR_BLUE_PRIMARY = RGBColor(2, 132, 199)      # Sky 600 (#0284C7)
COLOR_BLUE_ACCENT = RGBColor(56, 189, 248)      # Sky 400 (#38BDF8)
COLOR_BLUE_DARK = RGBColor(3, 105, 161)         # Sky 700 (#0369A1)
COLOR_BLUE_BG = RGBColor(240, 249, 255)         # Sky 50 (#F0F9FF)
COLOR_BLUE_BORDER = RGBColor(186, 230, 253)     # Sky 200 (#BAE6FD)

COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_DARK_TEXT = RGBColor(15, 23, 42)          # Slate 900
COLOR_GRAY_TEXT = RGBColor(100, 116, 139)       # Slate 500 (#64748B)
COLOR_LIGHT_TEXT = RGBColor(148, 163, 184)      # Slate 400 (#94A3B8)
COLOR_MUTED_TEXT = RGBColor(203, 213, 225)      # Slate 300 (#CBD5E1)

COLOR_CARD_BG = RGBColor(255, 255, 255)         # Card White
COLOR_CARD_BORDER = RGBColor(226, 232, 240)     # Slate 200 (#E2E8F0)

COLOR_ALERT_RED = RGBColor(239, 68, 68)         # Red 500 (#EF4444)
COLOR_ALERT_BG = RGBColor(254, 242, 242)        # Red 50 (#FEF2F2)
COLOR_ALERT_BORDER = RGBColor(254, 202, 202)    # Red 200 (#FECACA)

COLOR_SUCCESS_GREEN = RGBColor(16, 185, 129)    # Emerald 500 (#10B981)
COLOR_SUCCESS_BG = RGBColor(236, 253, 245)      # Emerald 50
COLOR_SUCCESS_BORDER = RGBColor(167, 243, 208)

COLOR_WARN_AMBER = RGBColor(245, 158, 11)       # Amber 500 (#F59E0B)
COLOR_WARN_BG = RGBColor(255, 251, 235)         # Amber 50
COLOR_WARN_BORDER = RGBColor(254, 243, 199)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"

PROJECT_DIR = Path(__file__).parent.resolve()
FIGURES_DIR = PROJECT_DIR / "results" / "figures"

# ==============================================================================
# REUSABLE DRAWING HELPERS
# ==============================================================================
def apply_slide_bg(slide, color=COLOR_BG_LIGHT):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, section_tag, title, subtitle):
    tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.38), Inches(2.3), Inches(0.32))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = COLOR_BLUE_BG
    tag_box.line.color.rgb = COLOR_BLUE_BORDER
    tag_box.line.width = Pt(1)
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = section_tag.upper()
    p_tag.font.name = FONT_HEADING
    p_tag.font.size = Pt(9.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_BLUE_PRIMARY
    p_tag.alignment = PP_ALIGN.CENTER

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.70), Inches(11.733), Inches(0.52))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = Inches(0)
    tf_title.margin_top = Inches(0)
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_DARK_TEXT

    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(11.733), Inches(0.32))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = Inches(0)
    tf_sub.margin_top = Inches(0)
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(11.5)
    p_sub.font.color.rgb = COLOR_GRAY_TEXT

def add_footer(slide, slide_num, total_slides=18):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.02), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_CARD_BORDER
    line.line.fill.background()

    foot_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(8.0), Inches(0.3))
    tf_left = foot_left.text_frame
    tf_left.margin_left = Inches(0)
    p_left = tf_left.paragraphs[0]
    p_left.text = "CloudGuard | Intelligent Cloud Server Anomaly Detection System — B.Tech Project Presentation"
    p_left.font.name = FONT_BODY
    p_left.font.size = Pt(9.5)
    p_left.font.color.rgb = COLOR_LIGHT_TEXT

    foot_right = slide.shapes.add_textbox(Inches(10.533), Inches(7.08), Inches(2.0), Inches(0.3))
    tf_right = foot_right.text_frame
    tf_right.margin_right = Inches(0)
    p_right = tf_right.paragraphs[0]
    p_right.text = f"{slide_num:02d} / {total_slides:02d}"
    p_right.font.name = FONT_BODY
    p_right.font.size = Pt(9.5)
    p_right.font.bold = True
    p_right.font.color.rgb = COLOR_GRAY_TEXT
    p_right.alignment = PP_ALIGN.RIGHT

def create_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER, border_width=1):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card

def add_bullet_item(tf, bold_label, text_body, is_first=False, font_size=10.0, bullet_color=COLOR_BLUE_PRIMARY):
    p = tf.paragraphs[0] if is_first else tf.add_paragraph()
    p.space_after = Pt(4)
    p.font.size = Pt(font_size)
    p.font.name = FONT_BODY

    run_bullet = p.add_run()
    run_bullet.text = "▪ "
    run_bullet.font.bold = True
    run_bullet.font.color.rgb = bullet_color

    run_title = p.add_run()
    run_title.text = bold_label + ": "
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_DARK_TEXT

    run_desc = p.add_run()
    run_desc.text = text_body
    run_desc.font.color.rgb = COLOR_GRAY_TEXT

# ==============================================================================
# SLIDE 1: COVER SLIDE
# ==============================================================================
def build_slide_01(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide, COLOR_NAVY_DARK)

    accent_bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.1))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = COLOR_NAVY_CARD
    accent_bar.line.color.rgb = COLOR_NAVY_BORDER
    accent_bar.line.width = Pt(1.5)

    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.15), Inches(3.6), Inches(0.38))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(12, 74, 110)
    pill.line.color.rgb = COLOR_BLUE_PRIMARY
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    tf_pill.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = "⚡ CLOUDGUARD OBSERVABILITY"
    p_pill.font.name = FONT_HEADING
    p_pill.font.size = Pt(11)
    p_pill.font.bold = True
    p_pill.font.color.rgb = COLOR_BLUE_ACCENT
    p_pill.alignment = PP_ALIGN.CENTER

    t_box = slide.shapes.add_textbox(Inches(1.3), Inches(1.68), Inches(10.7), Inches(1.6))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = Inches(0)
    p_t = tf_t.paragraphs[0]
    p_t.text = "CLOUD SERVER\nANOMALY DETECTION SYSTEM"
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(36)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE
    p_t.line_spacing = 1.05

    sub_box = slide.shapes.add_textbox(Inches(1.3), Inches(3.40), Inches(10.7), Inches(0.5))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = Inches(0)
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Intelligent Cloud Server Monitoring & Multi-Model Anomaly Detection Framework"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(14.5)
    p_sub.font.color.rgb = COLOR_BLUE_ACCENT

    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.3), Inches(4.02), Inches(10.733), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_NAVY_BORDER
    div.line.fill.background()

    # Left Team Details Card
    team_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(4.25), Inches(5.2), Inches(2.2))
    team_card.fill.solid()
    team_card.fill.fore_color.rgb = RGBColor(15, 23, 42)
    team_card.line.color.rgb = COLOR_NAVY_BORDER
    team_card.line.width = Pt(1)
    tf_team = team_card.text_frame
    tf_team.margin_left = Inches(0.25)
    tf_team.margin_top = Inches(0.2)
    
    p_lbl = tf_team.paragraphs[0]
    p_lbl.text = "PROJECT TEAM MEMBERS"
    p_lbl.font.name = FONT_HEADING
    p_lbl.font.size = Pt(10)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_BLUE_ACCENT
    p_lbl.space_after = Pt(6)

    members = [
        "1. Muhammed Anzil P P",
        "2. Fadhil Haneef",
        "3. [Team Member 3 / Student Roll No.]"
    ]
    for m in members:
        p_m = tf_team.add_paragraph()
        p_m.text = m
        p_m.font.name = FONT_BODY
        p_m.font.size = Pt(11)
        p_m.font.bold = True
        p_m.font.color.rgb = COLOR_WHITE
        p_m.space_after = Pt(3)

    # Right Academic Details Card
    acad_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.25), Inches(5.2), Inches(2.2))
    acad_card.fill.solid()
    acad_card.fill.fore_color.rgb = RGBColor(15, 23, 42)
    acad_card.line.color.rgb = COLOR_NAVY_BORDER
    acad_card.line.width = Pt(1)
    tf_acad = acad_card.text_frame
    tf_acad.margin_left = Inches(0.25)
    tf_acad.margin_top = Inches(0.2)

    p_albl = tf_acad.paragraphs[0]
    p_albl.text = "ACADEMIC PROGRAM & INSTITUTION"
    p_albl.font.name = FONT_HEADING
    p_albl.font.size = Pt(10)
    p_albl.font.bold = True
    p_albl.font.color.rgb = COLOR_BLUE_ACCENT
    p_albl.space_after = Pt(6)

    acad_items = [
        ("Program", "Bachelor of Technology (B.Tech)"),
        ("Department", "Department of Computer Science & Engineering"),
        ("Academic Year", "2025 – 2026"),
        ("Institution", "[College / University Name]")
    ]
    for label, val in acad_items:
        p_a = tf_acad.add_paragraph()
        p_a.space_after = Pt(3)
        r1 = p_a.add_run()
        r1.text = f"{label}: "
        r1.font.name = FONT_BODY
        r1.font.size = Pt(10.5)
        r1.font.bold = True
        r1.font.color.rgb = COLOR_LIGHT_TEXT

        r2 = p_a.add_run()
        r2.text = val
        r2.font.name = FONT_BODY
        r2.font.size = Pt(10.5)
        r2.font.bold = False
        r2.font.color.rgb = COLOR_WHITE

# ==============================================================================
# SLIDE 2: CONTENTS
# ==============================================================================
def build_slide_02(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "02 | Contents", "Presentation Outline", "Structured presentation of the B.Tech project in compliance with academic requirements")
    add_footer(slide, 2)

    sections = [
        ("01", "Introduction", "Cloud infrastructure reliability & performance telemetry background"),
        ("02", "Problem Definition", "Challenges of high-volume telemetry & manual anomaly inspection"),
        ("03", "Proposed System", "Centralized CloudGuard framework & dual-layer detection design"),
        ("04", "Module Description", "Detailed architecture of verified data, ML, and API modules"),
        ("05", "System Architecture", "End-to-end 5-tier architecture from data ingestion to dashboard"),
        ("06", "System Requirements", "Hardware and verified software technology prerequisites"),
        ("07", "Implementation & Tech Stack", "Roles of Python, Scikit-learn, PySpark, Flask, and JS frontend"),
        ("08", "Experimental Results", "Dataset analysis and empirical results across 12,096 observations"),
        ("09", "Anomaly Detection Analysis", "Isolation Forest vs. LOF cross-validation & threshold rules"),
        ("10", "Conclusion & Future Scope", "Project summary, references, and planned future cloud roadmap")
    ]

    col_width = 5.7
    card_height = 0.88
    top_base = 1.75
    y_gap = 0.16

    for i, (num, title, desc) in enumerate(sections):
        col = i // 5
        row = i % 5
        x = 0.8 + col * (col_width + 0.33)
        y = top_base + row * (card_height + y_gap)

        card = create_card(slide, x, y, col_width, card_height)

        num_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.18), Inches(y + 0.18), Inches(0.72), Inches(0.52))
        num_pill.fill.solid()
        num_pill.fill.fore_color.rgb = COLOR_BLUE_PRIMARY
        num_pill.line.fill.background()
        tf_num = num_pill.text_frame
        tf_num.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_num = tf_num.paragraphs[0]
        p_num.text = num
        p_num.font.name = FONT_HEADING
        p_num.font.size = Pt(14)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_WHITE
        p_num.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x + 1.05), Inches(y + 0.1), Inches(col_width - 1.2), Inches(card_height - 0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0)
        tf.margin_top = Inches(0)

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_DARK_TEXT
        p1.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_GRAY_TEXT

# ==============================================================================
# SLIDE 3: INTRODUCTION
# ==============================================================================
def build_slide_03(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "03 | Introduction", "Cloud Server Monitoring & System Reliability", "Understanding performance telemetry and the critical role of proactive anomaly detection")
    add_footer(slide, 3)

    cards = [
        ("Cloud Infrastructure Telemetry", [
            ("Infrastructure Growth", "Modern enterprise computing relies heavily on multi-tenant cloud servers."),
            ("Continuous Metric Stream", "Servers continuously generate operational performance telemetry at fine sampling intervals."),
            ("Key Telemetry Types", "Crucial resource metrics include CPU usage %, virtual memory %, disk write I/O, and network ingress/egress throughput."),
            ("Telemetry Significance", "Real-time metrics reflect the operational health, service quality, and stability of host instances.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG, COLOR_BLUE_BORDER),

        ("The Anomaly Challenge", [
            ("Root Causes of Anomalies", "Sudden or unusual changes indicate runaway processes, memory leaks, hardware degradation, or cyber intrusion."),
            ("Silent Degradation", "Resource exhaustion can silently slow response latencies before catastrophic host crashes occur."),
            ("Multivariate Complexity", "Anomalies rarely occur in isolation; they manifest across correlated metrics simultaneously."),
            ("Need for Early Triage", "Continuous automated monitoring is required to identify degradation before SLAs are breached.")
        ], COLOR_ALERT_RED, COLOR_ALERT_BG, COLOR_ALERT_BORDER),

        ("The CloudGuard Solution", [
            ("Unified Monitoring", "CloudGuard provides a centralized monitoring dashboard and automated anomaly detection platform."),
            ("Dual-Layer Methodology", "Combines instant rule-based operational thresholds for zero-overhead triage with deep offline ML ensembles."),
            ("Academic Rigour", "Grounded in real-world server benchmarks (NAB AWS CloudWatch) and standard OS metric instrumentation."),
            ("Operator Usability", "Delivers visual, non-blocking telemetry streaming for system administrators during viva and production.")
        ], COLOR_SUCCESS_GREEN, COLOR_SUCCESS_BG, COLOR_SUCCESS_BORDER)
    ]

    card_width = 3.65
    card_height = 4.25
    x_base = 0.8
    gap = 0.38
    y_pos = 1.75

    for i, (title, items, border_c, bg_c, header_border) in enumerate(cards):
        x = x_base + i * (card_width + gap)
        card = create_card(slide, x, y_pos, card_width, card_height)

        # Header bar
        hbar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.15), Inches(y_pos + 0.15), Inches(card_width - 0.3), Inches(0.48))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = bg_c
        hbar.line.color.rgb = header_border
        hbar.line.width = Pt(1)
        tf_h = hbar.text_frame
        tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_h = tf_h.paragraphs[0]
        p_h.text = title.upper()
        p_h.font.name = FONT_HEADING
        p_h.font.size = Pt(10.5)
        p_h.font.bold = True
        p_h.font.color.rgb = border_c
        p_h.alignment = PP_ALIGN.CENTER

        # Bullet content
        tb = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y_pos + 0.75), Inches(card_width - 0.4), Inches(card_height - 0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0)
        tf.margin_top = Inches(0)

        for j, (lbl, txt) in enumerate(items):
            add_bullet_item(tf, lbl, txt, is_first=(j==0), font_size=10.0, bullet_color=border_c)

    # Bottom Summary Strip
    strip = create_card(slide, 0.8, 6.18, 11.733, 0.65, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)
    tb_s = slide.shapes.add_textbox(Inches(0.9), Inches(6.22), Inches(11.533), Inches(0.55))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True
    p_s = tf_s.paragraphs[0]
    p_s.text = "KEY TAKEAWAY: Modern cloud servers cannot rely on manual triage. CloudGuard bridges the gap between raw hardware metrics and intelligent anomaly alerts through automated, centralized observability."
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(11)
    p_s.font.bold = True
    p_s.font.color.rgb = COLOR_DARK_TEXT
    p_s.alignment = PP_ALIGN.CENTER

# ==============================================================================
# SLIDE 4: PROBLEM DEFINITION
# ==============================================================================
def build_slide_04(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "04 | Problem Definition", "Challenges in Cloud Telemetry & Anomaly Identification", "Overcoming the limitations of manual inspection and isolated metric alerting")
    add_footer(slide, 4)

    # Process Flow Diagram (5 Steps)
    flow_steps = [
        ("SERVER METRICS", "High-velocity CPU, RAM, disk, & network streams emitted"),
        ("HIGH DATA VOLUME", "Continuous 5-minute sampling yields massive datasets"),
        ("MANUAL TRIAGE BOTTLENECK", "Humans cannot evaluate hundreds of streams concurrently"),
        ("DELAYED IDENTIFICATION", "Silent resource leaks propagate unnoticed"),
        ("PERFORMANCE OUTAGES", "Cascading degradation, SLA penalties, and crashes")
    ]

    step_w = 2.05
    step_h = 0.95
    step_gap = 0.37
    x_start = 0.8
    y_flow = 1.75

    for i, (stitle, sdesc) in enumerate(flow_steps):
        x = x_start + i * (step_w + step_gap)
        is_last = (i == len(flow_steps) - 1)
        bg = COLOR_ALERT_BG if is_last else COLOR_BLUE_BG
        border = COLOR_ALERT_BORDER if is_last else COLOR_BLUE_BORDER
        tcolor = COLOR_ALERT_RED if is_last else COLOR_BLUE_PRIMARY

        box = create_card(slide, x, y_flow, step_w, step_h, bg_color=bg, border_color=border)
        tb = slide.shapes.add_textbox(Inches(x + 0.08), Inches(y_flow + 0.1), Inches(step_w - 0.16), Inches(step_h - 0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0)
        tf.margin_top = Inches(0)
        p1 = tf.paragraphs[0]
        p1.text = stitle
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = tcolor
        p1.alignment = PP_ALIGN.CENTER
        p1.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = sdesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = COLOR_GRAY_TEXT
        p2.alignment = PP_ALIGN.CENTER

        # Add Arrow connector
        if i < len(flow_steps) - 1:
            arrow_x = x + step_w + 0.08
            arrow_y = y_flow + step_h / 2 - 0.15
            arr = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(arrow_x), Inches(arrow_y), Inches(0.22), Inches(0.3))
            arr.fill.solid()
            arr.fill.fore_color.rgb = COLOR_GRAY_TEXT
            arr.line.fill.background()

    # 3 Problem Dimension Cards
    dim_cards = [
        ("High Telemetry Velocity & Scale", [
            ("Data Inundation", "A medium cloud deployment with 50 servers generates over 14,400 data points daily at 5-minute sampling."),
            ("Information Overload", "Alert fatigue sets in when operators are bombarded by raw notifications without contextual severity scoring."),
            ("Storage & Ingestion Costs", "Raw telemetry requires optimized pipelines to validate, store, and preprocess metrics without causing latency.")
        ]),
        ("Siloed & Static Threshold Limitations", [
            ("Isolated Boundaries", "Conventional monitoring tools check CPU, memory, and disk separately with static percentage limits."),
            ("Invisible Compound Anomalies", "Failures often stem from subtle inter-dependencies—such as moderate CPU spikes coinciding with heavy disk queue length."),
            ("High False-Positive Rates", "Static thresholds trigger false alarms during planned spikes while missing silent, creeping memory leaks.")
        ]),
        ("Operational Downtime & Detection Lag", [
            ("Prolonged MTTD", "Manual investigation results in delayed Mean Time to Detect (MTTD), allowing degradation to impact end-users."),
            ("Cascading Failures", "An undetected bottleneck on a database or EC2 instance can propagate downstream to load balancers and web APIs."),
            ("Need for Unified Dashboard", "Administrators require a consolidated single-pane-of-glass dashboard providing real-time triage.")
        ])
    ]

    cd_w = 3.65
    cd_h = 3.8
    y_dims = 2.95

    for i, (dtitle, ditems) in enumerate(dim_cards):
        x = x_start + i * (cd_w + 0.38)
        card = create_card(slide, x, y_dims, cd_w, cd_h)

        # Title Pill
        tpill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.15), Inches(y_dims + 0.15), Inches(cd_w - 0.3), Inches(0.42))
        tpill.fill.solid()
        tpill.fill.fore_color.rgb = COLOR_BLUE_BG
        tpill.line.color.rgb = COLOR_BLUE_BORDER
        tpill.line.width = Pt(1)
        tf_tp = tpill.text_frame
        tf_tp.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_tp = tf_tp.paragraphs[0]
        p_tp.text = dtitle.upper()
        p_tp.font.name = FONT_HEADING
        p_tp.font.size = Pt(10)
        p_tp.font.bold = True
        p_tp.font.color.rgb = COLOR_BLUE_PRIMARY
        p_tp.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y_dims + 0.68), Inches(cd_w - 0.4), Inches(cd_h - 0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0)
        tf.margin_top = Inches(0)

        for j, (lbl, txt) in enumerate(ditems):
            add_bullet_item(tf, lbl, txt, is_first=(j==0), font_size=9.8, bullet_color=COLOR_ALERT_RED)

# ==============================================================================
# SLIDE 5: PROPOSED SYSTEM
# ==============================================================================
def build_slide_05(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "05 | Proposed System", "The CloudGuard Framework: Dual-Layer Architecture", "A unified system integrating low-latency real-time thresholding with deep machine learning")
    add_footer(slide, 5)

    # Top Pipeline Cards (Step Flow)
    pipe_steps = [
        "System Metrics Ingestion",
        "Data Validation & Preprocessing",
        "Dual Anomaly Detection",
        "Flask REST API Services",
        "CloudGuard Web Dashboard",
        "Live Operational Triage"
    ]
    p_w = 1.80
    p_h = 0.55
    p_gap = 0.18
    p_x = 0.8
    y_pipe = 1.75

    for i, step in enumerate(pipe_steps):
        x = p_x + i * (p_w + p_gap)
        card = create_card(slide, x, y_pipe, p_w, p_h, bg_color=COLOR_BLUE_BG, border_color=COLOR_BLUE_BORDER)
        tb = slide.shapes.add_textbox(Inches(x + 0.05), Inches(y_pipe + 0.05), Inches(p_w - 0.1), Inches(p_h - 0.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = f"{i+1}. {step}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_BLUE_PRIMARY
        p.alignment = PP_ALIGN.CENTER

    # 2 Big Architectural Layer Cards
    col_w = 5.7
    card_h = 4.35
    y_card = 2.50

    # Layer 1: Real-Time Operational Triage
    card_l1 = create_card(slide, 0.8, y_card, col_w, card_h)
    
    h_pill1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(y_card + 0.2), Inches(col_w - 0.4), Inches(0.42))
    h_pill1.fill.solid()
    h_pill1.fill.fore_color.rgb = COLOR_SUCCESS_BG
    h_pill1.line.color.rgb = COLOR_SUCCESS_BORDER
    h_pill1.line.width = Pt(1)
    tf_hp1 = h_pill1.text_frame
    tf_hp1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_hp1 = tf_hp1.paragraphs[0]
    p_hp1.text = "LAYER 1: REAL-TIME OPERATIONAL TRIAGE (LIVE SYSTEM)"
    p_hp1.font.name = FONT_HEADING
    p_hp1.font.size = Pt(10.5)
    p_hp1.font.bold = True
    p_hp1.font.color.rgb = COLOR_SUCCESS_GREEN
    p_hp1.alignment = PP_ALIGN.CENTER

    tb_l1 = slide.shapes.add_textbox(Inches(1.0), Inches(y_card + 0.72), Inches(col_w - 0.4), Inches(card_h - 0.85))
    tf_l1 = tb_l1.text_frame
    tf_l1.word_wrap = True
    tf_l1.margin_left = Inches(0)
    tf_l1.margin_top = Inches(0)

    l1_items = [
        ("Implementation Purpose", "Provide zero-latency, transparent real-time status monitoring for the live server dashboard."),
        ("Live Telemetry Harvesting", "Uses Python psutil library to collect active CPU utilization %, virtual memory %, and disk storage % directly from the host system."),
        ("Configured Threshold Boundaries", "Applies evaluate_metric() rules: Warning at 70% CPU, 75% RAM, 80% Disk; Anomaly at 85% CPU, 90% RAM, 90% Disk."),
        ("Status Classification", "Synthesizes individual metric evaluations into overall system states: HEALTHY, WARNING, or ANOMALY DETECTED."),
        ("REST API Delivery", "Flask endpoint /api/metrics delivers live JSON payload to frontend every 3 seconds without computational overhead."),
        ("Modularity", "Designed as an interchangeable interface (evaluate_metric) allowing deep ML models to plug in without changing API contracts.")
    ]
    for j, (lbl, txt) in enumerate(l1_items):
        add_bullet_item(tf_l1, lbl, txt, is_first=(j==0), font_size=9.5, bullet_color=COLOR_SUCCESS_GREEN)

    # Layer 2: Deep Behavioral Analytics
    card_l2 = create_card(slide, 6.833, y_card, col_w, card_h)

    h_pill2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.033), Inches(y_card + 0.2), Inches(col_w - 0.4), Inches(0.42))
    h_pill2.fill.solid()
    h_pill2.fill.fore_color.rgb = COLOR_BLUE_BG
    h_pill2.line.color.rgb = COLOR_BLUE_BORDER
    h_pill2.line.width = Pt(1)
    tf_hp2 = h_pill2.text_frame
    tf_hp2.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_hp2 = tf_hp2.paragraphs[0]
    p_hp2.text = "LAYER 2: DEEP BEHAVIORAL ANALYTICS (ML PIPELINE)"
    p_hp2.font.name = FONT_HEADING
    p_hp2.font.size = Pt(10.5)
    p_hp2.font.bold = True
    p_hp2.font.color.rgb = COLOR_BLUE_PRIMARY
    p_hp2.alignment = PP_ALIGN.CENTER

    tb_l2 = slide.shapes.add_textbox(Inches(7.033), Inches(y_card + 0.72), Inches(col_w - 0.4), Inches(card_h - 0.85))
    tf_l2 = tb_l2.text_frame
    tf_l2.word_wrap = True
    tf_l2.margin_left = Inches(0)
    tf_l2.margin_top = Inches(0)

    l2_items = [
        ("Implementation Purpose", "Detect complex multivariate outliers and subtle behavioural shifts across multi-server telemetry history."),
        ("Benchmark Dataset", "Evaluates 12,096 observations across 3 cloud servers (SERVER-01, 02, 03) from Numenta Anomaly Benchmark (NAB)."),
        ("1-Hour Rolling Features", "Calculates 12-step look-back rolling averages, moving standard deviations, and first-order metric changes (feature_engineering.py)."),
        ("Multi-Model ML Ensemble", "Trains Isolation Forest (n_estimators=100) and Local Outlier Factor (n_neighbors=20) on normalized telemetry."),
        ("Ensemble Severity Scoring", "Categorizes predictions into NORMAL (10,972), POSSIBLE_ANOMALY (1,038), and HIGH_CONFIDENCE_ANOMALY (86)."),
        ("Big Data PySpark Aggregation", "PySpark pipeline (pyspark/server_aggregation.py) computes server-level summary statistics at scale.")
    ]
    for j, (lbl, txt) in enumerate(l2_items):
        add_bullet_item(tf_l2, lbl, txt, is_first=(j==0), font_size=9.5, bullet_color=COLOR_BLUE_PRIMARY)

print("Slide 3, 4, 5 defined")


# ==============================================================================
# SLIDE 6: MODULE DESCRIPTION
# ==============================================================================
def build_slide_06(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "06 | Module Description", "Core Implemented Modules in CloudGuard", "Detailed overview of the six functional modules implemented in the project codebase")
    add_footer(slide, 6)

    modules = [
        ("1. Data Collection & Benchmark Ingestion", [
            ("Live OS Ingestion", "psutil library queries active host CPU %, virtual memory %, and disk storage %."),
            ("Benchmark Loader", "data_loader.py ingests Numenta Anomaly Benchmark (NAB) CloudWatch files for EC2 and RDS."),
            ("Multivariate Capture", "Collects CPU, memory, disk write I/O, network traffic, response time, and request rate.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG, COLOR_BLUE_BORDER),

        ("2. Data Validation & Preprocessing", [
            ("Schema Enforcement", "data_validator.py validates column names, data types, timestamp alignment, and null values."),
            ("MinMax Normalization", "data_processor.py fits and transforms metrics into [0, 1] range to avoid magnitude bias."),
            ("State Serialization", "Fitted scaler is serialized to models/scaler.joblib for consistent inference.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG, COLOR_BLUE_BORDER),

        ("3. Temporal Feature Engineering", [
            ("1-Hour Lookback Window", "feature_engineering.py groups data by server_id and calculates 12-step rolling moving averages."),
            ("Volatility Extraction", "Computes rolling standard deviations to capture sudden variance bursts."),
            ("Rate-of-Change", "Calculates first-order differentials to highlight steep spikes before threshold breaches.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG, COLOR_BLUE_BORDER),

        ("4. Machine Learning Detection Module", [
            ("Isolation Forest", "sklearn IsolationForest (n_estimators=100, contamination=0.05) isolates multi-dimensional outliers."),
            ("Local Outlier Factor", "LOF (n_neighbors=20, contamination=0.05) evaluates local density deviations."),
            ("Ensemble Classification", "Combines outputs into NORMAL, POSSIBLE_ANOMALY, and HIGH_CONFIDENCE_ANOMALY.")
        ], COLOR_ALERT_RED, COLOR_ALERT_BG, COLOR_ALERT_BORDER),

        ("5. Big Data Aggregation Module", [
            ("Distributed Pipeline", "Local PySpark engine (pyspark/server_aggregation.py) processes historical metric datasets."),
            ("Statistical Aggregation", "Computes server-wise mean, stddev, min, and max across millions of records."),
            ("Enterprise Scalability", "Demonstrates distributed Big Data capability ready for multi-node cloud clusters.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG, COLOR_BLUE_BORDER),

        ("6. Backend API & Web Dashboard", [
            ("Flask REST API", "website/api/app.py provides lightweight JSON endpoints (/api/metrics, /api/health)."),
            ("Rule-Based Triage", "Applies configurable operational thresholds (CPU 70/85, Mem 75/90, Disk 80/90)."),
            ("Interactive UI", "HTML5, CSS3, and ES6 JavaScript dashboard with 3-second auto-polling and dynamic DOM updates.")
        ], COLOR_SUCCESS_GREEN, COLOR_SUCCESS_BG, COLOR_SUCCESS_BORDER)
    ]

    card_w = 3.65
    card_h = 2.45
    x_base = 0.8
    y_base = 1.75
    x_gap = 0.38
    y_gap = 0.22

    for i, (title, items, border_c, bg_c, hborder_c) in enumerate(modules):
        col = i % 3
        row = i // 3
        x = x_base + col * (card_w + x_gap)
        y = y_base + row * (card_h + y_gap)

        card = create_card(slide, x, y, card_w, card_h)

        # Header pill
        hpill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.12), Inches(y + 0.12), Inches(card_w - 0.24), Inches(0.38))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = bg_c
        hpill.line.color.rgb = hborder_c
        hpill.line.width = Pt(1)
        tf_hp = hpill.text_frame
        tf_hp.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_hp = tf_hp.paragraphs[0]
        p_hp.text = title.upper()
        p_hp.font.name = FONT_HEADING
        p_hp.font.size = Pt(9.5)
        p_hp.font.bold = True
        p_hp.font.color.rgb = border_c
        p_hp.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.55), Inches(card_w - 0.3), Inches(card_h - 0.65))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0)
        tf.margin_top = Inches(0)

        for j, (lbl, txt) in enumerate(items):
            add_bullet_item(tf, lbl, txt, is_first=(j==0), font_size=9.2, bullet_color=border_c)

# ==============================================================================
# SLIDE 7: ARCHITECTURAL DIAGRAM
# ==============================================================================
def build_slide_07(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "07 | System Architecture", "CloudGuard End-to-End System Architecture", "Five-tier architectural hierarchy illustrating data ingestion, processing, detection, API, and UI")
    add_footer(slide, 7)

    tiers = [
        ("TIER 1: TELEMETRY & DATA SOURCES", [
            ("Live Host Telemetry", "psutil sampler (CPU %, Virtual Memory %, Disk Utilization)"),
            ("Benchmark Datasets", "Numenta Anomaly Benchmark (NAB): EC2 & RDS 14-Day Metrics (12,096 Records)")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("TIER 2: DATA PROCESSING & BIG DATA", [
            ("Schema Validation", "DataValidator (data_validator.py)"),
            ("Feature Normalization", "MinMaxScaler (models/scaler.joblib)"),
            ("Temporal Features", "1-Hr Rolling Window (feature_engineering.py)"),
            ("PySpark Aggregation", "Distributed Spark Engine (pyspark/server_aggregation.py)")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("TIER 3: ANOMALY DETECTION ENGINE", [
            ("Real-Time Operational Triage", "Configurable Rule Thresholds (CPU 70/85, Mem 75/90, Disk 80/90)"),
            ("Deep Offline ML Ensemble", "Isolation Forest (isolation_forest.joblib) + Local Outlier Factor (LOF)")
        ], COLOR_ALERT_RED, COLOR_ALERT_BG),

        ("TIER 4: BACKEND & REST API SERVICES", [
            ("WSGI Web Server", "Python Flask Application (website/api/app.py)"),
            ("REST Endpoints", "/api/metrics (JSON Telemetry & Status) | /api/health (System Health)")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("TIER 5: PRESENTATION & CONSUMPTION", [
            ("CloudGuard Web Dashboard", "HTML5 + Vanilla CSS3 + ES6 JavaScript (website/index.html)"),
            ("Auto-Refresh Loop", "Asynchronous fetch() every 3 seconds | Non-blocking dynamic DOM update"),
            ("Operator Alerting", "Live Status Badge (HEALTHY / WARNING / ANOMALY DETECTED) & Visual Alerts")
        ], COLOR_SUCCESS_GREEN, COLOR_SUCCESS_BG)
    ]

    tier_h = 0.88
    y_start = 1.70
    y_gap = 0.18
    t_w = 11.733

    for i, (tname, boxes, accent_c, bg_c) in enumerate(tiers):
        y = y_start + i * (tier_h + y_gap)

        # Outer tier card
        tcard = create_card(slide, 0.8, y, t_w, tier_h, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)

        # Left Tier Label
        tlbl = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.92), Inches(y + 0.12), Inches(2.5), Inches(tier_h - 0.24))
        tlbl.fill.solid()
        tlbl.fill.fore_color.rgb = bg_c
        tlbl.line.color.rgb = accent_c
        tlbl.line.width = Pt(1)
        tf_tl = tlbl.text_frame
        tf_tl.word_wrap = True
        tf_tl.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_tl = tf_tl.paragraphs[0]
        p_tl.text = tname
        p_tl.font.name = FONT_HEADING
        p_tl.font.size = Pt(9.5)
        p_tl.font.bold = True
        p_tl.font.color.rgb = accent_c
        p_tl.alignment = PP_ALIGN.CENTER

        # Inner Sub-Boxes
        num_boxes = len(boxes)
        avail_w = t_w - 2.85
        box_w = (avail_w - (num_boxes - 1) * 0.15) / num_boxes

        for k, (btitle, bdesc) in enumerate(boxes):
            bx = 3.55 + k * (box_w + 0.15)
            sbox = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(bx), Inches(y + 0.12), Inches(box_w), Inches(tier_h - 0.24))
            sbox.fill.solid()
            sbox.fill.fore_color.rgb = COLOR_CARD_BG
            sbox.line.color.rgb = COLOR_CARD_BORDER
            sbox.line.width = Pt(1)

            tf_sb = sbox.text_frame
            tf_sb.word_wrap = True
            tf_sb.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf_sb.margin_left = Inches(0.08)
            tf_sb.margin_right = Inches(0.08)

            p_b1 = tf_sb.paragraphs[0]
            p_b1.text = btitle
            p_b1.font.name = FONT_HEADING
            p_b1.font.size = Pt(9.5)
            p_b1.font.bold = True
            p_b1.font.color.rgb = COLOR_DARK_TEXT
            p_b1.alignment = PP_ALIGN.CENTER

            p_b2 = tf_sb.add_paragraph()
            p_b2.text = bdesc
            p_b2.font.name = FONT_BODY
            p_b2.font.size = Pt(8.0)
            p_b2.font.color.rgb = COLOR_GRAY_TEXT
            p_b2.alignment = PP_ALIGN.CENTER

        # Connector Down Arrow between tiers
        if i < len(tiers) - 1:
            arr_y = y + tier_h + 0.02
            arr = slide.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(6.55), Inches(arr_y), Inches(0.22), Inches(0.14))
            arr.fill.solid()
            arr.fill.fore_color.rgb = COLOR_BLUE_PRIMARY
            arr.line.fill.background()

print("Slide 6 and 7 defined")


import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# COLOR PALETTE & DESIGN TOKENS (Currex-inspired Tech / Navy Palette)
# ==============================================================================
COLOR_BG_LIGHT = RGBColor(248, 250, 252)       # Slate 50 (#F8FAFC)
COLOR_NAVY_DARK = RGBColor(15, 23, 42)          # Slate 900 (#0F172A)
COLOR_NAVY_CARD = RGBColor(30, 41, 59)          # Slate 800 (#1E293B)
COLOR_NAVY_BORDER = RGBColor(51, 65, 85)        # Slate 700 (#334155)

COLOR_BLUE_PRIMARY = RGBColor(2, 132, 199)      # Sky 600 (#0284C7)
COLOR_BLUE_ACCENT = RGBColor(56, 189, 248)      # Sky 400 (#38BDF8)
COLOR_BLUE_DARK = RGBColor(3, 105, 161)         # Sky 700 (#0369A1)
COLOR_BLUE_BG = RGBColor(240, 249, 255)         # Sky 50 (#F0F9FF)
COLOR_BLUE_BORDER = RGBColor(186, 230, 253)     # Sky 200 (#BAE6FD)

COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_DARK_TEXT = RGBColor(15, 23, 42)          # Slate 900
COLOR_GRAY_TEXT = RGBColor(100, 116, 139)       # Slate 500 (#64748B)
COLOR_LIGHT_TEXT = RGBColor(148, 163, 184)      # Slate 400 (#94A3B8)
COLOR_MUTED_TEXT = RGBColor(203, 213, 225)      # Slate 300 (#CBD5E1)

COLOR_CARD_BG = RGBColor(255, 255, 255)         # Card White
COLOR_CARD_BORDER = RGBColor(226, 232, 240)     # Slate 200 (#E2E8F0)

COLOR_ALERT_RED = RGBColor(239, 68, 68)         # Red 500 (#EF4444)
COLOR_ALERT_BG = RGBColor(254, 242, 242)        # Red 50 (#FEF2F2)
COLOR_ALERT_BORDER = RGBColor(254, 202, 202)    # Red 200 (#FECACA)

COLOR_SUCCESS_GREEN = RGBColor(16, 185, 129)    # Emerald 500 (#10B981)
COLOR_SUCCESS_BG = RGBColor(236, 253, 245)      # Emerald 50
COLOR_SUCCESS_BORDER = RGBColor(167, 243, 208)

COLOR_WARN_AMBER = RGBColor(245, 158, 11)       # Amber 500 (#F59E0B)
COLOR_WARN_BG = RGBColor(255, 251, 235)         # Amber 50
COLOR_WARN_BORDER = RGBColor(254, 243, 199)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"

PROJECT_DIR = Path(__file__).parent.resolve()
FIGURES_DIR = PROJECT_DIR / "results" / "figures"

def apply_slide_bg(slide, color=COLOR_BG_LIGHT):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, section_tag, title, subtitle):
    tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.38), Inches(2.3), Inches(0.32))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = COLOR_BLUE_BG
    tag_box.line.color.rgb = COLOR_BLUE_BORDER
    tag_box.line.width = Pt(1)
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = section_tag.upper()
    p_tag.font.name = FONT_HEADING
    p_tag.font.size = Pt(9.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_BLUE_PRIMARY
    p_tag.alignment = PP_ALIGN.CENTER

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.70), Inches(11.733), Inches(0.52))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = Inches(0)
    tf_title.margin_top = Inches(0)
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_DARK_TEXT

    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.22), Inches(11.733), Inches(0.32))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_left = Inches(0)
    tf_sub.margin_top = Inches(0)
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(11.5)
    p_sub.font.color.rgb = COLOR_GRAY_TEXT

def add_footer(slide, slide_num, total_slides=18):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.02), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_CARD_BORDER
    line.line.fill.background()

    foot_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(8.0), Inches(0.3))
    tf_left = foot_left.text_frame
    tf_left.margin_left = Inches(0)
    p_left = tf_left.paragraphs[0]
    p_left.text = "CloudGuard | Intelligent Cloud Server Anomaly Detection System — B.Tech Project Presentation"
    p_left.font.name = FONT_BODY
    p_left.font.size = Pt(9.5)
    p_left.font.color.rgb = COLOR_LIGHT_TEXT

    foot_right = slide.shapes.add_textbox(Inches(10.533), Inches(7.08), Inches(2.0), Inches(0.3))
    tf_right = foot_right.text_frame
    tf_right.margin_right = Inches(0)
    p_right = tf_right.paragraphs[0]
    p_right.text = f"{slide_num:02d} / {total_slides:02d}"
    p_right.font.name = FONT_BODY
    p_right.font.size = Pt(9.5)
    p_right.font.bold = True
    p_right.font.color.rgb = COLOR_GRAY_TEXT
    p_right.alignment = PP_ALIGN.RIGHT

def create_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER, border_width=1):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card

def add_bullet_item(tf, bold_label, text_body, is_first=False, font_size=10.0, bullet_color=COLOR_BLUE_PRIMARY):
    p = tf.paragraphs[0] if is_first else tf.add_paragraph()
    p.space_after = Pt(4)
    p.font.size = Pt(font_size)
    p.font.name = FONT_BODY

    run_bullet = p.add_run()
    run_bullet.text = "▪ "
    run_bullet.font.bold = True
    run_bullet.font.color.rgb = bullet_color

    run_title = p.add_run()
    run_title.text = bold_label + ": "
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_DARK_TEXT

    run_desc = p.add_run()
    run_desc.text = text_body
    run_desc.font.color.rgb = COLOR_GRAY_TEXT

# ==============================================================================
# SLIDE 8: SYSTEM REQUIREMENTS
# ==============================================================================
def build_slide_08(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "08 | System Requirements", "Hardware & Software Specifications", "Verified prerequisites and runtime dependencies for running the CloudGuard ecosystem")
    add_footer(slide, 8)

    col_w = 5.7
    card_h = 5.1
    y_pos = 1.72

    # Left: Hardware Requirements
    card_hw = create_card(slide, 0.8, y_pos, col_w, card_h)
    hpill_hw = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(y_pos + 0.2), Inches(col_w - 0.4), Inches(0.42))
    hpill_hw.fill.solid()
    hpill_hw.fill.fore_color.rgb = COLOR_BLUE_BG
    hpill_hw.line.color.rgb = COLOR_BLUE_BORDER
    hpill_hw.line.width = Pt(1)
    tf_hphw = hpill_hw.text_frame
    tf_hphw.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_hphw = tf_hphw.paragraphs[0]
    p_hphw.text = "HARDWARE SPECIFICATIONS"
    p_hphw.font.name = FONT_HEADING
    p_hphw.font.size = Pt(11)
    p_hphw.font.bold = True
    p_hphw.font.color.rgb = COLOR_BLUE_PRIMARY
    p_hphw.alignment = PP_ALIGN.CENTER

    tb_hw = slide.shapes.add_textbox(Inches(1.0), Inches(y_pos + 0.72), Inches(col_w - 0.4), Inches(card_h - 0.85))
    tf_hw = tb_hw.text_frame
    tf_hw.word_wrap = True

    hw_items = [
        ("Host System Architecture", "Standard PC, Laptop, or Cloud Virtual Machine (x86_64 architecture)."),
        ("Central Processing Unit (CPU)", "Multi-core processor (Intel Core i5 / AMD Ryzen 5 or equivalent; >= 4 cores recommended for Spark and ML training)."),
        ("System Memory (RAM)", "Minimum 8 GB RAM (16 GB recommended to support in-memory PySpark DataFrame aggregations and Jupyter analysis concurrently)."),
        ("Persistent Storage", "Minimum 10 GB free SSD storage to accommodate Python environment, NAB historical datasets, serialized model binaries, and generated reports."),
        ("Network Interface", "Standard loopback network adapter (127.0.0.1) for local Flask WSGI server and browser dashboard communication."),
        ("Display Resolution", "1920 x 1080 (Full HD) display recommended for viewing the responsive multi-card web monitoring dashboard.")
    ]
    for j, (lbl, txt) in enumerate(hw_items):
        add_bullet_item(tf_hw, lbl, txt, is_first=(j==0), font_size=9.6, bullet_color=COLOR_BLUE_PRIMARY)

    # Right: Software Requirements
    card_sw = create_card(slide, 6.833, y_pos, col_w, card_h)
    hpill_sw = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.033), Inches(y_pos + 0.2), Inches(col_w - 0.4), Inches(0.42))
    hpill_sw.fill.solid()
    hpill_sw.fill.fore_color.rgb = COLOR_SUCCESS_BG
    hpill_sw.line.color.rgb = COLOR_SUCCESS_BORDER
    hpill_sw.line.width = Pt(1)
    tf_hpsw = hpill_sw.text_frame
    tf_hpsw.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_hpsw = tf_hpsw.paragraphs[0]
    p_hpsw.text = "VERIFIED SOFTWARE ENVIRONMENT"
    p_hpsw.font.name = FONT_HEADING
    p_hpsw.font.size = Pt(11)
    p_hpsw.font.bold = True
    p_hpsw.font.color.rgb = COLOR_SUCCESS_GREEN
    p_hpsw.alignment = PP_ALIGN.CENTER

    tb_sw = slide.shapes.add_textbox(Inches(7.033), Inches(y_pos + 0.72), Inches(col_w - 0.4), Inches(card_h - 0.85))
    tf_sw = tb_sw.text_frame
    tf_sw.word_wrap = True

    sw_items = [
        ("Operating System", "Microsoft Windows 10/11 (64-bit), Ubuntu Linux (20.04+), or macOS."),
        ("Python Runtime", "Python 3.11.x (Anaconda 'cloud_anomaly' environment or standard virtualenv)."),
        ("Web Framework & Telemetry", "Flask >= 3.0.0 (WSGI microframework) and psutil >= 5.9.0 (system resource telemetry gathering)."),
        ("Scientific Computing & ML", "pandas >= 2.0.0, numpy >= 1.24.0, scikit-learn >= 1.2.0, scipy >= 1.10.0, joblib >= 1.2.0."),
        ("Big Data & JVM Runtime", "PySpark >= 3.4.0 with Java JDK 11 (AdoptOpenJDK runtime configured in JAVA_HOME)."),
        ("Frontend & Client", "HTML5, CSS3, modern Vanilla JavaScript (ES6+), and any modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox)."),
        ("Database Technology", "MySQL via XAMPP (relational database schema designed for production telemetry persistence)."),
        ("Development IDE", "Visual Studio Code and Jupyter Notebook (ipykernel >= 6.20.0).")
    ]
    for j, (lbl, txt) in enumerate(sw_items):
        add_bullet_item(tf_sw, lbl, txt, is_first=(j==0), font_size=9.4, bullet_color=COLOR_SUCCESS_GREEN)

# ==============================================================================
# SLIDE 9: IMPLEMENTATION & TECHNOLOGIES
# ==============================================================================
def build_slide_09(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "09 | Implementation & Tech Stack", "Technology Stack & Architectural Roles", "Detailed breakdown of the languages, frameworks, and libraries utilized across CloudGuard")
    add_footer(slide, 9)

    tech_categories = [
        ("DATA & BIG DATA PROCESSING", [
            ("Python 3.11+", "Core programming language orchestrating data pipelines, feature engineering, and inference."),
            ("Pandas", "High-performance tabular metric manipulation, temporal alignment, and rolling calculations."),
            ("NumPy", "Efficient multi-dimensional array operations and vectorized mathematical computations."),
            ("PySpark 3.4+", "Distributed DataFrame engine executing server-level summary aggregations across historical records.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("MACHINE LEARNING FRAMEWORK", [
            ("Scikit-learn", "Implements Isolation Forest (tree isolation) and Local Outlier Factor (local density outlier detection)."),
            ("Joblib", "Serializes trained model binaries (isolation_forest.joblib) and MinMaxScaler states (scaler.joblib).")
        ], COLOR_ALERT_RED, COLOR_ALERT_BG),

        ("BACKEND & REST API", [
            ("Flask 3.0+", "Lightweight WSGI web microframework exposing RESTful endpoints (/api/metrics, /api/health)."),
            ("psutil 5.9+", "Cross-platform library gathering real-time OS CPU utilization, virtual memory, and disk usage.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("FRONTEND & VISUALIZATION", [
            ("HTML5 & CSS3", "Semantic structure and custom dark-themed UI with status cards and animated progress bars."),
            ("JavaScript (ES6)", "Asynchronous non-blocking API polling (fetch) and dynamic DOM updates every 3 seconds."),
            ("Matplotlib & Seaborn", "Generates publication-quality EDA figures, correlation heatmaps, and distribution plots.")
        ], COLOR_SUCCESS_GREEN, COLOR_SUCCESS_BG),

        ("DEVELOPMENT & PERSISTENCE", [
            ("Jupyter Notebook", "Phased notebooks (01_data_exploration, 02_preprocessing, 03_anomaly_detection)."),
            ("VS Code", "Primary code authoring, linting, debugging, and terminal execution environment."),
            ("MySQL (via XAMPP)", "Relational database schema designed for production telemetry persistence (schema.sql).")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG)
    ]

    card_w = 5.7
    card_h = 2.45
    top_y = 1.72
    bot_y = 4.35

    coords = [
        (0.8, top_y, card_w, card_h),
        (6.833, top_y, card_w, card_h),
        (0.8, bot_y, 3.65, card_h),
        (4.833, bot_y, 3.65, card_h),
        (8.866, bot_y, 3.65, card_h)
    ]

    for i, (cat_title, items, border_c, bg_c) in enumerate(tech_categories):
        x, y, w, h = coords[i]
        card = create_card(slide, x, y, w, h)

        hpill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.12), Inches(y + 0.12), Inches(w - 0.24), Inches(0.38))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = bg_c
        hpill.line.color.rgb = border_c
        hpill.line.width = Pt(1)
        tf_hp = hpill.text_frame
        tf_hp.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_hp = tf_hp.paragraphs[0]
        p_hp.text = cat_title
        p_hp.font.name = FONT_HEADING
        p_hp.font.size = Pt(9.5)
        p_hp.font.bold = True
        p_hp.font.color.rgb = border_c
        p_hp.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.55), Inches(w - 0.3), Inches(h - 0.65))
        tf = tb.text_frame
        tf.word_wrap = True

        for j, (lbl, txt) in enumerate(items):
            add_bullet_item(tf, lbl, txt, is_first=(j==0), font_size=9.2, bullet_color=border_c)

print("Slide 8 and 9 defined")


import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# SLIDE 10: WEB DASHBOARD
# ==============================================================================
def build_slide_10(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "10 | Web Dashboard", "CloudGuard Interface & Live Interaction Flow", "Real-time monitoring dashboard structure and asynchronous client-server communication mechanism")
    add_footer(slide, 10)

    # Left Side: UI Anatomy (4 Cards in a 2x2 grid)
    ui_cards = [
        ("1. Sidebar Navigation", [
            ("Core Navigation", "Quick routing between Dashboard, Server Metrics, Anomalies, Analytics, and Settings."),
            ("System Status Dot", "Displays live operational connectivity state ('System Online').")
        ]),
        ("2. Live Metric Gauges", [
            ("Multi-Resource Tracking", "Dedicated metric cards for CPU Usage, Memory, and Disk Usage."),
            ("Progress Bars", "Dynamic animated progress fills providing immediate visual percentage feedback.")
        ]),
        ("3. System Status Card", [
            ("Three-State Indicator", "Prominently displays HEALTHY, WARNING, or ANOMALY DETECTED."),
            ("Live Heartbeat", "Displays real-time timestamp of last telemetry ingestion and status message.")
        ]),
        ("4. Anomaly Alert Panel", [
            ("Contextual Icon", "Shield icon transitions from 🛡️ (Safe) to ⚠️ (Warning) or 🚨 (Anomaly)."),
            ("Diagnostic Guidance", "Informs the operator immediately when any metric breaches critical bounds.")
        ])
    ]

    col_w = 2.85
    card_h = 2.45
    x_base = 0.8
    y_base = 1.72
    gap = 0.15

    for i, (title, items) in enumerate(ui_cards):
        col = i % 2
        row = i // 2
        x = x_base + col * (col_w + gap)
        y = y_base + row * (card_h + gap)

        card = create_card(slide, x, y, col_w, card_h)
        hpill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.1), Inches(y + 0.1), Inches(col_w - 0.2), Inches(0.35))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = COLOR_BLUE_BG
        hpill.line.color.rgb = COLOR_BLUE_BORDER
        hpill.line.width = Pt(1)
        tf_hp = hpill.text_frame
        tf_hp.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_hp = tf_hp.paragraphs[0]
        p_hp.text = title.upper()
        p_hp.font.name = FONT_HEADING
        p_hp.font.size = Pt(9.0)
        p_hp.font.bold = True
        p_hp.font.color.rgb = COLOR_BLUE_PRIMARY
        p_hp.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x + 0.12), Inches(y + 0.50), Inches(col_w - 0.24), Inches(card_h - 0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        for j, (lbl, txt) in enumerate(items):
            add_bullet_item(tf, lbl, txt, is_first=(j==0), font_size=8.8)

    # Right Side: Client-Server Polling Flow Card
    flow_x = 6.833
    flow_w = 5.7
    flow_h = 5.05
    card_flow = create_card(slide, flow_x, y_base, flow_w, flow_h)

    hpill_flow = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(flow_x + 0.2), Inches(y_base + 0.15), Inches(flow_w - 0.4), Inches(0.42))
    hpill_flow.fill.solid()
    hpill_flow.fill.fore_color.rgb = COLOR_SUCCESS_BG
    hpill_flow.line.color.rgb = COLOR_SUCCESS_BORDER
    hpill_flow.line.width = Pt(1)
    tf_hpf = hpill_flow.text_frame
    tf_hpf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_hpf = tf_hpf.paragraphs[0]
    p_hpf.text = "CLIENT-SERVER ASYNCHRONOUS POLLING LIFECYCLE"
    p_hpf.font.name = FONT_HEADING
    p_hpf.font.size = Pt(10.5)
    p_hpf.font.bold = True
    p_hpf.font.color.rgb = COLOR_SUCCESS_GREEN
    p_hpf.alignment = PP_ALIGN.CENTER

    tb_flow = slide.shapes.add_textbox(Inches(flow_x + 0.2), Inches(y_base + 0.68), Inches(flow_w - 0.4), Inches(flow_h - 0.8))
    tf_flow = tb_flow.text_frame
    tf_flow.word_wrap = True

    flow_steps = [
        ("1. Scheduled Client Poll", "JavaScript frontend (assets/js/script.js) executes loadMetrics() immediately on page load, followed by setInterval() every 3,000 milliseconds (3 seconds)."),
        ("2. Asynchronous API Fetch", "Browser initiates an asynchronous non-blocking HTTP GET request: fetch('/api/metrics') without triggering full page reloads."),
        ("3. Host Resource Sampling", "Flask application (website/api/app.py) handles the request and invokes psutil.cpu_percent(interval=1), psutil.virtual_memory(), and psutil.disk_usage('/')."),
        ("4. Rule-Based Evaluation", "Backend executes evaluate_metric() for each resource against configured limits: Warning (70% CPU, 75% RAM, 80% Disk); Anomaly (85% CPU, 90% RAM, 90% Disk)."),
        ("5. Overall Status Synthesis", "Synthesizes overall_status ('anomaly' if any metric exceeds anomaly limit, 'warning' if any exceeds warning limit, else 'normal')."),
        ("6. JSON Response Delivery", "Flask serializes and returns structured JSON payload containing raw usage values, byte totals, individual statuses, and timestamp."),
        ("7. Dynamic DOM Rendering", "Frontend parses JSON, updates card numbers, modifies progress bar widths, and dynamically updates CSS color classes (status-normal, status-warning, status-danger).")
    ]
    for j, (lbl, txt) in enumerate(flow_steps):
        add_bullet_item(tf_flow, lbl, txt, is_first=(j==0), font_size=9.0, bullet_color=COLOR_SUCCESS_GREEN)

# ==============================================================================
# SLIDE 11: WORKING / DATA FLOW
# ==============================================================================
def build_slide_11(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "11 | System Working", "Working & Data Flow: End-to-End Operational Lifecycle", "Nine-step chronological progression from server telemetry emission to operator alerting")
    add_footer(slide, 11)

    stages = [
        ("STAGE 1: INGESTION & PREPARATION", [
            ("Step 1: Telemetry Capture", "Live host metrics gathered via psutil or historical NAB telemetry streams ingested via data_loader.py."),
            ("Step 2: Schema Validation", "data_validator.py checks columns, formats timestamps, verifies data types, and checks for missing values."),
            ("Step 3: MinMax Normalization", "data_processor.py scales metric features to [0, 1] range using fitted MinMaxScaler (models/scaler.joblib).")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG, COLOR_BLUE_BORDER),

        ("STAGE 2: FEATURE ENGINEERING & ML", [
            ("Step 4: 1-Hour Rolling Lookback", "feature_engineering.py groups by server_id and computes 12-step moving averages and rolling standard deviations."),
            ("Step 5: Dual-Model ML Scoring", "Normalized feature vectors are passed through Isolation Forest (isolation_forest.joblib) and Local Outlier Factor."),
            ("Step 6: Ensemble Consensus", "Classifies records into NORMAL (both agree), POSSIBLE_ANOMALY (one flags), or HIGH_CONFIDENCE_ANOMALY (both agree).")
        ], COLOR_ALERT_RED, COLOR_ALERT_BG, COLOR_ALERT_BORDER),

        ("STAGE 3: SERVING & VISUALIZATION", [
            ("Step 7: Real-Time Evaluation", "Flask backend applies evaluate_metric() against configured warning and anomaly thresholds for zero-latency triage."),
            ("Step 8: REST API Exposure", "website/api/app.py delivers JSON telemetry over /api/metrics and system diagnostics over /api/health."),
            ("Step 9: Dynamic UI Rendering", "JavaScript dashboard polls every 3s, updating live gauges, status shields, and progress bars without page reloads.")
        ], COLOR_SUCCESS_GREEN, COLOR_SUCCESS_BG, COLOR_SUCCESS_BORDER)
    ]

    col_w = 3.65
    card_h = 5.05
    x_base = 0.8
    y_pos = 1.72
    gap = 0.38

    for i, (stitle, ssteps, border_c, bg_c, hborder_c) in enumerate(stages):
        x = x_base + i * (col_w + gap)
        card = create_card(slide, x, y_pos, col_w, card_h)

        hpill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.15), Inches(y_pos + 0.15), Inches(col_w - 0.3), Inches(0.42))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = bg_c
        hpill.line.color.rgb = hborder_c
        hpill.line.width = Pt(1)
        tf_hp = hpill.text_frame
        tf_hp.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_hp = tf_hp.paragraphs[0]
        p_hp.text = stitle
        p_hp.font.name = FONT_HEADING
        p_hp.font.size = Pt(10)
        p_hp.font.bold = True
        p_hp.font.color.rgb = border_c
        p_hp.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y_pos + 0.70), Inches(col_w - 0.3), Inches(card_h - 0.8))
        tf = tb.text_frame
        tf.word_wrap = True

        for j, (lbl, txt) in enumerate(ssteps):
            add_bullet_item(tf, lbl, txt, is_first=(j==0), font_size=9.5, bullet_color=border_c)

print("Slide 10 and 11 defined")


import os
import sys
import shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# SLIDE 12: RESULTS
# ==============================================================================
def build_slide_12(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "12 | Results", "Experimental Results: Dataset & Server Performance Analytics", "Empirical evaluation on 12,096 observations from the Numenta Anomaly Benchmark (NAB)")
    add_footer(slide, 12)

    # Left Side: 3 Server Result Cards (5.5" wide)
    server_results = [
        ("SERVER-01: Baseline Production EC2 Instance", [
            ("Total Records Evaluated", "4,032 observations (14-day continuous window @ 5-min intervals)."),
            ("Normal Observations", "4,018 records (99.65% normal operation)."),
            ("Anomalies Flagged", "14 records (0.35% anomaly frequency)."),
            ("Behavioral Profile", "Highly stable production server; rare transient anomalies correspond to sudden disk write bursts.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("SERVER-02: High-Load Stress EC2 Instance", [
            ("Total Records Evaluated", "4,032 observations (14-day continuous window @ 5-min intervals)."),
            ("Normal Observations", "3,521 records (87.33% normal operation)."),
            ("Anomalies Flagged", "511 records (12.67% anomaly frequency)."),
            ("Behavioral Profile", "Volatile workload experiencing repeated severe CPU utilization saturation (approaching 100%) and network traffic spikes.")
        ], COLOR_ALERT_RED, COLOR_ALERT_BG),

        ("SERVER-03: Relational Database Instance (RDS)", [
            ("Total Records Evaluated", "4,032 observations (14-day continuous window @ 5-min intervals)."),
            ("Normal Observations", "3,952 records (98.02% normal operation)."),
            ("Anomalies Flagged", "80 records (1.98% anomaly frequency)."),
            ("Behavioral Profile", "Moderate database workload; anomalies correlate with batch query execution spikes and elevated memory latency.")
        ], COLOR_SUCCESS_GREEN, COLOR_SUCCESS_BG)
    ]

    card_w = 5.5
    card_h = 1.55
    x_left = 0.8
    y_base = 1.72
    y_gap = 0.16

    for i, (stitle, items, border_c, bg_c) in enumerate(server_results):
        y = y_base + i * (card_h + y_gap)
        card = create_card(slide, x_left, y, card_w, card_h)

        hpill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x_left + 0.1), Inches(y + 0.1), Inches(card_w - 0.2), Inches(0.32))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = bg_c
        hpill.line.color.rgb = border_c
        hpill.line.width = Pt(1)
        tf_hp = hpill.text_frame
        tf_hp.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_hp = tf_hp.paragraphs[0]
        p_hp.text = stitle.upper()
        p_hp.font.name = FONT_HEADING
        p_hp.font.size = Pt(8.8)
        p_hp.font.bold = True
        p_hp.font.color.rgb = border_c
        p_hp.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x_left + 0.12), Inches(y + 0.45), Inches(card_w - 0.24), Inches(card_h - 0.50))
        tf = tb.text_frame
        tf.word_wrap = True

        for j, (lbl, txt) in enumerate(items):
            add_bullet_item(tf, lbl, txt, is_first=(j==0), font_size=8.5, bullet_color=border_c)

    # Right Side: Embedded Real Project Figure
    right_x = 6.6
    right_w = 5.933
    right_h = 5.0
    fig_path = FIGURES_DIR / "server_comparison.png"

    card_fig = create_card(slide, right_x, y_base, right_w, right_h)

    # Title over chart
    ch_pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(right_x + 0.2), Inches(y_base + 0.15), Inches(right_w - 0.4), Inches(0.38))
    ch_pill.fill.solid()
    ch_pill.fill.fore_color.rgb = COLOR_BLUE_BG
    ch_pill.line.color.rgb = COLOR_BLUE_BORDER
    ch_pill.line.width = Pt(1)
    tf_cp = ch_pill.text_frame
    tf_cp.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_cp = tf_cp.paragraphs[0]
    p_cp.text = "EMPIRICAL SERVER METRIC COMPARISON (GENERATED EDA)"
    p_cp.font.name = FONT_HEADING
    p_cp.font.size = Pt(10)
    p_cp.font.bold = True
    p_cp.font.color.rgb = COLOR_BLUE_PRIMARY
    p_cp.alignment = PP_ALIGN.CENTER

    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(right_x + 0.2), Inches(y_base + 0.60), width=Inches(right_w - 0.4), height=Inches(right_h - 0.75))
    else:
        # Fallback if image not found
        tb_nofig = slide.shapes.add_textbox(Inches(right_x + 0.3), Inches(y_base + 1.5), Inches(right_w - 0.6), Inches(2.0))
        tf_nf = tb_nofig.text_frame
        p_nf = tf_nf.paragraphs[0]
        p_nf.text = "Visual analytics generated by python/eda_generator.py saved in results/figures/server_comparison.png"
        p_nf.font.name = FONT_BODY
        p_nf.font.size = Pt(11)

# ==============================================================================
# SLIDE 13: ANOMALY DETECTION RESULT
# ==============================================================================
def build_slide_13(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "13 | Results", "Anomaly Detection Analysis: ML Ensemble & Threshold Rules", "Quantitative breakdown of Isolation Forest, Local Outlier Factor, and real-time rule evaluations")
    add_footer(slide, 13)

    # Top: Machine Learning Severity Breakdown Card
    top_w = 11.733
    top_h = 2.15
    y_top = 1.72
    card_top = create_card(slide, 0.8, y_top, top_w, top_h)

    hpill_top = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(y_top + 0.15), Inches(top_w - 0.4), Inches(0.38))
    hpill_top.fill.solid()
    hpill_top.fill.fore_color.rgb = COLOR_BLUE_BG
    hpill_top.line.color.rgb = COLOR_BLUE_BORDER
    hpill_top.line.width = Pt(1)
    tf_hpt = hpill_top.text_frame
    tf_hpt.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_hpt = tf_hpt.paragraphs[0]
    p_hpt.text = "OFFLINE MACHINE LEARNING ENSEMBLE SEVERITY BREAKDOWN (12,096 TOTAL RECORDS)"
    p_hpt.font.name = FONT_HEADING
    p_hpt.font.size = Pt(10)
    p_hpt.font.bold = True
    p_hpt.font.color.rgb = COLOR_BLUE_PRIMARY
    p_hpt.alignment = PP_ALIGN.CENTER

    tb_top = slide.shapes.add_textbox(Inches(1.0), Inches(y_top + 0.58), Inches(top_w - 0.4), Inches(top_h - 0.65))
    tf_top = tb_top.text_frame
    tf_top.word_wrap = True

    sev_items = [
        ("NORMAL (Both Models Normal)", "10,972 records (90.71%) — High-confidence normal baseline where Isolation Forest and Local Outlier Factor agree."),
        ("POSSIBLE_ANOMALY (Single Model Flag)", "1,038 records (8.58%) — Observations flagged as anomalous by either Isolation Forest or LOF individually, representing borderline outliers or algorithm-specific sensitivities."),
        ("HIGH_CONFIDENCE_ANOMALY (Mutual Consensus)", "86 records (0.71%) — Multi-dimensional anomalies flagged simultaneously by both Isolation Forest and Local Outlier Factor, representing critical system disturbances requiring immediate operator attention.")
    ]
    for j, (lbl, txt) in enumerate(sev_items):
        bc = COLOR_SUCCESS_GREEN if j==0 else (COLOR_WARN_AMBER if j==1 else COLOR_ALERT_RED)
        add_bullet_item(tf_top, lbl, txt, is_first=(j==0), font_size=9.5, bullet_color=bc)

    # Bottom Left: Model Crosstab Comparison Card
    bot_y = 4.02
    bot_h = 2.80
    bot_w = 5.7
    card_bl = create_card(slide, 0.8, bot_y, bot_w, bot_h)

    hpill_bl = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(bot_y + 0.15), Inches(bot_w - 0.4), Inches(0.38))
    hpill_bl.fill.solid()
    hpill_bl.fill.fore_color.rgb = COLOR_ALERT_BG
    hpill_bl.line.color.rgb = COLOR_ALERT_BORDER
    hpill_bl.line.width = Pt(1)
    tf_hpbl = hpill_bl.text_frame
    tf_hpbl.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_hpbl = tf_hpbl.paragraphs[0]
    p_hpbl.text = "CROSS-MODEL AGREEMENT MATRIX (ISOLATION FOREST vs LOF)"
    p_hpbl.font.name = FONT_HEADING
    p_hpbl.font.size = Pt(9.5)
    p_hpbl.font.bold = True
    p_hpbl.font.color.rgb = COLOR_ALERT_RED
    p_hpbl.alignment = PP_ALIGN.CENTER

    tb_bl = slide.shapes.add_textbox(Inches(1.0), Inches(bot_y + 0.58), Inches(bot_w - 0.4), Inches(bot_h - 0.65))
    tf_bl = tb_bl.text_frame
    tf_bl.word_wrap = True

    crosstab_items = [
        ("Mutual Anomalies (Both Flagged)", "86 records — Tree-based isolation and density-based clustering agree on severe multi-dimensional deviation."),
        ("Isolation Forest Exclusive Anomalies", "519 records — Outliers identified via random recursive partitioning across high-dimensional feature bounds."),
        ("Local Outlier Factor Exclusive Anomalies", "519 records — Outliers identified by measuring local density deviation relative to k=20 nearest neighbors."),
        ("Mutual Normal Observations", "10,972 records — Consistent baseline validation across both independent paradigms.")
    ]
    for j, (lbl, txt) in enumerate(crosstab_items):
        add_bullet_item(tf_bl, lbl, txt, is_first=(j==0), font_size=9.2, bullet_color=COLOR_ALERT_RED)

    # Bottom Right: Real-Time Operational Threshold Rules Card
    card_br = create_card(slide, 6.833, bot_y, bot_w, bot_h)

    hpill_br = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.033), Inches(bot_y + 0.15), Inches(bot_w - 0.4), Inches(0.38))
    hpill_br.fill.solid()
    hpill_br.fill.fore_color.rgb = COLOR_SUCCESS_BG
    hpill_br.line.color.rgb = COLOR_SUCCESS_BORDER
    hpill_br.line.width = Pt(1)
    tf_hpbr = hpill_br.text_frame
    tf_hpbr.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_hpbr = tf_hpbr.paragraphs[0]
    p_hpbr.text = "REAL-TIME DASHBOARD THRESHOLD LOGIC (FLASK API)"
    p_hpbr.font.name = FONT_HEADING
    p_hpbr.font.size = Pt(9.5)
    p_hpbr.font.bold = True
    p_hpbr.font.color.rgb = COLOR_SUCCESS_GREEN
    p_hpbr.alignment = PP_ALIGN.CENTER

    tb_br = slide.shapes.add_textbox(Inches(7.033), Inches(bot_y + 0.58), Inches(bot_w - 0.4), Inches(bot_h - 0.65))
    tf_br = tb_br.text_frame
    tf_br.word_wrap = True

    thresh_items = [
        ("CPU Utilization Thresholds", "Warning at >= 70% | Critical Anomaly at >= 85% utilization."),
        ("Virtual Memory Thresholds", "Warning at >= 75% | Critical Anomaly at >= 90% utilization."),
        ("Disk Storage Thresholds", "Warning at >= 80% | Critical Anomaly at >= 90% utilization."),
        ("Status Priority Synthesis", "If any resource is 'anomaly' -> overall is 'anomaly'; else if any is 'warning' -> overall is 'warning'; else 'normal'."),
        ("Architectural Transparency", "Provides immediate, explainable heuristics for live monitoring, completely distinct from the deep offline ML pipeline.")
    ]
    for j, (lbl, txt) in enumerate(thresh_items):
        add_bullet_item(tf_br, lbl, txt, is_first=(j==0), font_size=9.2, bullet_color=COLOR_SUCCESS_GREEN)

# ==============================================================================
# SLIDE 14: DASHBOARD FEATURES
# ==============================================================================
def build_slide_14(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "14 | Features", "CloudGuard Dashboard Capabilities & Operational Strengths", "Architectural advantages and interactive monitoring capabilities implemented in the system")
    add_footer(slide, 14)

    features = [
        ("1. Real-Time OS Telemetry", [
            ("Live Ingestion", "Harvests active host processor, RAM, and disk storage metrics instantly using psutil."),
            ("Low Overhead", "Negligible system footprint ensures monitoring does not degrade server performance.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("2. Multi-Tier Status Triage", [
            ("Tri-State Indicators", "Prominently displays HEALTHY, WARNING, or ANOMALY DETECTED with dynamic styling."),
            ("Contextual Alerts", "Shield icon and message change instantly to inform operators of system state.")
        ], COLOR_ALERT_RED, COLOR_ALERT_BG),

        ("3. Configurable Operational Thresholds", [
            ("Auditable Boundaries", "Rules defined in website/api/app.py can be adjusted to match custom workload SLAs."),
            ("Transparent Logic", "Eliminates black-box confusion during live operational triage.")
        ], COLOR_SUCCESS_GREEN, COLOR_SUCCESS_BG),

        ("4. Non-Blocking Asynchronous Polling", [
            ("3-Second Auto Refresh", "JavaScript fetch() polls backend asynchronously every 3 seconds."),
            ("Seamless Updates", "DOM elements, percentages, and progress bars update without page reloads.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("5. Decoupled RESTful Architecture", [
            ("Microservice Design", "Flask backend and HTML/JS frontend are strictly decoupled via REST endpoints."),
            ("Interoperable JSON", "Enables external tools, CLI scripts, or mobile dashboards to consume /api/metrics.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("6. Modular Machine Learning Extensibility", [
            ("Standardized Interface", "evaluate_metric() contract allows drop-in deployment of isolation_forest.joblib."),
            ("Future Ready", "Ready for online inference integration without altering frontend client code.")
        ], COLOR_SUCCESS_GREEN, COLOR_SUCCESS_BG)
    ]

    card_w = 3.65
    card_h = 2.45
    x_base = 0.8
    y_base = 1.72
    x_gap = 0.38
    y_gap = 0.22

    for i, (title, items, border_c, bg_c) in enumerate(features):
        col = i % 3
        row = i // 3
        x = x_base + col * (card_w + x_gap)
        y = y_base + row * (card_h + y_gap)

        card = create_card(slide, x, y, card_w, card_h)

        hpill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.12), Inches(y + 0.12), Inches(card_w - 0.24), Inches(0.38))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = bg_c
        hpill.line.color.rgb = border_c
        hpill.line.width = Pt(1)
        tf_hp = hpill.text_frame
        tf_hp.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_hp = tf_hp.paragraphs[0]
        p_hp.text = title.upper()
        p_hp.font.name = FONT_HEADING
        p_hp.font.size = Pt(9.5)
        p_hp.font.bold = True
        p_hp.font.color.rgb = border_c
        p_hp.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.55), Inches(card_w - 0.3), Inches(card_h - 0.65))
        tf = tb.text_frame
        tf.word_wrap = True

        for j, (lbl, txt) in enumerate(items):
            add_bullet_item(tf, lbl, txt, is_first=(j==0), font_size=9.2, bullet_color=border_c)

# ==============================================================================
# SLIDE 15: CONCLUSION
# ==============================================================================
def build_slide_15(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "15 | Conclusion", "Project Summary & Academic Contributions", "Synthesis of achievements in cloud server monitoring and multi-model anomaly detection")
    add_footer(slide, 15)

    conclusions = [
        ("Centralized Observability Platform", [
            ("Cohesive Solution", "Successfully designed and deployed CloudGuard, a centralized monitoring and anomaly detection platform for cloud servers."),
            ("Single-Pane-of-Glass", "Unified real-time host metric visualization, status badges, and diagnostic guidance into a clean, modern interface."),
            ("Zero-Overhead Triage", "Ensured non-blocking telemetry acquisition that provides immediate visibility without burdening server resources.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("Dual-Engine Anomaly Detection Methodology", [
            ("Balanced Design", "Demonstrated the practical value of separating operational real-time heuristics from deep offline machine learning."),
            ("Transparent Baseline", "Real-time rule-based thresholds provide explainable, immediate alerts for live production triage."),
            ("Multivariate ML Rigour", "Offline ensemble modeling (Isolation Forest + LOF) accurately isolates subtle multi-dimensional outliers across 12,096 benchmark records.")
        ], COLOR_ALERT_RED, COLOR_ALERT_BG),

        ("Scalable Big Data & Feature Pipeline", [
            ("Distributed Analytics", "Integrated PySpark for server-level statistical aggregations, establishing enterprise Big Data scalability."),
            ("Temporal Feature Engineering", "Engineered 1-hour rolling lookback features (moving averages, volatility, rate-of-change) to capture workload shifts."),
            ("Model Serialization", "Preserved fitted MinMaxScaler and Isolation Forest binaries via Joblib for repeatable, consistent inference.")
        ], COLOR_SUCCESS_GREEN, COLOR_SUCCESS_BG),

        ("Academic Transparency & Extensibility", [
            ("Ground Truth Fidelity", "Evaluated against authentic public cloud benchmarks (Numenta Anomaly Benchmark AWS CloudWatch subset)."),
            ("No Fabricated Metrics", "Strictly distinguished between live heuristic triage and offline ML evaluation without manufactured claims."),
            ("Extensible Architecture", "Modular REST API and codebase structure allows straightforward integration of remote agent fleets and cloud APIs.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG)
    ]

    card_w = 5.7
    card_h = 2.45
    top_y = 1.72
    bot_y = 4.35

    coords = [
        (0.8, top_y), (6.833, top_y),
        (0.8, bot_y), (6.833, bot_y)
    ]

    for i, (title, items, border_c, bg_c) in enumerate(conclusions):
        x, y = coords[i]
        card = create_card(slide, x, y, card_w, card_h)

        hpill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.15), Inches(y + 0.15), Inches(card_w - 0.3), Inches(0.40))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = bg_c
        hpill.line.color.rgb = border_c
        hpill.line.width = Pt(1)
        tf_hp = hpill.text_frame
        tf_hp.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_hp = tf_hp.paragraphs[0]
        p_hp.text = title.upper()
        p_hp.font.name = FONT_HEADING
        p_hp.font.size = Pt(10)
        p_hp.font.bold = True
        p_hp.font.color.rgb = border_c
        p_hp.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x + 0.18), Inches(y + 0.60), Inches(card_w - 0.36), Inches(card_h - 0.70))
        tf = tb.text_frame
        tf.word_wrap = True

        for j, (lbl, txt) in enumerate(items):
            add_bullet_item(tf, lbl, txt, is_first=(j==0), font_size=9.4, bullet_color=border_c)

# ==============================================================================
# SLIDE 16: FUTURE SCOPE
# ==============================================================================
def build_slide_16(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "16 | Future Scope", "Planned Enhancements & Production Roadmap", "Clearly designated future capabilities for extending CloudGuard into enterprise cloud environments")
    add_footer(slide, 16)

    roadmap = [
        ("1. Remote Multi-Server Agent Fleet", [
            ("Cross-Platform Daemons", "Develop lightweight Go or Rust daemon agents installed across remote cloud instances."),
            ("Secure Transport", "Stream metrics over secure gRPC or HTTPS with TLS encryption to a central aggregator.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("2. Native Cloud Provider Connectors", [
            ("AWS / Azure / GCP APIs", "Integrate native APIs (AWS CloudWatch, Azure Monitor, GCP Cloud Operations)."),
            ("Multi-Cloud Federation", "Aggregate metrics across heterogeneous multi-cloud environments in a single view.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("3. Streaming ML Inference Engine", [
            ("Real-Time ML Scoring", "Embed pre-trained models (isolation_forest.joblib) directly into online streaming pipelines."),
            ("Kafka / Spark Streaming", "Score incoming telemetry events within milliseconds using sliding window state.")
        ], COLOR_ALERT_RED, COLOR_ALERT_BG),

        ("4. Automated Alert Dispatcher", [
            ("Multi-Channel Notifications", "Dispatch critical incident alerts via Email (SMTP), SMS, Slack webhooks, and Telegram bots."),
            ("Escalation Policies", "Implement severity-based alert throttling and on-call escalation schedules.")
        ], COLOR_SUCCESS_GREEN, COLOR_SUCCESS_BG),

        ("5. Production Database Persistence", [
            ("MySQL Schema Deployment", "Deploy designed relational schema (database/schema.sql) with automated indexing."),
            ("Time-Series Partitioning", "Partition tables by calendar month and implement automated cold-storage archiving.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG),

        ("6. Container & Kubernetes Monitoring", [
            ("Container Observability", "Collect telemetry at the Docker container and Kubernetes Pod/Node abstraction layer."),
            ("Cluster Health Scoring", "Detect node starvation, pod crash loops, and resource quota saturation.")
        ], COLOR_BLUE_PRIMARY, COLOR_BLUE_BG)
    ]

    card_w = 3.65
    card_h = 2.45
    x_base = 0.8
    y_base = 1.72
    x_gap = 0.38
    y_gap = 0.22

    for i, (title, items, border_c, bg_c) in enumerate(roadmap):
        col = i % 3
        row = i // 3
        x = x_base + col * (card_w + x_gap)
        y = y_base + row * (card_h + y_gap)

        card = create_card(slide, x, y, card_w, card_h)

        hpill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.12), Inches(y + 0.12), Inches(card_w - 0.24), Inches(0.38))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = bg_c
        hpill.line.color.rgb = border_c
        hpill.line.width = Pt(1)
        tf_hp = hpill.text_frame
        tf_hp.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_hp = tf_hp.paragraphs[0]
        p_hp.text = title.upper()
        p_hp.font.name = FONT_HEADING
        p_hp.font.size = Pt(9.5)
        p_hp.font.bold = True
        p_hp.font.color.rgb = border_c
        p_hp.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.55), Inches(card_w - 0.3), Inches(card_h - 0.65))
        tf = tb.text_frame
        tf.word_wrap = True

        for j, (lbl, txt) in enumerate(items):
            add_bullet_item(tf, lbl, txt, is_first=(j==0), font_size=9.2, bullet_color=border_c)

# ==============================================================================
# SLIDE 17: REFERENCES
# ==============================================================================
def build_slide_17(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide)
    add_header(slide, "17 | References", "Academic Literature & Technical Documentation", "Formal citations for algorithms, benchmark datasets, and frameworks utilized across the project")
    add_footer(slide, 17)

    refs = [
        ("Numenta Anomaly Benchmark (NAB)", [
            ("Citation", "Ahmad, S., Lavin, A., Purdy, S., & Agha, Z. (2017). 'Evaluating Real-Time Anomaly Detection: The Numenta Anomaly Benchmark.' IEEE Transactions on Machine Learning Applications."),
            ("Project Usage", "Source of the realAWSCloudwatch/ historical telemetry dataset across EC2, RDS, and ELB server profiles.")
        ]),
        ("Isolation Forest Algorithm", [
            ("Citation", "Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). 'Isolation Forest.' Eighth IEEE International Conference on Data Mining (ICDM), pp. 413–422."),
            ("Project Usage", "Primary tree-based unsupervised outlier detection algorithm serialized in models/isolation_forest.joblib.")
        ]),
        ("Local Outlier Factor (LOF)", [
            ("Citation", "Breunig, M. M., Kriegel, H. P., Ng, R. T., & Sander, J. (2000). 'LOF: Identifying Density-Based Local Outliers.' ACM SIGMOD Record, 29(2), pp. 93–104."),
            ("Project Usage", "Density-based cross-validation model utilized in the multi-model ensemble detection pipeline.")
        ]),
        ("Scikit-learn Machine Learning Framework", [
            ("Citation", "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2011). 'Scikit-learn: Machine Learning in Python.' Journal of Machine Learning Research (JMLR), 12, pp. 2825–2830."),
            ("Project Usage", "Provides implementations of MinMaxScaler, IsolationForest, and LocalOutlierFactor.")
        ]),
        ("Apache Spark & Distributed Computing", [
            ("Citation", "Zaharia, M., Xin, R. S., Wendell, P., Das, T., Armbrust, M., Dave, A., et al. (2016). 'Apache Spark: A Unified Engine for Big Data Processing.' Communications of the ACM, 59(11), pp. 56–65."),
            ("Project Usage", "PySpark distributed processing framework utilized for scalable server-wise metric aggregation.")
        ]),
        ("Flask & System Process Telemetry", [
            ("Citation", "Pallets Projects (2023). 'Flask: A lightweight WSGI web application framework.' https://flask.palletsprojects.com/ | Rodola, G. (2023). 'psutil: Cross-platform process and system monitoring in Python.'"),
            ("Project Usage", "Core runtime libraries for live OS metric sampling and asynchronous REST API delivery.")
        ])
    ]

    card_w = 5.7
    card_h = 1.55
    x_left = 0.8
    x_right = 6.833
    y_base = 1.72
    y_gap = 0.18

    for i, (rtitle, ritems) in enumerate(refs):
        col = i // 3
        row = i % 3
        x = x_left if col == 0 else x_right
        y = y_base + row * (card_h + y_gap)

        card = create_card(slide, x, y, card_w, card_h)

        hpill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.12), Inches(y + 0.10), Inches(card_w - 0.24), Inches(0.32))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = COLOR_BLUE_BG
        hpill.line.color.rgb = COLOR_BLUE_BORDER
        hpill.line.width = Pt(1)
        tf_hp = hpill.text_frame
        tf_hp.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_hp = tf_hp.paragraphs[0]
        p_hp.text = rtitle.upper()
        p_hp.font.name = FONT_HEADING
        p_hp.font.size = Pt(9.0)
        p_hp.font.bold = True
        p_hp.font.color.rgb = COLOR_BLUE_PRIMARY
        p_hp.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.45), Inches(card_w - 0.3), Inches(card_h - 0.50))
        tf = tb.text_frame
        tf.word_wrap = True

        for j, (lbl, txt) in enumerate(ritems):
            add_bullet_item(tf, lbl, txt, is_first=(j==0), font_size=8.8, bullet_color=COLOR_BLUE_PRIMARY)

# ==============================================================================
# SLIDE 18: THANK YOU & Q&A
# ==============================================================================
def build_slide_18(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_slide_bg(slide, COLOR_NAVY_DARK)

    hero_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.1))
    hero_card.fill.solid()
    hero_card.fill.fore_color.rgb = COLOR_NAVY_CARD
    hero_card.line.color.rgb = COLOR_NAVY_BORDER
    hero_card.line.width = Pt(1.5)

    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.666), Inches(1.2), Inches(4.0), Inches(0.38))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(12, 74, 110)
    pill.line.color.rgb = COLOR_BLUE_PRIMARY
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    tf_pill.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = "⚡ CLOUDGUARD PRESENTATION CONCLUSION"
    p_pill.font.name = FONT_HEADING
    p_pill.font.size = Pt(10.5)
    p_pill.font.bold = True
    p_pill.font.color.rgb = COLOR_BLUE_ACCENT
    p_pill.alignment = PP_ALIGN.CENTER

    t_box = slide.shapes.add_textbox(Inches(1.5), Inches(1.75), Inches(10.333), Inches(1.1))
    tf_t = t_box.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = "THANK YOU"
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(46)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_WHITE
    p_t.alignment = PP_ALIGN.CENTER

    sub_box = slide.shapes.add_textbox(Inches(1.5), Inches(2.85), Inches(10.333), Inches(0.5))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Questions & Academic Discussion"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(22)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_BLUE_ACCENT
    p_sub.alignment = PP_ALIGN.CENTER

    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.0), Inches(3.55), Inches(7.333), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = COLOR_NAVY_BORDER
    div.line.fill.background()

    info_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), Inches(3.85), Inches(8.333), Inches(2.5))
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = RGBColor(15, 23, 42)
    info_card.line.color.rgb = COLOR_NAVY_BORDER
    info_card.line.width = Pt(1)
    tf_info = info_card.text_frame
    tf_info.margin_top = Inches(0.2)
    tf_info.margin_left = Inches(0.3)
    tf_info.margin_right = Inches(0.3)

    p_prj = tf_info.paragraphs[0]
    p_prj.text = "Cloud Server Anomaly Detection System (CloudGuard)"
    p_prj.font.name = FONT_HEADING
    p_prj.font.size = Pt(14)
    p_prj.font.bold = True
    p_prj.font.color.rgb = COLOR_WHITE
    p_prj.alignment = PP_ALIGN.CENTER
    p_prj.space_after = Pt(8)

    p_tm = tf_info.add_paragraph()
    p_tm.text = "Project Team: Muhammed Anzil P P  |  Fadhil Haneef  |  [Team Member 3]"
    p_tm.font.name = FONT_BODY
    p_tm.font.size = Pt(11.5)
    p_tm.font.bold = True
    p_tm.font.color.rgb = COLOR_BLUE_ACCENT
    p_tm.alignment = PP_ALIGN.CENTER
    p_tm.space_after = Pt(4)

    p_dpt = tf_info.add_paragraph()
    p_dpt.text = "Department of Computer Science & Engineering  |  Bachelor of Technology (B.Tech)"
    p_dpt.font.name = FONT_BODY
    p_dpt.font.size = Pt(11)
    p_dpt.font.color.rgb = COLOR_LIGHT_TEXT
    p_dpt.alignment = PP_ALIGN.CENTER
    p_dpt.space_after = Pt(4)

    p_yr = tf_info.add_paragraph()
    p_yr.text = "[College / University Name]  |  Academic Year: 2025 – 2026"
    p_yr.font.name = FONT_BODY
    p_yr.font.size = Pt(10.5)
    p_yr.font.color.rgb = COLOR_MUTED_TEXT
    p_yr.alignment = PP_ALIGN.CENTER

print("Slide 12 to 18 defined")




def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    print("Building Slide 01: Cover Slide...")
    build_slide_01(prs)
    print("Building Slide 02: Contents...")
    build_slide_02(prs)
    print("Building Slide 03: Introduction...")
    build_slide_03(prs)
    print("Building Slide 04: Problem Definition...")
    build_slide_04(prs)
    print("Building Slide 05: Proposed System...")
    build_slide_05(prs)
    print("Building Slide 06: Module Description...")
    build_slide_06(prs)
    print("Building Slide 07: System Architecture...")
    build_slide_07(prs)
    print("Building Slide 08: System Requirements...")
    build_slide_08(prs)
    print("Building Slide 09: Implementation & Tech Stack...")
    build_slide_09(prs)
    print("Building Slide 10: Web Dashboard...")
    build_slide_10(prs)
    print("Building Slide 11: Working / Data Flow...")
    build_slide_11(prs)
    print("Building Slide 12: Experimental Results...")
    build_slide_12(prs)
    print("Building Slide 13: Anomaly Detection Results...")
    build_slide_13(prs)
    print("Building Slide 14: Dashboard Features...")
    build_slide_14(prs)
    print("Building Slide 15: Conclusion...")
    build_slide_15(prs)
    print("Building Slide 16: Future Scope...")
    build_slide_16(prs)
    print("Building Slide 17: References...")
    build_slide_17(prs)
    print("Building Slide 18: Thank You & Q&A...")
    build_slide_18(prs)

    output_filename = "Cloud_Server_Anomaly_Detection_Project_Presentation.pptx"
    
    # Save to project folder
    proj_output = PROJECT_DIR / output_filename
    prs.save(str(proj_output))
    print(f"Presentation saved successfully to: {proj_output}")

    # Also save to workspace root
    ws_root = PROJECT_DIR.parent.parent
    ws_output = ws_root / output_filename
    prs.save(str(ws_output))
    print(f"Presentation saved successfully to workspace root: {ws_output}")

if __name__ == "__main__":
    main()
