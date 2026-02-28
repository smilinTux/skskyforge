"""
Tests for the daily entry generator.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin
"""

import pytest
from datetime import date

from skskyforge.generators import generate_daily_entry
from skskyforge.models import (
    BirthData,
    DailyPreparation,
    UserProfile,
)


@pytest.fixture
def sample_profile():
    """Minimal valid profile for testing."""
    return UserProfile(
        name="test-user",
        birth_data=BirthData(date=date(1990, 6, 15)),
    )


class TestGenerateDailyEntry:
    """Tests for the main generate_daily_entry orchestrator."""

    def test_returns_daily_preparation(self, sample_profile):
        result = generate_daily_entry(date(2026, 3, 1), sample_profile)
        assert isinstance(result, DailyPreparation)

    def test_date_fields(self, sample_profile):
        target = date(2026, 1, 15)
        result = generate_daily_entry(target, sample_profile)
        assert result.date == target
        assert result.day_of_week == "Thursday"
        assert result.day_of_year == 15

    def test_moon_data_populated(self, sample_profile):
        result = generate_daily_entry(date(2026, 2, 10), sample_profile)
        assert result.moon is not None
        assert result.moon.phase != ""
        assert result.moon.zodiac_sign != ""
        assert result.moon.sign_element in ("Fire", "Earth", "Air", "Water")

    def test_numerology_populated(self, sample_profile):
        result = generate_daily_entry(date(2026, 2, 10), sample_profile)
        assert result.numerology is not None
        assert 1 <= result.numerology.personal_day <= 33
        assert result.numerology.life_path == sample_profile.life_path_number

    def test_biorhythm_populated(self, sample_profile):
        result = generate_daily_entry(date(2026, 2, 10), sample_profile)
        assert result.biorhythm is not None
        assert -100 <= result.biorhythm.physical <= 100
        assert -100 <= result.biorhythm.emotional <= 100
        assert -100 <= result.biorhythm.intellectual <= 100

    def test_solar_transit_populated(self, sample_profile):
        result = generate_daily_entry(date(2026, 2, 10), sample_profile)
        assert result.solar_transit is not None
        assert result.solar_transit.sun_sign != ""
        assert 1 <= result.solar_transit.house_focus <= 12

    def test_human_design_populated(self, sample_profile):
        result = generate_daily_entry(date(2026, 2, 10), sample_profile)
        assert result.human_design is not None
        assert result.human_design.type in (
            "Generator", "Manifesting Generator",
            "Projector", "Manifestor", "Reflector",
        )

    def test_i_ching_populated(self, sample_profile):
        result = generate_daily_entry(date(2026, 2, 10), sample_profile)
        assert result.i_ching is not None
        assert 1 <= result.i_ching.hexagram_number <= 64

    def test_risk_analysis_populated(self, sample_profile):
        result = generate_daily_entry(date(2026, 2, 10), sample_profile)
        assert result.risk_analysis is not None
        assert result.risk_analysis.overall_risk_level in (
            "Low", "Moderate", "Elevated", "High",
        )

    def test_wellness_populated(self, sample_profile):
        result = generate_daily_entry(date(2026, 2, 10), sample_profile)
        assert result.exercise is not None
        assert result.nourishment is not None

    def test_practices_populated(self, sample_profile):
        result = generate_daily_entry(date(2026, 2, 10), sample_profile)
        assert result.morning_ritual is not None
        assert result.meditation is not None
        assert result.journaling is not None
        assert result.spiritual_reading is not None
        assert result.evening_ritual is not None

    def test_synthesis_populated(self, sample_profile):
        result = generate_daily_entry(date(2026, 2, 10), sample_profile)
        assert result.daily_theme != ""
        assert len(result.theme_keywords) > 0
        assert len(result.power_hours) > 0
        assert result.affirmation != ""
        assert result.daily_mantra != ""
        assert result.closing_reflection != ""
        assert result.tomorrow_preview != ""

    def test_life_path_auto_calculated(self):
        """Life path should be calculated if not present on profile."""
        profile = UserProfile(
            name="fresh",
            birth_data=BirthData(date=date(1990, 6, 15)),
        )
        assert profile.life_path_number is None
        generate_daily_entry(date(2026, 1, 1), profile)
        assert profile.life_path_number is not None

    def test_different_dates_produce_different_entries(self, sample_profile):
        e1 = generate_daily_entry(date(2026, 1, 1), sample_profile)
        e2 = generate_daily_entry(date(2026, 7, 1), sample_profile)
        assert e1.date != e2.date
        assert e1.daily_theme != e2.daily_theme or e1.moon.phase != e2.moon.phase

    def test_serializable(self, sample_profile):
        """Entry must serialize to JSON via pydantic."""
        entry = generate_daily_entry(date(2026, 1, 1), sample_profile)
        data = entry.model_dump(mode="json")
        assert isinstance(data, dict)
        assert data["date"] == "2026-01-01"


class TestGeneratorPerformance:
    """Performance smoke tests."""

    def test_single_day_under_five_seconds(self, sample_profile):
        import time
        start = time.perf_counter()
        generate_daily_entry(date(2026, 4, 15), sample_profile)
        assert time.perf_counter() - start < 5.0

    def test_week_under_thirty_seconds(self, sample_profile):
        import time
        from datetime import timedelta
        start = time.perf_counter()
        d = date(2026, 1, 1)
        for _ in range(7):
            generate_daily_entry(d, sample_profile)
            d += timedelta(days=1)
        assert time.perf_counter() - start < 30.0
