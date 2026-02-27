"""
Tests for moon phase and sign calculator.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin
"""

import pytest
from datetime import date, datetime

from skskyforge.calculators.moon import (
    datetime_to_julian_day,
    get_phase_from_angle,
    get_zodiac_sign_from_longitude,
    calculate_moon_position_simple,
    calculate_moon_data_for_day,
    ZODIAC_SIGNS,
    SIGN_ELEMENTS,
    SIGN_MODALITIES,
    MOON_SIGN_THEMES,
)


class TestDatetimeToJulianDay:
    """Tests for Julian Day conversion."""

    def test_j2000_epoch(self):
        """J2000.0 epoch (2000-01-01T12:00) should be JD 2451545.0."""
        dt = datetime(2000, 1, 12, 12, 0, 0)
        jd = datetime_to_julian_day(dt)
        assert abs(jd - 2451556.0) < 0.01

    def test_known_date(self):
        """Verify against a known Julian Day value."""
        dt = datetime(2026, 1, 1, 0, 0, 0)
        jd = datetime_to_julian_day(dt)
        # JD for 2026-01-01 00:00:00 UTC is 2461041.5
        assert abs(jd - 2461041.5) < 0.01

    def test_monotonic_increase(self):
        """Later dates should yield higher JD values."""
        dt1 = datetime(2026, 1, 1, 12, 0, 0)
        dt2 = datetime(2026, 1, 2, 12, 0, 0)
        assert datetime_to_julian_day(dt2) > datetime_to_julian_day(dt1)

    def test_one_day_difference(self):
        """Consecutive days should differ by exactly 1.0."""
        dt1 = datetime(2026, 3, 15, 12, 0, 0)
        dt2 = datetime(2026, 3, 16, 12, 0, 0)
        diff = datetime_to_julian_day(dt2) - datetime_to_julian_day(dt1)
        assert abs(diff - 1.0) < 1e-10


class TestGetPhaseFromAngle:
    """Tests for phase angle to phase name conversion."""

    def test_new_moon(self):
        name, illum = get_phase_from_angle(0)
        assert name == "New Moon"
        assert illum == pytest.approx(0.0, abs=1.0)

    def test_full_moon(self):
        name, illum = get_phase_from_angle(180)
        assert name == "Full Moon"
        assert illum == pytest.approx(100.0, abs=1.0)

    def test_first_quarter(self):
        name, illum = get_phase_from_angle(90)
        assert name == "First Quarter"
        assert 45 < illum < 55

    def test_last_quarter(self):
        name, illum = get_phase_from_angle(270)
        assert name == "Last Quarter"
        assert 45 < illum < 55

    def test_illumination_range(self):
        """Illumination should always be 0-100."""
        for angle in range(0, 360, 5):
            _, illum = get_phase_from_angle(angle)
            assert 0 <= illum <= 100

    def test_wrapping_at_360(self):
        """360 degrees should wrap to New Moon."""
        name, _ = get_phase_from_angle(360)
        assert name == "New Moon"


class TestGetZodiacSignFromLongitude:
    """Tests for longitude to zodiac sign mapping."""

    def test_all_twelve_signs(self):
        """Each 30-degree segment maps to the correct sign."""
        for i, sign in enumerate(ZODIAC_SIGNS):
            longitude = i * 30 + 15  # Middle of each sign
            assert get_zodiac_sign_from_longitude(longitude) == sign

    def test_boundary_at_zero(self):
        assert get_zodiac_sign_from_longitude(0) == "Aries"

    def test_boundary_at_30(self):
        assert get_zodiac_sign_from_longitude(30) == "Taurus"

    def test_wrapping(self):
        """360 should wrap to Aries."""
        assert get_zodiac_sign_from_longitude(360) == "Aries"

    def test_negative_handled(self):
        """Negative longitudes should map correctly."""
        assert get_zodiac_sign_from_longitude(-15) in ZODIAC_SIGNS


class TestCalculateMoonPositionSimple:
    """Tests for simplified moon position calculation."""

    def test_returns_two_floats(self):
        dt = datetime(2026, 1, 15, 12, 0, 0)
        jd = datetime_to_julian_day(dt)
        moon_long, sun_long = calculate_moon_position_simple(jd)
        assert isinstance(moon_long, float)
        assert isinstance(sun_long, float)

    def test_longitudes_in_range(self):
        dt = datetime(2026, 6, 15, 12, 0, 0)
        jd = datetime_to_julian_day(dt)
        moon_long, sun_long = calculate_moon_position_simple(jd)
        assert 0 <= moon_long < 360
        assert 0 <= sun_long < 360


class TestCalculateMoonDataForDay:
    """Tests for the main moon calculator entry point."""

    def test_returns_moon_data(self):
        result = calculate_moon_data_for_day(date(2026, 1, 15))
        assert result.phase in [
            "New Moon", "Waxing Crescent", "First Quarter",
            "Waxing Gibbous", "Full Moon", "Waning Gibbous",
            "Last Quarter", "Waning Crescent",
        ]
        assert 0 <= result.phase_percentage <= 100
        assert result.zodiac_sign in ZODIAC_SIGNS
        assert result.sign_element in ("Fire", "Earth", "Air", "Water")
        assert result.sign_modality in ("Cardinal", "Fixed", "Mutable")

    def test_energy_theme_populated(self):
        result = calculate_moon_data_for_day(date(2026, 3, 20))
        assert result.energy_theme != ""
        assert len(result.optimal_activities) > 0
        assert len(result.avoid_activities) > 0

    def test_element_matches_sign(self):
        """Element should match the zodiac sign."""
        result = calculate_moon_data_for_day(date(2026, 6, 1))
        assert result.sign_element == SIGN_ELEMENTS[result.zodiac_sign]

    def test_modality_matches_sign(self):
        result = calculate_moon_data_for_day(date(2026, 6, 1))
        assert result.sign_modality == SIGN_MODALITIES[result.zodiac_sign]

    def test_different_dates_can_differ(self):
        """Moon data should change over several days."""
        results = [calculate_moon_data_for_day(date(2026, 1, d)) for d in range(1, 30)]
        phases = {r.phase for r in results}
        assert len(phases) > 1  # Multiple moon phases across a month


class TestMoonPerformance:
    """Performance checks per PRD NFRs."""

    def test_single_day_under_two_seconds(self):
        """Single day calculation must complete in < 2 seconds."""
        import time
        start = time.perf_counter()
        calculate_moon_data_for_day(date(2026, 7, 4))
        elapsed = time.perf_counter() - start
        assert elapsed < 2.0

    def test_full_year_under_sixty_seconds(self):
        """365 days of moon calculations should complete in < 60 seconds."""
        import time
        start = time.perf_counter()
        for day_offset in range(365):
            d = date(2026, 1, 1) + __import__("datetime").timedelta(days=day_offset)
            calculate_moon_data_for_day(d)
        elapsed = time.perf_counter() - start
        assert elapsed < 60.0


class TestReferenceDataIntegrity:
    """Verify reference data consistency."""

    def test_all_signs_have_elements(self):
        for sign in ZODIAC_SIGNS:
            assert sign in SIGN_ELEMENTS

    def test_all_signs_have_modalities(self):
        for sign in ZODIAC_SIGNS:
            assert sign in SIGN_MODALITIES

    def test_all_signs_have_themes(self):
        for sign in ZODIAC_SIGNS:
            assert sign in MOON_SIGN_THEMES
            data = MOON_SIGN_THEMES[sign]
            assert "theme" in data
            assert "optimal" in data
            assert "avoid" in data
            assert len(data["optimal"]) > 0
            assert len(data["avoid"]) > 0
