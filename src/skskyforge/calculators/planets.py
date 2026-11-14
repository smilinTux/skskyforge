"""
Planetary position and aspect calculator for SKSkyforge.

Calculates ecliptic longitudes for the classical and modern planets,
then derives major aspects between them.

Copyright (C) 2025 smilinTux
SK = staycuriousANDkeepsmilin

This file is part of SKSkyforge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from datetime import date

# Planet display names keyed by Swiss Ephemeris constant name
PLANET_NAMES = [
    "Sun",
    "Moon",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
]

# Major aspects: (name, angle, orb_degrees, symbol)
MAJOR_ASPECTS = [
    ("Conjunction", 0, 8, "\u260c"),
    ("Sextile", 60, 6, "\u26b9"),
    ("Square", 90, 7, "\u25a1"),
    ("Trine", 120, 7, "\u25b3"),
    ("Opposition", 180, 8, "\u260d"),
]

# Aspect quality descriptions
ASPECT_QUALITIES = {
    "Conjunction": "intensifying",
    "Sextile": "harmonious opportunity",
    "Square": "challenging tension",
    "Trine": "flowing harmony",
    "Opposition": "polarizing awareness",
}

# Human Design gate mapping: planet longitude -> gate number
# Each gate spans 360/64 = 5.625 degrees of ecliptic longitude
HD_GATE_ORDER = [
    41,
    19,
    13,
    49,
    30,
    55,
    37,
    63,  # 0-45 degrees
    22,
    36,
    25,
    17,
    21,
    51,
    42,
    3,  # 45-90
    27,
    24,
    2,
    23,
    8,
    20,
    16,
    35,  # 90-135
    45,
    12,
    15,
    52,
    39,
    53,
    62,
    56,  # 135-180
    31,
    33,
    7,
    4,
    29,
    59,
    40,
    64,  # 180-225
    47,
    6,
    46,
    18,
    48,
    57,
    32,
    50,  # 225-270
    28,
    44,
    1,
    43,
    14,
    34,
    9,
    5,  # 270-315
    26,
    11,
    10,
    58,
    38,
    54,
    61,
    60,  # 315-360
]


def _angular_distance(lon1: float, lon2: float) -> float:
    """Shortest angular distance between two ecliptic longitudes."""
    diff = abs(lon1 - lon2) % 360
    return min(diff, 360 - diff)


def longitude_to_hd_gate(longitude: float) -> tuple[int, int]:
    """
    Convert ecliptic longitude to Human Design gate and line.

    Args:
        longitude: Ecliptic longitude in degrees (0-360).

    Returns:
        Tuple of (gate_number, line_number).
    """
    # Each gate spans 5.625 degrees
    gate_index = int(longitude / 5.625) % 64
    gate_number = HD_GATE_ORDER[gate_index]

    # Each line spans 5.625/6 = 0.9375 degrees within the gate
    position_in_gate = longitude % 5.625
    line = int(position_in_gate / 0.9375) + 1
    line = min(line, 6)

    return gate_number, line


def calculate_planetary_positions(target_date: date) -> dict[str, float]:
    """
    Calculate ecliptic longitudes for all major planets.

    Uses Swiss Ephemeris if available, otherwise returns an
    empty dict (aspects cannot be computed without ephemeris).

    Args:
        target_date: Date to calculate for.

    Returns:
        Dict mapping planet name to ecliptic longitude in degrees.
    """
    return _calculate_positions_impl(target_date)


def calculate_aspects(
    positions: dict[str, float],
    aspects: list[tuple[str, int, int, str]] | None = None,
) -> list[str]:
    """
    Calculate major aspects between planets.

    Args:
        positions: Dict of planet name -> ecliptic longitude.
        aspects: Optional custom aspect definitions. Defaults to MAJOR_ASPECTS.

    Returns:
        List of human-readable aspect strings.
    """
    if len(positions) < 2:
        return []

    aspect_defs = aspects or MAJOR_ASPECTS
    planet_list = list(positions.items())
    result: list[str] = []

    for i, (name_a, lon_a) in enumerate(planet_list):
        for name_b, lon_b in planet_list[i + 1 :]:
            dist = _angular_distance(lon_a, lon_b)
            for aspect_name, angle, orb, symbol in aspect_defs:
                if abs(dist - angle) <= orb:
                    quality = ASPECT_QUALITIES.get(aspect_name, "")
                    result.append(
                        f"{name_a} {symbol} {name_b} ({aspect_name}, {quality})"
                    )
                    break  # only closest matching aspect per planet pair

    return result


def calculate_hd_gates(
    positions: dict[str, float],
) -> list[tuple[str, int, int]]:
    """
    Calculate Human Design gate activations from planetary positions.

    Args:
        positions: Dict of planet name -> ecliptic longitude.

    Returns:
        List of (planet_name, gate_number, line_number) tuples.
    """
    gates = []
    for planet, longitude in positions.items():
        gate, line = longitude_to_hd_gate(longitude)
        gates.append((planet, gate, line))
    return gates


# ---------------------------------------------------------------------------
# Swiss Ephemeris integration with fallback
# ---------------------------------------------------------------------------

# Map planet names to swisseph constants
_SWE_PLANETS: list[tuple[str, int]] = []

try:
    import swisseph as swe

    _SWE_PLANETS = [
        ("Sun", swe.SUN),
        ("Moon", swe.MOON),
        ("Mercury", swe.MERCURY),
        ("Venus", swe.VENUS),
        ("Mars", swe.MARS),
        ("Jupiter", swe.JUPITER),
        ("Saturn", swe.SATURN),
        ("Uranus", swe.URANUS),
        ("Neptune", swe.NEPTUNE),
        ("Pluto", swe.PLUTO),
    ]

    def _positions_swe(target_date: date) -> dict[str, float]:
        """Calculate all planetary positions using Swiss Ephemeris."""
        jd = swe.julday(
            target_date.year,
            target_date.month,
            target_date.day,
            12.0,
        )
        positions: dict[str, float] = {}
        for name, planet_id in _SWE_PLANETS:
            pos = swe.calc_ut(jd, planet_id)[0]
            positions[name] = pos[0]
        return positions

    _calculate_positions_impl = _positions_swe

except ImportError:

    def _positions_fallback(target_date: date) -> dict[str, float]:
        """Fallback: only Sun position via simple formula."""
        from .solar import _sun_longitude_simple

        return {"Sun": _sun_longitude_simple(target_date)}

    _calculate_positions_impl = _positions_fallback
