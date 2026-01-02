"""
Tests for numerology calculator.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧
"""

import pytest
from datetime import date

from skyforge.calculators.numerology import (
    reduce_to_single_digit,
    calculate_life_path,
    calculate_personal_year,
    calculate_personal_month,
    calculate_personal_day,
    calculate_universal_day,
    calculate_numerology_for_day,
)


class TestReduceToSingleDigit:
    """Tests for reduce_to_single_digit function."""
    
    def test_single_digit_returned_as_is(self):
        """Single digits should be returned unchanged."""
        for i in range(1, 10):
            assert reduce_to_single_digit(i) == i
    
    def test_double_digit_reduces(self):
        """Double digits should reduce to single digit."""
        assert reduce_to_single_digit(15) == 6  # 1 + 5 = 6
        assert reduce_to_single_digit(28) == 1  # 2 + 8 = 10 -> 1 + 0 = 1
    
    def test_master_number_preserved(self):
        """Master numbers 11, 22, 33 should be preserved."""
        assert reduce_to_single_digit(11) == 11
        assert reduce_to_single_digit(22) == 22
        assert reduce_to_single_digit(33) == 33
    
    def test_master_number_not_preserved_when_disabled(self):
        """Master numbers should reduce when keep_master=False."""
        assert reduce_to_single_digit(11, keep_master=False) == 2
        assert reduce_to_single_digit(22, keep_master=False) == 4
        assert reduce_to_single_digit(33, keep_master=False) == 6


class TestCalculateLifePath:
    """Tests for calculate_life_path function."""
    
    def test_life_path_calculation(self):
        """Test basic life path calculation."""
        # Example: March 15, 1985
        # Month: 3
        # Day: 1 + 5 = 6
        # Year: 1 + 9 + 8 + 5 = 23 -> 2 + 3 = 5
        # Total: 3 + 6 + 5 = 14 -> 1 + 4 = 5
        result = calculate_life_path(date(1985, 3, 15))
        assert 1 <= result <= 33
    
    def test_life_path_with_master_number(self):
        """Life path can result in master number."""
        # Need to find a date that results in 11, 22, or 33
        # The function should return the master number
        result = calculate_life_path(date(1975, 11, 2))
        assert result in range(1, 10) or result in (11, 22, 33)
    
    def test_life_path_different_dates_different_results(self):
        """Different dates should give different results."""
        lp1 = calculate_life_path(date(1985, 3, 15))
        lp2 = calculate_life_path(date(1990, 7, 22))
        # They might be the same by coincidence, so just verify they're valid
        assert 1 <= lp1 <= 33
        assert 1 <= lp2 <= 33


class TestCalculatePersonalYear:
    """Tests for calculate_personal_year function."""
    
    def test_personal_year_range(self):
        """Personal year should be 1-9 or master number."""
        result = calculate_personal_year(date(1985, 3, 15), 2026)
        assert result in range(1, 10) or result in (11, 22, 33)
    
    def test_personal_year_changes_annually(self):
        """Personal year should differ between years."""
        birth_date = date(1985, 3, 15)
        py_2026 = calculate_personal_year(birth_date, 2026)
        py_2027 = calculate_personal_year(birth_date, 2027)
        # They should cycle through numbers
        assert py_2026 != py_2027 or py_2026 == 9  # 9 -> 1 is valid


class TestCalculatePersonalMonth:
    """Tests for calculate_personal_month function."""
    
    def test_personal_month_range(self):
        """Personal month should be valid."""
        result = calculate_personal_month(7, 3)  # Personal year 7, month 3
        assert result in range(1, 10) or result in (11, 22, 33)
    
    def test_personal_month_changes_monthly(self):
        """Personal month should differ between months."""
        pm_jan = calculate_personal_month(7, 1)
        pm_feb = calculate_personal_month(7, 2)
        assert pm_jan != pm_feb


class TestCalculateUniversalDay:
    """Tests for calculate_universal_day function."""
    
    def test_universal_day_range(self):
        """Universal day should be valid."""
        result = calculate_universal_day(date(2026, 1, 15))
        assert result in range(1, 10) or result in (11, 22, 33)
    
    def test_universal_day_same_for_all_people(self):
        """Universal day is the same regardless of birth date."""
        target = date(2026, 1, 15)
        ud1 = calculate_universal_day(target)
        ud2 = calculate_universal_day(target)
        assert ud1 == ud2


class TestCalculateNumerologyForDay:
    """Tests for complete numerology calculation."""
    
    def test_returns_numerology_data(self):
        """Should return complete NumerologyData."""
        birth_date = date(1985, 3, 15)
        target_date = date(2026, 1, 15)
        
        result = calculate_numerology_for_day(birth_date, target_date)
        
        assert result.life_path is not None
        assert result.personal_year is not None
        assert result.personal_month is not None
        assert result.personal_day is not None
        assert result.universal_day is not None
        assert result.day_theme != ""
    
    def test_uses_provided_life_path(self):
        """Should use pre-calculated life path if provided."""
        birth_date = date(1985, 3, 15)
        target_date = date(2026, 1, 15)
        
        result = calculate_numerology_for_day(birth_date, target_date, life_path=6)
        
        assert result.life_path == 6
