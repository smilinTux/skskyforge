"""
Tests for geocoding service.

Copyright (C) 2025 smilinTux
SK = staycuriousANDkeepsmilin
"""

from unittest.mock import MagicMock, patch

import pytest

from skskyforge.services.geocoding import (
    GeocodingResult,
    geocode_city,
    detect_timezone,
    geocode_and_update_location,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_location(lat=30.267153, lon=-97.743057, address="Austin, TX, USA"):
    """Return a mock geopy Location."""
    loc = MagicMock()
    loc.latitude = lat
    loc.longitude = lon
    loc.address = address
    return loc


# ---------------------------------------------------------------------------
# geocode_city
# ---------------------------------------------------------------------------


class TestGeocodeCity:
    """Tests for the geocode_city function."""

    @patch(
        "skskyforge.services.geocoding.detect_timezone", return_value="America/Chicago"
    )
    def test_successful_geocode(self, mock_tz):
        mock_loc = _make_location()
        mock_geolocator = MagicMock()
        mock_geolocator.geocode.return_value = mock_loc

        with patch("geopy.geocoders.Nominatim", return_value=mock_geolocator):
            result = geocode_city("Austin, TX")

        assert result is not None
        assert isinstance(result, GeocodingResult)
        assert result.city == "Austin, TX"
        assert result.latitude == 30.267153
        assert result.longitude == -97.743057
        assert result.timezone == "America/Chicago"
        assert result.display_name == "Austin, TX, USA"

    @patch(
        "skskyforge.services.geocoding.detect_timezone", return_value="America/Chicago"
    )
    def test_coordinates_rounded(self, mock_tz):
        mock_loc = _make_location(lat=51.50735090000001, lon=-0.12775829999999)
        mock_geolocator = MagicMock()
        mock_geolocator.geocode.return_value = mock_loc

        with patch("geopy.geocoders.Nominatim", return_value=mock_geolocator):
            result = geocode_city("London")

        assert result.latitude == 51.507351
        assert result.longitude == -0.127758

    @patch("skskyforge.services.geocoding.detect_timezone", return_value=None)
    def test_timezone_fallback_to_utc(self, mock_tz):
        mock_loc = _make_location()
        mock_geolocator = MagicMock()
        mock_geolocator.geocode.return_value = mock_loc

        with patch("geopy.geocoders.Nominatim", return_value=mock_geolocator):
            result = geocode_city("Somewhere")

        assert result.timezone == "UTC"

    def test_city_not_found(self):
        mock_geolocator = MagicMock()
        mock_geolocator.geocode.return_value = None

        with patch("geopy.geocoders.Nominatim", return_value=mock_geolocator):
            result = geocode_city("Nonexistent City XYZ123")

        assert result is None

    def test_geocoding_exception(self):
        mock_geolocator = MagicMock()
        mock_geolocator.geocode.side_effect = Exception("Network error")

        with patch("geopy.geocoders.Nominatim", return_value=mock_geolocator):
            result = geocode_city("Austin, TX")

        assert result is None

    def test_geopy_not_installed(self):
        with patch.dict("sys.modules", {"geopy": None, "geopy.geocoders": None}):
            # Force reimport to trigger ImportError
            import importlib
            from skskyforge.services import geocoding

            importlib.reload(geocoding)
            result = geocoding.geocode_city("Austin")
            assert result is None
            # Restore
            importlib.reload(geocoding)

    @patch(
        "skskyforge.services.geocoding.detect_timezone", return_value="Europe/London"
    )
    def test_display_name_fallback(self, mock_tz):
        """If location.address is None, display_name falls back to city."""
        mock_loc = _make_location()
        mock_loc.address = None
        mock_geolocator = MagicMock()
        mock_geolocator.geocode.return_value = mock_loc

        with patch("geopy.geocoders.Nominatim", return_value=mock_geolocator):
            result = geocode_city("TestCity")

        assert result.display_name == "TestCity"


# ---------------------------------------------------------------------------
# detect_timezone
# ---------------------------------------------------------------------------


class TestDetectTimezone:
    """Tests for the detect_timezone function."""

    def test_known_coordinates(self):
        with patch("timezonefinder.TimezoneFinder") as MockTF:
            MockTF.return_value.timezone_at.return_value = "America/Chicago"
            tz = detect_timezone(30.267, -97.743)
            assert tz == "America/Chicago"

    def test_ocean_returns_none(self):
        with patch("timezonefinder.TimezoneFinder") as MockTF:
            MockTF.return_value.timezone_at.return_value = None
            tz = detect_timezone(0.0, 0.0)
            assert tz is None

    def test_exception_returns_none(self):
        with patch("timezonefinder.TimezoneFinder") as MockTF:
            MockTF.return_value.timezone_at.side_effect = Exception("broken")
            tz = detect_timezone(30.0, -97.0)
            assert tz is None


# ---------------------------------------------------------------------------
# geocode_and_update_location
# ---------------------------------------------------------------------------


class TestGeocodeAndUpdateLocation:
    """Tests for the convenience tuple function."""

    @patch("skskyforge.services.geocoding.geocode_city")
    def test_successful(self, mock_gc):
        mock_gc.return_value = GeocodingResult(
            city="Austin, TX",
            latitude=30.267153,
            longitude=-97.743057,
            timezone="America/Chicago",
            display_name="Austin, TX, USA",
        )
        lat, lon, tz = geocode_and_update_location("Austin, TX")
        assert lat == 30.267153
        assert lon == -97.743057
        assert tz == "America/Chicago"

    @patch("skskyforge.services.geocoding.geocode_city", return_value=None)
    def test_failure_returns_defaults(self, mock_gc):
        lat, lon, tz = geocode_and_update_location("Nowhere")
        assert lat is None
        assert lon is None
        assert tz == "UTC"
