"""
Moon phase and sign calculator for SkyForge.

Calculates lunar phases, zodiac signs, and void-of-course periods
using Swiss Ephemeris.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple

from ..models.domains import MoonData


# Zodiac signs in order
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Element mapping for zodiac signs
SIGN_ELEMENTS = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water",
}

# Modality mapping for zodiac signs
SIGN_MODALITIES = {
    "Aries": "Cardinal", "Cancer": "Cardinal", "Libra": "Cardinal", "Capricorn": "Cardinal",
    "Taurus": "Fixed", "Leo": "Fixed", "Scorpio": "Fixed", "Aquarius": "Fixed",
    "Gemini": "Mutable", "Virgo": "Mutable", "Sagittarius": "Mutable", "Pisces": "Mutable",
}

# Moon sign energy themes
MOON_SIGN_THEMES = {
    "Aries": {
        "theme": "Action & Initiative",
        "optimal": ["Starting new projects", "Physical activity", "Quick decisions"],
        "avoid": ["Patience-required tasks", "Delicate negotiations", "Long-term planning"],
    },
    "Taurus": {
        "theme": "Stability & Comfort",
        "optimal": ["Financial planning", "Enjoying nature", "Cooking", "Sensual pleasures"],
        "avoid": ["Rushing", "Sudden changes", "Skipping meals"],
    },
    "Gemini": {
        "theme": "Communication & Curiosity",
        "optimal": ["Writing", "Learning", "Short trips", "Networking"],
        "avoid": ["Detailed analysis", "Emotional depth", "Long-term commitments"],
    },
    "Cancer": {
        "theme": "Nurturing & Emotional Depth",
        "optimal": ["Family time", "Home projects", "Self-care", "Emotional conversations"],
        "avoid": ["Confrontations", "Major business decisions", "Excessive socializing"],
    },
    "Leo": {
        "theme": "Creativity & Self-Expression",
        "optimal": ["Creative projects", "Leadership", "Romance", "Public speaking"],
        "avoid": ["Humility tasks", "Background roles", "Criticism"],
    },
    "Virgo": {
        "theme": "Analysis & Service",
        "optimal": ["Organizing", "Health routines", "Detail work", "Helping others"],
        "avoid": ["Big picture thinking", "Spontaneity", "Overlooking details"],
    },
    "Libra": {
        "theme": "Harmony & Partnership",
        "optimal": ["Relationships", "Negotiations", "Art appreciation", "Social events"],
        "avoid": ["Confrontation", "Solo decisions", "Unbalanced situations"],
    },
    "Scorpio": {
        "theme": "Transformation & Depth",
        "optimal": ["Deep research", "Psychological work", "Intimacy", "Endings/Beginnings"],
        "avoid": ["Superficial interactions", "Avoiding emotions", "Control issues"],
    },
    "Sagittarius": {
        "theme": "Expansion & Adventure",
        "optimal": ["Travel", "Philosophy", "Higher learning", "Optimism"],
        "avoid": ["Details", "Confinement", "Pessimistic people"],
    },
    "Capricorn": {
        "theme": "Achievement & Structure",
        "optimal": ["Career planning", "Long-term goals", "Discipline", "Authority"],
        "avoid": ["Spontaneity", "Emotional displays", "Shortcuts"],
    },
    "Aquarius": {
        "theme": "Innovation & Humanity",
        "optimal": ["Technology", "Social causes", "Unconventional ideas", "Group activities"],
        "avoid": ["Tradition for tradition's sake", "Emotional demands", "Routine"],
    },
    "Pisces": {
        "theme": "Intuition & Compassion",
        "optimal": ["Meditation", "Creative arts", "Spiritual practices", "Compassion"],
        "avoid": ["Harsh reality", "Strict boundaries", "Confrontation"],
    },
}

# Phase names based on angle ranges
PHASE_RANGES = [
    (0, 22.5, "New Moon"),
    (22.5, 67.5, "Waxing Crescent"),
    (67.5, 112.5, "First Quarter"),
    (112.5, 157.5, "Waxing Gibbous"),
    (157.5, 202.5, "Full Moon"),
    (202.5, 247.5, "Waning Gibbous"),
    (247.5, 292.5, "Last Quarter"),
    (292.5, 337.5, "Waning Crescent"),
    (337.5, 360, "New Moon"),
]


def datetime_to_julian_day(dt: datetime) -> float:
    """
    Convert datetime to Julian Day number.
    
    Args:
        dt: Python datetime object.
    
    Returns:
        Julian Day number as float.
    """
    # Simple Julian Day calculation
    year = dt.year
    month = dt.month
    day = dt.day + dt.hour / 24.0 + dt.minute / 1440.0 + dt.second / 86400.0
    
    if month <= 2:
        year -= 1
        month += 12
    
    A = int(year / 100)
    B = 2 - A + int(A / 4)
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    return jd


def get_phase_from_angle(angle: float) -> Tuple[str, float]:
    """
    Convert phase angle to phase name and illumination percentage.
    
    Args:
        angle: Phase angle in degrees (0-360).
    
    Returns:
        Tuple of (phase_name, illumination_percentage).
    """
    # Illumination percentage (0 at new moon, 100 at full moon)
    illumination = (1 - abs(180 - angle) / 180) * 100
    
    # Determine phase name
    angle = angle % 360
    for start, end, phase_name in PHASE_RANGES:
        if start <= angle < end:
            return phase_name, round(illumination, 1)
    
    return "New Moon", round(illumination, 1)


def get_zodiac_sign_from_longitude(longitude: float) -> str:
    """
    Get zodiac sign from ecliptic longitude.
    
    Args:
        longitude: Ecliptic longitude in degrees (0-360).
    
    Returns:
        Zodiac sign name.
    """
    sign_index = int(longitude / 30) % 12
    return ZODIAC_SIGNS[sign_index]


def calculate_moon_position_simple(jd: float) -> Tuple[float, float]:
    """
    Calculate approximate Moon position using simplified formula.
    
    This is a simplified calculation. For production use,
    Swiss Ephemeris (swisseph) should be used for accuracy.
    
    Args:
        jd: Julian Day number.
    
    Returns:
        Tuple of (moon_longitude, sun_longitude) in degrees.
    """
    # Days since J2000.0
    d = jd - 2451545.0
    
    # Sun's mean longitude
    L_sun = (280.466 + 0.9856474 * d) % 360
    
    # Moon's mean longitude
    L_moon = (218.32 + 13.176396 * d) % 360
    
    # Moon's mean anomaly
    M_moon = (134.963 + 13.064993 * d) % 360
    
    # Moon's longitude with basic correction
    moon_long = (L_moon + 6.29 * _sin_deg(M_moon)) % 360
    
    return moon_long, L_sun


def _sin_deg(degrees: float) -> float:
    """Sine function that takes degrees."""
    import math
    return math.sin(math.radians(degrees))


def calculate_moon_data_for_day(target_date: date) -> MoonData:
    """
    Calculate complete moon data for a specific day.
    
    Args:
        target_date: Date to calculate for.
    
    Returns:
        MoonData: Complete moon data for the day.
    """
    # Convert to datetime at noon UTC
    dt = datetime(target_date.year, target_date.month, target_date.day, 12, 0, 0)
    jd = datetime_to_julian_day(dt)
    
    # Calculate positions
    moon_long, sun_long = calculate_moon_position_simple(jd)
    
    # Calculate phase angle (Moon - Sun)
    phase_angle = (moon_long - sun_long) % 360
    
    # Get phase name and illumination
    phase_name, illumination = get_phase_from_angle(phase_angle)
    
    # Get zodiac sign
    zodiac_sign = get_zodiac_sign_from_longitude(moon_long)
    
    # Get sign properties
    element = SIGN_ELEMENTS[zodiac_sign]
    modality = SIGN_MODALITIES[zodiac_sign]
    
    # Get theme data
    theme_data = MOON_SIGN_THEMES[zodiac_sign]
    
    # VOC calculation would require Swiss Ephemeris for accuracy
    # For now, we'll use a placeholder
    is_voc = False  # Would be calculated with full ephemeris
    
    return MoonData(
        phase=phase_name,
        phase_percentage=illumination,
        zodiac_sign=zodiac_sign,
        sign_element=element,
        sign_modality=modality,
        moon_void_of_course=is_voc,
        voc_start=None,
        voc_end=None,
        energy_theme=theme_data["theme"],
        optimal_activities=theme_data["optimal"],
        avoid_activities=theme_data["avoid"],
    )


# Try to use Swiss Ephemeris if available
try:
    import swisseph as swe
    
    def calculate_moon_data_for_day_swe(target_date: date) -> MoonData:
        """
        Calculate moon data using Swiss Ephemeris (more accurate).
        
        Args:
            target_date: Date to calculate for.
        
        Returns:
            MoonData: Complete moon data for the day.
        """
        # Convert to datetime at noon UTC
        dt = datetime(target_date.year, target_date.month, target_date.day, 12, 0, 0)
        jd = swe.julday(dt.year, dt.month, dt.day, 12.0)
        
        # Get Moon position
        moon_pos = swe.calc_ut(jd, swe.MOON)[0]
        moon_long = moon_pos[0]
        
        # Get Sun position
        sun_pos = swe.calc_ut(jd, swe.SUN)[0]
        sun_long = sun_pos[0]
        
        # Calculate phase angle
        phase_angle = (moon_long - sun_long) % 360
        
        # Get phase name and illumination
        phase_name, illumination = get_phase_from_angle(phase_angle)
        
        # Get zodiac sign
        zodiac_sign = get_zodiac_sign_from_longitude(moon_long)
        
        # Get sign properties
        element = SIGN_ELEMENTS[zodiac_sign]
        modality = SIGN_MODALITIES[zodiac_sign]
        
        # Get theme data
        theme_data = MOON_SIGN_THEMES[zodiac_sign]
        
        return MoonData(
            phase=phase_name,
            phase_percentage=illumination,
            zodiac_sign=zodiac_sign,
            sign_element=element,
            sign_modality=modality,
            moon_void_of_course=False,  # Would need aspect calculation
            voc_start=None,
            voc_end=None,
            energy_theme=theme_data["theme"],
            optimal_activities=theme_data["optimal"],
            avoid_activities=theme_data["avoid"],
        )
    
    # Use Swiss Ephemeris version if available
    calculate_moon_data = calculate_moon_data_for_day_swe
    
except ImportError:
    # Fall back to simple calculation
    calculate_moon_data = calculate_moon_data_for_day
