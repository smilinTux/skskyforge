"""
Calendar request models for SkyForge.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from .profile import UserProfile


class CalendarRequest(BaseModel):
    """
    Request to generate a sovereign alignment calendar.
    
    Attributes:
        target_year: Year to generate calendar for (1900-2100)
        profile: User profile with birth data
        start_date: Start date (default: Jan 1 of target_year)
        end_date: End date (default: Dec 31 of target_year)
        output_formats: List of output formats to generate
    """
    target_year: int = Field(..., ge=1900, le=2100)
    profile: UserProfile
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    output_formats: List[str] = Field(default=["json"])
    
    @field_validator('output_formats')
    @classmethod
    def validate_formats(cls, v: List[str]) -> List[str]:
        """Validate output format strings."""
        valid_formats = {"json", "pdf", "excel", "csv"}
        normalized = []
        for fmt in v:
            fmt_lower = fmt.lower()
            if fmt_lower not in valid_formats:
                raise ValueError(
                    f"Invalid format: {fmt}. Valid formats: {valid_formats}"
                )
            normalized.append(fmt_lower)
        return normalized
    
    def get_start_date(self) -> date:
        """Get effective start date."""
        if self.start_date:
            return self.start_date
        return date(self.target_year, 1, 1)
    
    def get_end_date(self) -> date:
        """Get effective end date."""
        if self.end_date:
            return self.end_date
        return date(self.target_year, 12, 31)
    
    def get_date_range(self) -> List[date]:
        """
        Get list of all dates in the request range.
        
        Returns:
            List[date]: All dates from start to end (inclusive).
        """
        from datetime import timedelta
        
        start = self.get_start_date()
        end = self.get_end_date()
        
        dates = []
        current = start
        while current <= end:
            dates.append(current)
            current += timedelta(days=1)
        
        return dates
    
    def get_total_days(self) -> int:
        """Get total number of days in the request."""
        return len(self.get_date_range())
