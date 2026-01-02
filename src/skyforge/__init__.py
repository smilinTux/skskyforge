"""
SkyForge - Sovereign Alignment Calendar System

"Forge your sovereign path through the cosmos"

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

__version__ = "1.0.0"
__author__ = "S&K Holding QT (Quantum Technologies)"
__license__ = "AGPL-3.0"

from .models import (
    BirthData,
    BirthTimeRange,
    Location,
    UserProfile,
    CalendarRequest,
    DailyPreparation,
)

from .generators import generate_daily_entry

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
