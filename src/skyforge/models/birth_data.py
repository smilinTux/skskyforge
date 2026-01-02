"""
Birth data models for SkyForge.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from datetime import date, time
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class BirthTimeRange(str, Enum):
    """
    Approximate birth time ranges when exact time is unknown.
    
    Each range maps to a midpoint time for calculations:
    - EXACT: Use provided exact time
    - MORNING: 6:00 AM - 11:59 AM → midpoint 9:00 AM
    - AFTERNOON: 12:00 PM - 5:59 PM → midpoint 3:00 PM
    - EVENING: 6:00 PM - 9:59 PM → midpoint 8:00 PM
    - NIGHT: 10:00 PM - 5:59 AM → midpoint 2:00 AM
    - UNKNOWN: Use noon (12:00 PM) default
    """
    EXACT = "exact"
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    UNKNOWN = "unknown"
    
    def get_midpoint_time(self) -> time:
        """
        Get the midpoint time for this range.
        
        Returns:
            time: The midpoint time to use for calculations.
        """
        midpoints = {
            BirthTimeRange.EXACT: time(12, 0),      # Shouldn't be called
            BirthTimeRange.MORNING: time(9, 0),     # 6-12 midpoint
            BirthTimeRange.AFTERNOON: time(15, 0),  # 12-18 midpoint
            BirthTimeRange.EVENING: time(20, 0),    # 18-22 midpoint
            BirthTimeRange.NIGHT: time(2, 0),       # 22-6 midpoint
            BirthTimeRange.UNKNOWN: time(12, 0),    # Noon default
        }
        return midpoints.get(self, time(12, 0))


class Location(BaseModel):
    """
    Geographic location for astrological calculations.
    
    Attributes:
        city: City name for display and geocoding (e.g., "Austin, TX, USA")
        latitude: Latitude in decimal degrees (-90 to 90)
        longitude: Longitude in decimal degrees (-180 to 180)
        timezone: IANA timezone string (e.g., "America/Chicago")
    """
    city: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    timezone: str = "UTC"
    
    @field_validator('timezone')
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """Validate timezone string against pytz database."""
        import pytz
        if v not in pytz.all_timezones:
            raise ValueError(f"Invalid timezone: {v}")
        return v
    
    def has_coordinates(self) -> bool:
        """Check if coordinates are available."""
        return self.latitude is not None and self.longitude is not None
    
    def __str__(self) -> str:
        if self.city:
            return self.city
        elif self.has_coordinates():
            return f"{self.latitude:.4f}, {self.longitude:.4f}"
        return "Unknown Location"


class BirthData(BaseModel):
    """
    User's birth information for personalized calculations.
    
    Attributes:
        date: Birth date (required)
        time: Exact birth time if known
        time_range: Approximate time range if exact time unknown
        location: Birth location for accurate chart calculations
    """
    date: date
    time: Optional[time] = None
    time_range: BirthTimeRange = BirthTimeRange.UNKNOWN
    location: Optional[Location] = None
    
    def get_effective_time(self) -> time:
        """
        Get the time to use for calculations.
        
        Returns exact time if provided, otherwise returns the midpoint
        of the specified time range.
        
        Returns:
            time: The effective birth time for calculations.
        """
        if self.time is not None:
            return self.time
        return self.time_range.get_midpoint_time()
    
    def get_effective_datetime(self):
        """
        Get combined date and effective time as datetime.
        
        Returns:
            datetime: Combined birth date and time.
        """
        from datetime import datetime
        return datetime.combine(self.date, self.get_effective_time())
    
    def has_exact_time(self) -> bool:
        """Check if exact birth time is known."""
        return self.time is not None or self.time_range == BirthTimeRange.EXACT
    
    def get_time_confidence(self) -> str:
        """
        Get confidence level for time-sensitive calculations.
        
        Returns:
            str: "high", "medium", or "low"
        """
        if self.has_exact_time():
            return "high"
        elif self.time_range in (BirthTimeRange.MORNING, BirthTimeRange.AFTERNOON,
                                  BirthTimeRange.EVENING, BirthTimeRange.NIGHT):
            return "medium"
        return "low"
