"""
Geocoding and timezone detection service for SKSkyforge.

Uses geopy (Nominatim) for geocoding city names to coordinates,
and timezonefinder for automatic timezone detection from coordinates.

Copyright (C) 2025 smilinTux
SK = staycuriousANDkeepsmilin

This file is part of SKSkyforge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class GeocodingResult:
    """Result of a geocoding lookup."""

    city: str
    latitude: float
    longitude: float
    timezone: str
    display_name: str


def geocode_city(city: str) -> GeocodingResult | None:
    """Geocode a city name to coordinates and timezone.

    Uses the Nominatim geocoder (OpenStreetMap) via geopy, then
    detects the IANA timezone from the resulting coordinates.

    Args:
        city: City name, e.g. ``"Austin, TX"`` or ``"London, UK"``.

    Returns:
        GeocodingResult if found, otherwise ``None``.
    """
    try:
        from geopy.geocoders import Nominatim
    except ImportError:
        logger.warning("geopy not installed: pip install geopy")
        return None

    try:
        geolocator = Nominatim(
            user_agent="skskyforge/1.0",
            timeout=10,
        )
        location = geolocator.geocode(city)
        if location is None:
            logger.warning("City not found: %s", city)
            return None

        lat = location.latitude
        lon = location.longitude
        tz = detect_timezone(lat, lon)

        return GeocodingResult(
            city=city,
            latitude=round(lat, 6),
            longitude=round(lon, 6),
            timezone=tz or "UTC",
            display_name=location.address or city,
        )

    except Exception as e:
        logger.warning("Geocoding failed for '%s': %s", city, e)
        return None


def detect_timezone(latitude: float, longitude: float) -> str | None:
    """Detect IANA timezone from geographic coordinates.

    Args:
        latitude: Latitude in decimal degrees.
        longitude: Longitude in decimal degrees.

    Returns:
        IANA timezone string (e.g. ``"America/Chicago"``), or ``None``.
    """
    try:
        from timezonefinder import TimezoneFinder
    except ImportError:
        logger.warning("timezonefinder not installed: pip install timezonefinder")
        return None

    try:
        tf = TimezoneFinder()
        return tf.timezone_at(lat=latitude, lng=longitude)
    except Exception as e:
        logger.warning("Timezone detection failed: %s", e)
        return None


def geocode_and_update_location(city: str) -> tuple[float | None, float | None, str]:
    """Convenience function returning (lat, lon, timezone) for a city.

    Suitable for direct use in CLI profile creation flows.

    Args:
        city: City name to geocode.

    Returns:
        Tuple of (latitude, longitude, timezone). Lat/lon are ``None``
        on failure; timezone falls back to ``"UTC"``.
    """
    result = geocode_city(city)
    if result is None:
        return None, None, "UTC"
    return result.latitude, result.longitude, result.timezone
