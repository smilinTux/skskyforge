"""
Daily entry model - the complete daily sovereign alignment guide.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from datetime import date
from typing import List

from pydantic import BaseModel, Field

from .domains import (
    MoonData,
    NumerologyData,
    SolarTransitData,
    HumanDesignData,
    IChingData,
    BiorhythmData,
    RiskAnalysisData,
    ExerciseRecommendation,
    NourishmentGuidance,
    MorningRitualData,
    MeditationPractice,
    JournalingPrompt,
    SpiritualReading,
    EveningRitualData,
    PowerHour,
    CautionPeriod,
)


class DailyPreparation(BaseModel):
    """
    Complete daily sovereign alignment guide for optimal performance.
    
    This is the core output model of SkyForge, containing all 10 domains
    of guidance synthesized into a comprehensive daily preparation system.
    """
    
    # ==========================================================================
    # Header Information
    # ==========================================================================
    date: date
    day_of_week: str              # "Monday", "Tuesday", etc.
    day_of_year: int              # 1-366
    
    # ==========================================================================
    # 1. COSMIC ALIGNMENT
    # ==========================================================================
    moon: MoonData
    solar_transit: SolarTransitData
    
    # ==========================================================================
    # 2. PERSONAL NUMBERS
    # ==========================================================================
    numerology: NumerologyData
    
    # ==========================================================================
    # 3. DESIGN & WISDOM
    # ==========================================================================
    human_design: HumanDesignData
    i_ching: IChingData
    
    # ==========================================================================
    # 4. BIORHYTHM CYCLES
    # ==========================================================================
    biorhythm: BiorhythmData
    
    # ==========================================================================
    # 5. RISK AWARENESS
    # ==========================================================================
    risk_analysis: RiskAnalysisData
    
    # ==========================================================================
    # 6. DAILY PRACTICES (Optimal Performance)
    # ==========================================================================
    morning_ritual: MorningRitualData
    exercise: ExerciseRecommendation
    nourishment: NourishmentGuidance
    meditation: MeditationPractice
    journaling: JournalingPrompt
    spiritual_reading: SpiritualReading
    evening_ritual: EveningRitualData
    
    # ==========================================================================
    # 7. SYNTHESIS
    # ==========================================================================
    daily_theme: str = ""
    theme_keywords: List[str] = Field(default_factory=list)
    power_hours: List[PowerHour] = Field(default_factory=list)
    caution_periods: List[CautionPeriod] = Field(default_factory=list)
    affirmation: str = ""
    daily_mantra: str = ""
    closing_reflection: str = ""
    tomorrow_preview: str = ""
    
    def get_overall_energy(self) -> str:
        """Get overall energy level from biorhythm data."""
        return self.biorhythm.overall_energy
    
    def get_risk_level(self) -> str:
        """Get overall risk level."""
        return self.risk_analysis.overall_risk_level
    
    def has_critical_biorhythm(self) -> bool:
        """Check if any biorhythm cycle is at critical point."""
        return (
            self.biorhythm.physical_critical or
            self.biorhythm.emotional_critical or
            self.biorhythm.intellectual_critical
        )
    
    def has_moon_voc(self) -> bool:
        """Check if Moon is void of course."""
        return self.moon.moon_void_of_course
    
    def to_summary_dict(self) -> dict:
        """
        Get a summary dictionary for display purposes.
        
        Returns:
            dict: Key summary information.
        """
        return {
            "date": self.date.isoformat(),
            "day_of_week": self.day_of_week,
            "daily_theme": self.daily_theme,
            "moon_phase": self.moon.phase,
            "moon_sign": self.moon.zodiac_sign,
            "personal_day": self.numerology.personal_day,
            "overall_energy": self.get_overall_energy(),
            "risk_level": self.get_risk_level(),
            "affirmation": self.affirmation,
        }
