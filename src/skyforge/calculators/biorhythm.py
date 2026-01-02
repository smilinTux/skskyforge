"""
Biorhythm calculator for SkyForge.

Calculates physical, emotional, and intellectual biorhythm cycles
using standard sinusoidal formulas.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

import math
from datetime import date
from typing import List, Tuple

from ..models.domains import BiorhythmData


# Standard biorhythm cycle lengths in days
PHYSICAL_CYCLE = 23
EMOTIONAL_CYCLE = 28
INTELLECTUAL_CYCLE = 33

# Critical threshold (values within ±CRITICAL_THRESHOLD are "critical")
CRITICAL_THRESHOLD = 5


def calculate_cycle_value(days_alive: int, cycle_length: int) -> float:
    """
    Calculate biorhythm value for a single cycle.
    
    Formula: sin(2π × days_alive / cycle_length) × 100
    
    Args:
        days_alive: Number of days since birth.
        cycle_length: Length of the cycle in days.
    
    Returns:
        Cycle value from -100 to +100.
    """
    radians = 2 * math.pi * days_alive / cycle_length
    return math.sin(radians) * 100


def get_cycle_phase(value: float) -> str:
    """
    Determine the phase of a biorhythm cycle.
    
    Phases:
    - Peak: value > 80
    - High: value > 50
    - Rising: value > 0 and < 50
    - Critical: value near 0 (within ±5)
    - Falling: value < 0 and > -50
    - Low: value < -50
    - Valley: value < -80
    
    Args:
        value: Cycle value (-100 to +100).
    
    Returns:
        Phase name string.
    """
    if abs(value) <= CRITICAL_THRESHOLD:
        return "Critical"
    elif value > 80:
        return "Peak"
    elif value > 50:
        return "High"
    elif value > 0:
        return "Rising"
    elif value > -50:
        return "Falling"
    elif value > -80:
        return "Low"
    else:
        return "Valley"


def is_critical_day(days_alive: int, cycle_length: int) -> bool:
    """
    Check if a day is a critical day for a cycle.
    
    Critical days occur when the cycle crosses zero (changes from
    positive to negative or vice versa).
    
    Args:
        days_alive: Number of days since birth.
        cycle_length: Length of the cycle in days.
    
    Returns:
        True if this is a critical day for the cycle.
    """
    value = calculate_cycle_value(days_alive, cycle_length)
    return abs(value) <= CRITICAL_THRESHOLD


def calculate_overall_energy(physical: float, emotional: float, intellectual: float) -> str:
    """
    Calculate overall energy level from all three cycles.
    
    Args:
        physical: Physical cycle value.
        emotional: Emotional cycle value.
        intellectual: Intellectual cycle value.
    
    Returns:
        Overall energy: "High", "Moderate", "Low", or "Mixed"
    """
    values = [physical, emotional, intellectual]
    avg = sum(values) / 3
    
    # Check for mixed signals
    positive_count = sum(1 for v in values if v > 20)
    negative_count = sum(1 for v in values if v < -20)
    
    if positive_count >= 2 and negative_count >= 1:
        return "Mixed"
    elif negative_count >= 2 and positive_count >= 1:
        return "Mixed"
    elif avg > 40:
        return "High"
    elif avg > -20:
        return "Moderate"
    else:
        return "Low"


def get_best_activities(physical: float, emotional: float, intellectual: float) -> List[str]:
    """
    Determine best activities based on cycle values.
    
    Args:
        physical: Physical cycle value.
        emotional: Emotional cycle value.
        intellectual: Intellectual cycle value.
    
    Returns:
        List of recommended activities.
    """
    activities = []
    
    if physical > 50:
        activities.extend(["Exercise", "Physical labor", "Sports", "Active tasks"])
    elif physical > 0:
        activities.extend(["Moderate activity", "Walking", "Light exercise"])
    
    if emotional > 50:
        activities.extend(["Social events", "Creative expression", "Relationships"])
    elif emotional > 0:
        activities.extend(["Connecting with friends", "Artistic pursuits"])
    
    if intellectual > 50:
        activities.extend(["Complex problem-solving", "Learning", "Strategic planning"])
    elif intellectual > 0:
        activities.extend(["Reading", "Research", "Mental tasks"])
    
    if not activities:
        activities = ["Rest", "Routine tasks", "Self-care"]
    
    return activities[:4]  # Limit to top 4


def get_challenging_activities(physical: float, emotional: float, intellectual: float) -> List[str]:
    """
    Determine challenging activities based on cycle values.
    
    Args:
        physical: Physical cycle value.
        emotional: Emotional cycle value.
        intellectual: Intellectual cycle value.
    
    Returns:
        List of activities to avoid or approach with caution.
    """
    challenges = []
    
    if physical < -30:
        challenges.extend(["Strenuous exercise", "Physical competitions"])
    if abs(physical) <= CRITICAL_THRESHOLD:
        challenges.append("High-risk physical activities")
    
    if emotional < -30:
        challenges.extend(["Difficult conversations", "Emotional decisions"])
    if abs(emotional) <= CRITICAL_THRESHOLD:
        challenges.append("Relationship confrontations")
    
    if intellectual < -30:
        challenges.extend(["Complex analysis", "Important decisions"])
    if abs(intellectual) <= CRITICAL_THRESHOLD:
        challenges.append("Strategic planning")
    
    return challenges[:4] if challenges else ["No specific challenges today"]


def get_peak_hours_recommendation(physical: float, intellectual: float) -> Tuple[str, str]:
    """
    Get recommendations for peak activity hours.
    
    Args:
        physical: Physical cycle value.
        intellectual: Intellectual cycle value.
    
    Returns:
        Tuple of (peak_physical_hours, peak_mental_hours).
    """
    # When physical is high, morning is good for physical activity
    if physical > 30:
        physical_hours = "Morning (6-10 AM) - Physical energy peak"
    elif physical > 0:
        physical_hours = "Late morning (9-11 AM)"
    else:
        physical_hours = "Gentle movement anytime, avoid strenuous activity"
    
    # Mental peak typically in late morning/early afternoon
    if intellectual > 30:
        mental_hours = "Late morning to early afternoon (10 AM - 2 PM)"
    elif intellectual > 0:
        mental_hours = "Mid-morning (9-11 AM)"
    else:
        mental_hours = "Routine mental tasks only, avoid complex decisions"
    
    return physical_hours, mental_hours


def calculate_biorhythm_for_day(birth_date: date, target_date: date) -> BiorhythmData:
    """
    Calculate complete biorhythm data for a specific day.
    
    Args:
        birth_date: User's birth date.
        target_date: Date to calculate for.
    
    Returns:
        BiorhythmData: Complete biorhythm data for the day.
    """
    days_alive = (target_date - birth_date).days
    
    # Calculate cycle values
    physical = round(calculate_cycle_value(days_alive, PHYSICAL_CYCLE), 1)
    emotional = round(calculate_cycle_value(days_alive, EMOTIONAL_CYCLE), 1)
    intellectual = round(calculate_cycle_value(days_alive, INTELLECTUAL_CYCLE), 1)
    
    # Determine phases
    physical_phase = get_cycle_phase(physical)
    emotional_phase = get_cycle_phase(emotional)
    intellectual_phase = get_cycle_phase(intellectual)
    
    # Check for critical days
    physical_critical = is_critical_day(days_alive, PHYSICAL_CYCLE)
    emotional_critical = is_critical_day(days_alive, EMOTIONAL_CYCLE)
    intellectual_critical = is_critical_day(days_alive, INTELLECTUAL_CYCLE)
    
    # Calculate composite values
    overall_energy = calculate_overall_energy(physical, emotional, intellectual)
    best_for = get_best_activities(physical, emotional, intellectual)
    challenging_for = get_challenging_activities(physical, emotional, intellectual)
    
    # Get timing recommendations
    peak_physical, peak_mental = get_peak_hours_recommendation(physical, intellectual)
    
    # Rest recommendation
    if overall_energy == "Low":
        rest_rec = "Extra rest needed - early bedtime recommended"
    elif any([physical_critical, emotional_critical, intellectual_critical]):
        rest_rec = "Critical day - additional rest and self-care important"
    elif overall_energy == "High":
        rest_rec = "Normal rest schedule, energy levels good"
    else:
        rest_rec = "Standard rest, wind down by 10 PM"
    
    return BiorhythmData(
        physical=physical,
        emotional=emotional,
        intellectual=intellectual,
        physical_phase=physical_phase,
        emotional_phase=emotional_phase,
        intellectual_phase=intellectual_phase,
        physical_critical=physical_critical,
        emotional_critical=emotional_critical,
        intellectual_critical=intellectual_critical,
        overall_energy=overall_energy,
        best_for=best_for,
        challenging_for=challenging_for,
        peak_physical_hours=peak_physical,
        peak_mental_hours=peak_mental,
        rest_recommended=rest_rec,
    )
