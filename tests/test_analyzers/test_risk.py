"""
Tests for risk analysis.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin
"""

import pytest

from skskyforge.models.domains import (
    MoonData,
    BiorhythmData,
    NumerologyData,
    RiskWarning,
)
from skskyforge.analyzers.risk import (
    calculate_risk_analysis,
    RISK_WEIGHTS,
    GROUNDING_TECHNIQUES,
)


def _make_moon(voc: bool = False, sign: str = "Aries") -> MoonData:
    """Factory helper for MoonData."""
    return MoonData(
        phase="Full Moon",
        phase_percentage=100.0,
        zodiac_sign=sign,
        sign_element="Fire",
        sign_modality="Cardinal",
        moon_void_of_course=voc,
        energy_theme="Action",
        optimal_activities=["test"],
        avoid_activities=["test"],
    )


def _make_biorhythm(
    physical: float = 50.0,
    emotional: float = 50.0,
    intellectual: float = 50.0,
    physical_critical: bool = False,
    emotional_critical: bool = False,
    intellectual_critical: bool = False,
) -> BiorhythmData:
    """Factory helper for BiorhythmData."""
    return BiorhythmData(
        physical=physical,
        emotional=emotional,
        intellectual=intellectual,
        physical_phase="High",
        emotional_phase="High",
        intellectual_phase="High",
        physical_critical=physical_critical,
        emotional_critical=emotional_critical,
        intellectual_critical=intellectual_critical,
        overall_energy="Moderate",
        best_for=["focus work"],
    )


def _make_numerology(personal_day: int = 1) -> NumerologyData:
    """Factory helper for NumerologyData."""
    return NumerologyData(
        life_path=5,
        personal_year=3,
        personal_month=6,
        personal_day=personal_day,
        universal_day=8,
        day_theme="Action",
        energy_quality="Active",
    )


class TestRiskAnalysisBaseline:
    """Test baseline (no risk factors)."""

    def test_no_risks_returns_low(self):
        result = calculate_risk_analysis(
            _make_moon(), _make_biorhythm(), _make_numerology()
        )
        assert result.overall_risk_level == "Low"
        assert result.risk_score < 25

    def test_no_risks_no_warnings(self):
        result = calculate_risk_analysis(
            _make_moon(), _make_biorhythm(), _make_numerology()
        )
        assert len(result.warnings) == 0

    def test_baseline_has_default_practices(self):
        result = calculate_risk_analysis(
            _make_moon(), _make_biorhythm(), _make_numerology()
        )
        assert len(result.protective_practices) > 0
        assert len(result.grounding_techniques) > 0


class TestMoonVOCRisk:
    """Test Moon Void of Course risk factor."""

    def test_voc_adds_spiritual_and_emotional_risk(self):
        result = calculate_risk_analysis(
            _make_moon(voc=True), _make_biorhythm(), _make_numerology()
        )
        assert result.spiritual_risk >= RISK_WEIGHTS["moon_voc"]
        assert result.emotional_risk >= RISK_WEIGHTS["moon_voc"]

    def test_voc_generates_warning(self):
        result = calculate_risk_analysis(
            _make_moon(voc=True), _make_biorhythm(), _make_numerology()
        )
        domains = [w.domain for w in result.warnings]
        assert "Spiritual" in domains


class TestBiorhythmRiskFactors:
    """Test biorhythm-related risk contributions."""

    def test_physical_critical_adds_physical_risk(self):
        result = calculate_risk_analysis(
            _make_moon(),
            _make_biorhythm(physical_critical=True),
            _make_numerology(),
        )
        assert result.physical_risk >= RISK_WEIGHTS["biorhythm_critical"]

    def test_emotional_critical_adds_emotional_risk(self):
        result = calculate_risk_analysis(
            _make_moon(),
            _make_biorhythm(emotional_critical=True),
            _make_numerology(),
        )
        assert result.emotional_risk >= RISK_WEIGHTS["biorhythm_critical"]

    def test_low_physical_adds_physical_risk(self):
        result = calculate_risk_analysis(
            _make_moon(),
            _make_biorhythm(physical=-60),
            _make_numerology(),
        )
        assert result.physical_risk >= RISK_WEIGHTS["biorhythm_low"]

    def test_low_emotional_adds_emotional_risk(self):
        result = calculate_risk_analysis(
            _make_moon(),
            _make_biorhythm(emotional=-60),
            _make_numerology(),
        )
        assert result.emotional_risk >= RISK_WEIGHTS["biorhythm_low"]

    def test_low_intellectual_adds_spiritual_risk(self):
        result = calculate_risk_analysis(
            _make_moon(),
            _make_biorhythm(intellectual=-60),
            _make_numerology(),
        )
        assert result.spiritual_risk >= 1

    def test_multiple_criticals_compound(self):
        result = calculate_risk_analysis(
            _make_moon(),
            _make_biorhythm(
                physical_critical=True,
                emotional_critical=True,
                intellectual_critical=True,
            ),
            _make_numerology(),
        )
        assert len(result.warnings) >= 3


class TestNumerologyRiskFactors:
    """Test numerology-related risk contributions."""

    def test_personal_day_7_adds_spiritual_risk(self):
        result = calculate_risk_analysis(
            _make_moon(), _make_biorhythm(), _make_numerology(personal_day=7)
        )
        assert result.spiritual_risk >= 1

    def test_personal_day_9_adds_emotional_risk(self):
        result = calculate_risk_analysis(
            _make_moon(), _make_biorhythm(), _make_numerology(personal_day=9)
        )
        assert result.emotional_risk >= 1

    def test_personal_day_4_adds_physical_risk(self):
        result = calculate_risk_analysis(
            _make_moon(), _make_biorhythm(), _make_numerology(personal_day=4)
        )
        assert result.physical_risk >= 1


class TestRiskScoring:
    """Test overall risk scoring and level determination."""

    def test_risk_scores_capped_at_10(self):
        result = calculate_risk_analysis(
            _make_moon(voc=True),
            _make_biorhythm(
                physical=-80, physical_critical=True,
                emotional=-80, emotional_critical=True,
                intellectual=-80, intellectual_critical=True,
            ),
            _make_numerology(personal_day=7),
        )
        assert result.spiritual_risk <= 10
        assert result.emotional_risk <= 10
        assert result.physical_risk <= 10

    def test_high_risk_scenario(self):
        result = calculate_risk_analysis(
            _make_moon(voc=True),
            _make_biorhythm(
                physical=-80, physical_critical=True,
                emotional=-80, emotional_critical=True,
                intellectual=-80, intellectual_critical=True,
            ),
            _make_numerology(personal_day=9),
        )
        assert result.overall_risk_level in ("Elevated", "High")
        assert result.risk_score >= 50

    def test_risk_level_categories(self):
        """Verify all four risk level categories exist."""
        assert set(GROUNDING_TECHNIQUES.keys()) == {"Low", "Moderate", "Elevated", "High"}


class TestProtectivePractices:
    """Test protective practice selection."""

    def test_high_spiritual_risk_gets_spiritual_practices(self):
        result = calculate_risk_analysis(
            _make_moon(voc=True),
            _make_biorhythm(intellectual_critical=True),
            _make_numerology(personal_day=7),
        )
        # spiritual risk should be >= 3, triggering spiritual practices
        assert any("meditation" in p.lower() or "grounding" in p.lower()
                    for p in result.protective_practices)

    def test_max_four_protective_practices(self):
        result = calculate_risk_analysis(
            _make_moon(voc=True),
            _make_biorhythm(
                physical=-80, physical_critical=True,
                emotional=-80, emotional_critical=True,
            ),
            _make_numerology(),
        )
        assert len(result.protective_practices) <= 4


class TestRiskPerformance:
    """Performance checks per PRD NFRs."""

    def test_risk_calculation_under_one_second(self):
        import time
        moon = _make_moon()
        bio = _make_biorhythm()
        num = _make_numerology()

        start = time.perf_counter()
        for _ in range(1000):
            calculate_risk_analysis(moon, bio, num)
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0  # 1000 iterations in < 1 second
