"""
SKSkyforge - Sovereign Alignment Calendar System

"Forge your sovereign path through the cosmos"

Copyright (C) 2025 smilinTux
SK = staycuriousANDkeepsmilin 🐧

This file is part of SKSkyforge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

__version__ = "1.0.0"
__author__ = "smilinTux"
__license__ = "AGPL-3.0"

from .generators import generate_daily_entry
from .models import (
    BirthData,
    BirthTimeRange,
    CalendarRequest,
    DailyPreparation,
    Location,
    UserProfile,
)

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    # Models
    "BirthData",
    "BirthTimeRange",
    "Location",
    "UserProfile",
    "CalendarRequest",
    "DailyPreparation",
    # Generators
    "generate_daily_entry",
]
