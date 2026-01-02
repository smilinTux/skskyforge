"""
Tests for biorhythm calculator.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧
"""

import pytest
import math
from datetime import date, timedelta

from skyforge.calculators.biorhythm import (
    calculate_cycle_value,
    get_cycle_phase,
    is_critical_day,
    calculate_biorhythm_for_day,
    PHYSICAL_CYCLE,
    EMOTIONAL_CYCLE,
    INTELLECTUAL_CYCLE,
)


class TestCalculateCycleValue:
    """Tests for calculate_cycle_value function."""
    
    def test_value_at_day_zero(self):
        """At birth (day 0), all cycles start at 0."""
        assert calculate_cycle_value(0, PHYSICAL_CYCLE) == pytest.approx(0, abs=0.01)
        assert calculate_cycle_value(0, EMOTIONAL_CYCLE) == pytest.approx(0, abs=0.01)
        assert calculate_cycle_value(0, INTELLECTUAL_CYCLE) == pytest.approx(0, abs=0.01)
    
    def test_value_range(self):
        """Cycle values should be between -100 and 100."""
        for days in range(0, 365):
            physical = calculate_cycle_value(days, PHYSICAL_CYCLE)
            assert -100 <= physical <= 100
            
            emotional = calculate_cycle_value(days, EMOTIONAL_CYCLE)
            assert -100 <= emotional <= 100
            
            intellectual = calculate_cycle_value(days, INTELLECTUAL_CYCLE)
            assert -100 <= intellectual <= 100
    
    def test_peak_at_quarter_cycle(self):
        """Peak (+100) should occur at 1/4 of cycle."""
        # Physical cycle: peak at day ~5.75 (23/4)
        physical_peak = calculate_cycle_value(int(PHYSICAL_CYCLE / 4), PHYSICAL_CYCLE)
        assert physical_peak > 95  # Near peak
        
    def test_valley_at_three_quarter_cycle(self):
        """Valley (-100) should occur at 3/4 of cycle."""
        physical_valley = calculate_cycle_value(int(3 * PHYSICAL_CYCLE / 4), PHYSICAL_CYCLE)
        assert physical_valley < -95  # Near valley


class TestGetCyclePhase:
    """Tests for get_cycle_phase function."""
    
    def test_peak_phase(self):
        """Values > 80 should be Peak."""
        assert get_cycle_phase(85) == "Peak"
        assert get_cycle_phase(100) == "Peak"
    
    def test_high_phase(self):
        """Values 50-80 should be High."""
        assert get_cycle_phase(60) == "High"
        assert get_cycle_phase(75) == "High"
    
    def test_critical_phase(self):
        """Values near 0 should be Critical."""
        assert get_cycle_phase(3) == "Critical"
        assert get_cycle_phase(-3) == "Critical"
        assert get_cycle_phase(0) == "Critical"
    
    def test_valley_phase(self):
        """Values < -80 should be Valley."""
        assert get_cycle_phase(-85) == "Valley"
        assert get_cycle_phase(-100) == "Valley"


class TestIsCriticalDay:
    """Tests for is_critical_day function."""
    
    def test_day_zero_is_critical(self):
        """Day zero should be critical for all cycles."""
        assert is_critical_day(0, PHYSICAL_CYCLE) == True
        assert is_critical_day(0, EMOTIONAL_CYCLE) == True
        assert is_critical_day(0, INTELLECTUAL_CYCLE) == True
    
    def test_half_cycle_is_critical(self):
        """Half cycle points should be critical."""
        # Physical: ~11.5 days
        half_physical = PHYSICAL_CYCLE // 2
        assert is_critical_day(half_physical, PHYSICAL_CYCLE) == True
    
    def test_peak_is_not_critical(self):
        """Peak is not critical."""
        quarter = PHYSICAL_CYCLE // 4
        assert is_critical_day(quarter, PHYSICAL_CYCLE) == False


class TestCalculateBiorhythmForDay:
    """Tests for complete biorhythm calculation."""
    
    def test_returns_biorhythm_data(self):
        """Should return complete BiorhythmData."""
        birth_date = date(1985, 3, 15)
        target_date = date(2026, 1, 15)
        
        result = calculate_biorhythm_for_day(birth_date, target_date)
        
        assert -100 <= result.physical <= 100
        assert -100 <= result.emotional <= 100
        assert -100 <= result.intellectual <= 100
        assert result.physical_phase in ["Peak", "High", "Rising", "Critical", "Falling", "Low", "Valley"]
        assert result.overall_energy in ["High", "Moderate", "Low", "Mixed"]
    
    def test_birth_day_values(self):
        """On birth day, all values should be near zero (critical)."""
        birth_date = date(1985, 3, 15)
        
        result = calculate_biorhythm_for_day(birth_date, birth_date)
        
        assert abs(result.physical) < 5
        assert abs(result.emotional) < 5
        assert abs(result.intellectual) < 5
    
    def test_critical_day_detection(self):
        """Critical days should be detected."""
        birth_date = date(1985, 3, 15)
        
        # Check day 0 (birth day)
        result = calculate_biorhythm_for_day(birth_date, birth_date)
        
        # At least one should be critical on birth day
        assert result.physical_critical or result.emotional_critical or result.intellectual_critical
    
    def test_best_for_recommendations(self):
        """Should provide activity recommendations."""
        birth_date = date(1985, 3, 15)
        target_date = date(2026, 1, 15)
        
        result = calculate_biorhythm_for_day(birth_date, target_date)
        
        assert isinstance(result.best_for, list)
        assert len(result.best_for) > 0
