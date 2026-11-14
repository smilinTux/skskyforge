"""
SKSkyforge data models.

Copyright (C) 2025 smilinTux
SK = staycuriousANDkeepsmilin 🐧

This file is part of SKSkyforge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from .birth_data import BirthData, BirthTimeRange, Location
from .calendar_request import CalendarRequest
from .daily_entry import DailyPreparation
from .domains import (
    # Biorhythm
    BiorhythmData,
    CautionPeriod,
    EveningRitualData,
    # Wellness
    ExerciseRecommendation,
    # Human Design
    GateData,
    HumanDesignData,
    # I Ching
    IChingData,
    JournalingPrompt,
    MeditationPractice,
    # Moon
    MoonData,
    # Practices
    MorningRitualData,
    NourishmentGuidance,
    # Numerology
    NumerologyData,
    # Synthesis
    PowerHour,
    RiskAnalysisData,
    # Risk
    RiskWarning,
    # Solar Transit
    SolarTransitData,
    SpiritualReading,
)
from .profile import ProfileMetadata, UserProfile

__all__ = [
    # Birth Data
    "BirthData",
    "BirthTimeRange",
    "Location",
    # Profile
    "UserProfile",
    "ProfileMetadata",
    # Calendar Request
    "CalendarRequest",
    # Moon
    "MoonData",
    # Numerology
    "NumerologyData",
    # Solar Transit
    "SolarTransitData",
    # Human Design
    "GateData",
    "HumanDesignData",
    # I Ching
    "IChingData",
    # Biorhythm
    "BiorhythmData",
    # Risk
    "RiskWarning",
    "RiskAnalysisData",
    # Wellness
    "ExerciseRecommendation",
    "NourishmentGuidance",
    # Practices
    "MorningRitualData",
    "MeditationPractice",
    "JournalingPrompt",
    "SpiritualReading",
    "EveningRitualData",
    # Synthesis
    "PowerHour",
    "CautionPeriod",
    # Daily Entry
    "DailyPreparation",
]
