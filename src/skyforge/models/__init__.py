"""
SkyForge data models.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from .birth_data import BirthData, BirthTimeRange, Location
from .profile import UserProfile, ProfileMetadata
from .calendar_request import CalendarRequest
from .domains import (
    # Moon
    MoonData,
    # Numerology
    NumerologyData,
    # Solar Transit
    SolarTransitData,
    # Human Design
    GateData,
    HumanDesignData,
    # I Ching
    IChingData,
    # Biorhythm
    BiorhythmData,
    # Risk
    RiskWarning,
    RiskAnalysisData,
    # Wellness
    ExerciseRecommendation,
    NourishmentGuidance,
    # Practices
    MorningRitualData,
    MeditationPractice,
    JournalingPrompt,
    SpiritualReading,
    EveningRitualData,
    # Synthesis
    PowerHour,
    CautionPeriod,
)
from .daily_entry import DailyPreparation

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
