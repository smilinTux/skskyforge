"""
PDF exporter for SKSkyforge daily entries.

Generates a styled PDF report with sovereign branding using ReportLab.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
Licensed under AGPL-3.0.
"""

from datetime import date
from pathlib import Path
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from ..models.daily_entry import DailyPreparation


# Sovereign theme colours
_BG = colors.HexColor("#0f0f1a")
_ACCENT = colors.HexColor("#7C3AED")
_CYAN = colors.HexColor("#00e5ff")
_TEXT = colors.HexColor("#e2e8f0")
_MUTED = colors.HexColor("#94a3b8")
_CARD_BG = colors.HexColor("#1a1a35")

# Styles
_styles = getSampleStyleSheet()

_TITLE_STYLE = ParagraphStyle(
    "SovereignTitle",
    parent=_styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=18,
    textColor=_ACCENT,
    spaceAfter=4 * mm,
)

_HEADING_STYLE = ParagraphStyle(
    "SovereignHeading",
    parent=_styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=12,
    textColor=_CYAN,
    spaceBefore=6 * mm,
    spaceAfter=2 * mm,
)

_BODY_STYLE = ParagraphStyle(
    "SovereignBody",
    parent=_styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    textColor=_TEXT,
    leading=13,
)

_SMALL_STYLE = ParagraphStyle(
    "SovereignSmall",
    parent=_styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    textColor=_MUTED,
    leading=11,
)


def _build_day_section(entry: DailyPreparation) -> list:
    """Build PDF elements for a single day."""
    elements: list = []

    # Day header
    header = (
        f"{entry.day_of_week}, {entry.date.strftime('%B %d, %Y')} "
        f"(Day {entry.day_of_year})"
    )
    elements.append(Paragraph(header, _TITLE_STYLE))
    elements.append(Paragraph(f"Theme: {entry.daily_theme}", _BODY_STYLE))
    elements.append(Spacer(1, 3 * mm))

    # Summary table
    summary_data = [
        ["Moon", f"{entry.moon.phase} in {entry.moon.zodiac_sign} ({entry.moon.sign_element})"],
        ["Sun", f"{entry.solar_transit.sun_sign} — House {entry.solar_transit.house_focus}: {entry.solar_transit.house_theme}"],
        ["Numerology", f"Personal Day {entry.numerology.personal_day} — {entry.numerology.day_theme}"],
        ["Biorhythm", f"P:{entry.biorhythm.physical:+.0f} E:{entry.biorhythm.emotional:+.0f} I:{entry.biorhythm.intellectual:+.0f} ({entry.biorhythm.overall_energy})"],
        ["I Ching", f"Hexagram {entry.i_ching.hexagram_number}: {entry.i_ching.hexagram_name}"],
        ["Risk", entry.risk_analysis.overall_risk_level],
    ]

    tbl = Table(summary_data, colWidths=[25 * mm, 140 * mm])
    tbl.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), _CYAN),
        ("TEXTCOLOR", (1, 0), (1, -1), _TEXT),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, _MUTED),
    ]))
    elements.append(tbl)
    elements.append(Spacer(1, 3 * mm))

    # Planetary aspects
    if entry.solar_transit.planetary_aspects:
        elements.append(Paragraph("Planetary Aspects", _HEADING_STYLE))
        for aspect in entry.solar_transit.planetary_aspects[:6]:
            elements.append(Paragraph(f"  {aspect}", _SMALL_STYLE))
        elements.append(Spacer(1, 2 * mm))

    # Human Design gates
    if entry.human_design.active_gates:
        elements.append(Paragraph("Human Design Gates", _HEADING_STYLE))
        gate_text = ", ".join(
            f"{g.planet}: Gate {g.gate_number}.{g.line}"
            for g in entry.human_design.active_gates[:5]
        )
        elements.append(Paragraph(gate_text, _SMALL_STYLE))
        elements.append(Spacer(1, 2 * mm))

    # Affirmation and mantra
    elements.append(Paragraph("Daily Affirmation", _HEADING_STYLE))
    elements.append(Paragraph(f'"{entry.affirmation}"', _BODY_STYLE))
    elements.append(Spacer(1, 2 * mm))
    elements.append(Paragraph(f"Mantra: {entry.daily_mantra}", _SMALL_STYLE))

    # Page break between days
    elements.append(Spacer(1, 10 * mm))

    return elements


def export_pdf(
    entries: List[DailyPreparation],
    output_path: Path,
) -> Path:
    """
    Export daily entries to PDF format.

    Generates a multi-page PDF with sovereign branding, one section
    per day containing alignment summary, planetary aspects, and
    daily guidance.

    Args:
        entries: List of generated daily entries.
        output_path: Path for the output PDF file.

    Returns:
        Path to the written file.
    """
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        title="SKSkyforge Sovereign Alignment Guide",
        author="SKSkyforge",
    )

    elements: list = []

    # Cover title
    elements.append(Paragraph("SKSkyforge", _TITLE_STYLE))
    elements.append(Paragraph("Sovereign Alignment Guide", _HEADING_STYLE))

    if entries:
        period = f"{entries[0].date.strftime('%B %d')} - {entries[-1].date.strftime('%B %d, %Y')}"
        elements.append(Paragraph(period, _BODY_STYLE))

    elements.append(Spacer(1, 10 * mm))

    # Day sections
    for entry in entries:
        elements.extend(_build_day_section(entry))

    doc.build(elements)
    return output_path
