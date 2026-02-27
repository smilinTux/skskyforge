"""
CSV exporter for SKSkyforge daily entries.

Exports a flat tabular view of daily alignment data suitable for
spreadsheet analysis and data science workflows.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
Licensed under AGPL-3.0.
"""

import csv
from pathlib import Path
from typing import List

from ..models.daily_entry import DailyPreparation


def _entry_to_row(entry: DailyPreparation) -> dict:
    """Flatten a DailyPreparation into a single dict row."""
    return {
        "date": entry.date.isoformat(),
        "day_of_week": entry.day_of_week,
        "day_of_year": entry.day_of_year,
        "daily_theme": entry.daily_theme,
        # Moon
        "moon_phase": entry.moon.phase,
        "moon_illumination": entry.moon.phase_percentage,
        "moon_sign": entry.moon.zodiac_sign,
        "moon_element": entry.moon.sign_element,
        "moon_modality": entry.moon.sign_modality,
        "moon_voc": entry.moon.moon_void_of_course,
        "moon_energy_theme": entry.moon.energy_theme,
        # Solar
        "sun_sign": entry.solar_transit.sun_sign,
        "house_focus": entry.solar_transit.house_focus,
        "house_theme": entry.solar_transit.house_theme,
        "planetary_aspects": "; ".join(entry.solar_transit.planetary_aspects),
        # Numerology
        "life_path": entry.numerology.life_path,
        "personal_year": entry.numerology.personal_year,
        "personal_month": entry.numerology.personal_month,
        "personal_day": entry.numerology.personal_day,
        "universal_day": entry.numerology.universal_day,
        "num_day_theme": entry.numerology.day_theme,
        "energy_quality": entry.numerology.energy_quality,
        # Human Design
        "hd_type": entry.human_design.type,
        "hd_strategy": entry.human_design.strategy,
        "hd_authority": entry.human_design.authority,
        "hd_gates": "; ".join(
            f"{g.planet}:G{g.gate_number}L{g.line}"
            for g in entry.human_design.active_gates
        ),
        "hd_signature": entry.human_design.signature_theme,
        # I Ching
        "hexagram_number": entry.i_ching.hexagram_number,
        "hexagram_name": entry.i_ching.hexagram_name,
        # Biorhythm
        "bio_physical": entry.biorhythm.physical,
        "bio_emotional": entry.biorhythm.emotional,
        "bio_intellectual": entry.biorhythm.intellectual,
        "bio_overall_energy": entry.biorhythm.overall_energy,
        # Risk
        "risk_level": entry.risk_analysis.overall_risk_level,
        # Synthesis
        "affirmation": entry.affirmation,
        "mantra": entry.daily_mantra,
    }


def export_csv(
    entries: List[DailyPreparation],
    output_path: Path,
) -> Path:
    """
    Export daily entries to CSV format.

    Args:
        entries: List of generated daily entries.
        output_path: Path for the output CSV file.

    Returns:
        Path to the written file.
    """
    if not entries:
        return output_path

    rows = [_entry_to_row(e) for e in entries]
    fieldnames = list(rows[0].keys())

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return output_path
