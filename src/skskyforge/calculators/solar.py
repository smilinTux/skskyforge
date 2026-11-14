"""
Solar position calculator for SKSkyforge.

Calculates sun ecliptic longitude, zodiac sign, and house focus
using Swiss Ephemeris with a simple fallback.

Copyright (C) 2025 smilinTux
SK = staycuriousANDkeepsmilin

This file is part of SKSkyforge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

import math
from datetime import date, datetime

from .moon import get_zodiac_sign_from_longitude

# House themes by number (1-12)
HOUSE_THEMES = {
    1: "Self & Identity",
    2: "Resources & Values",
    3: "Communication & Learning",
    4: "Home & Foundation",
    5: "Creativity & Joy",
    6: "Health & Service",
    7: "Partnerships & Relationships",
    8: "Transformation & Shared Resources",
    9: "Expansion & Philosophy",
    10: "Career & Public Image",
    11: "Community & Aspirations",
    12: "Spirituality & Release",
}


def _sun_longitude_simple(target_date: date) -> float:
    """
    Calculate approximate sun ecliptic longitude using simplified formula.

    Uses the low-accuracy solar position algorithm. Accurate to within
    ~1 degree, sufficient for zodiac sign determination most days.

    Args:
        target_date: Date to calculate for.

    Returns:
        Sun ecliptic longitude in degrees (0-360).
    """
    dt = datetime(target_date.year, target_date.month, target_date.day, 12, 0, 0)
    # Days since J2000.0 (2000-01-01 12:00 TT)
    d = (dt - datetime(2000, 1, 1, 12, 0, 0)).total_seconds() / 86400.0

    # Mean longitude of the Sun (degrees)
    L0 = (280.46646 + 0.9856474 * d) % 360

    # Mean anomaly of the Sun (degrees)
    M = (357.52911 + 0.9856003 * d) % 360
    M_rad = math.radians(M)

    # Equation of center (degrees)
    C = (
        1.9146 * math.sin(M_rad)
        + 0.0200 * math.sin(2 * M_rad)
        + 0.0003 * math.sin(3 * M_rad)
    )

    # Sun's ecliptic longitude
    sun_long = (L0 + C) % 360
    return sun_long


def calculate_sun_position(target_date: date) -> float:
    """
    Calculate sun ecliptic longitude for a given date.

    Uses Swiss Ephemeris if available, otherwise falls back to
    a simplified formula.

    Args:
        target_date: Date to calculate for.

    Returns:
        Sun ecliptic longitude in degrees (0-360).
    """
    return _calculate_sun_position_impl(target_date)


def get_sun_sign(target_date: date) -> str:
    """
    Get the zodiac sign the Sun occupies on a given date.

    Args:
        target_date: Date to determine sun sign for.

    Returns:
        Zodiac sign name (e.g. "Aries", "Taurus").
    """
    longitude = calculate_sun_position(target_date)
    return get_zodiac_sign_from_longitude(longitude)


def calculate_house_focus(target_date: date, birth_date: date) -> int:
    """
    Calculate the solar house focus for a given date.

    Uses the angular distance of the transiting Sun from the natal Sun
    position to determine which house is activated. Each house spans
    30 degrees of solar arc.

    Args:
        target_date: Current date.
        birth_date: User's birth date.

    Returns:
        House number 1-12.
    """
    natal_sun = calculate_sun_position(birth_date)
    transit_sun = calculate_sun_position(target_date)

    # Angular distance from natal Sun determines house
    arc = (transit_sun - natal_sun) % 360
    house = int(arc / 30) + 1
    return min(house, 12)


# ---------------------------------------------------------------------------
# Swiss Ephemeris integration with fallback
# ---------------------------------------------------------------------------

try:
    import swisseph as swe

    def _sun_longitude_swe(target_date: date) -> float:
        """Calculate sun longitude using Swiss Ephemeris."""
        jd = swe.julday(
            target_date.year,
            target_date.month,
            target_date.day,
            12.0,
        )
        sun_pos = swe.calc_ut(jd, swe.SUN)[0]
        return sun_pos[0]

    _calculate_sun_position_impl = _sun_longitude_swe

except ImportError:
    _calculate_sun_position_impl = _sun_longitude_simple
