"""
Domain-specific data models for SkyForge.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# =============================================================================
# Moon Data Models
# =============================================================================

class MoonData(BaseModel):
    """Moon phase and sign data for a specific day."""
    phase: str                    # "New Moon", "Waxing Crescent", etc.
    phase_percentage: float = Field(ge=0, le=100)  # Illumination
    zodiac_sign: str              # "Aries", "Taurus", etc.
    sign_element: str             # "Fire", "Earth", "Air", "Water"
    sign_modality: str            # "Cardinal", "Fixed", "Mutable"
    moon_void_of_course: bool = False
    voc_start: Optional[datetime] = None
    voc_end: Optional[datetime] = None
    energy_theme: str = ""
    optimal_activities: List[str] = Field(default_factory=list)
    avoid_activities: List[str] = Field(default_factory=list)


# =============================================================================
# Numerology Models
# =============================================================================

class NumerologyData(BaseModel):
    """Numerological data for a specific day."""
    life_path: int                # Constant (1-9, 11, 22, 33)
    personal_year: int            # Changes each birthday
    personal_month: int
    personal_day: int             # Daily vibration
    universal_day: int            # Collective energy
    
    # Interpretations
    day_theme: str = ""
    energy_quality: str = ""      # "Reflective", "Action-oriented", etc.
    favorable_for: List[str] = Field(default_factory=list)
    challenging_for: List[str] = Field(default_factory=list)
    
    # Master number alerts
    master_number_active: bool = False
    master_number_message: Optional[str] = None


# =============================================================================
# Solar Transit Models
# =============================================================================

class SolarTransitData(BaseModel):
    """Solar return and transit data for a specific day."""
    sun_sign: str                 # Current zodiac sign of Sun
    house_focus: int = Field(ge=1, le=12)  # 1-12 based on Solar Return
    house_theme: str = ""         # "Self & Identity", "Resources", etc.
    planetary_aspects: List[str] = Field(default_factory=list)
    transit_message: str = ""


# =============================================================================
# Human Design Models
# =============================================================================

class GateData(BaseModel):
    """Single gate activation data."""
    gate_number: int = Field(ge=1, le=64)
    gate_name: str
    line: int = Field(ge=1, le=6)
    planet: str                   # "Sun", "Moon", etc.
    theme: str = ""


class HumanDesignData(BaseModel):
    """Human Design data for a specific day."""
    # User's fixed design
    type: str                     # "Generator", "Projector", etc.
    strategy: str                 # "Wait to respond", etc.
    authority: str                # "Sacral", "Emotional", etc.
    
    # Daily transits
    active_gates: List[GateData] = Field(default_factory=list)
    active_channels: List[str] = Field(default_factory=list)
    defined_centers_today: List[str] = Field(default_factory=list)
    
    # Decision guidance
    decision_cue: str = ""
    energy_management: str = ""
    signature_theme: str = ""     # "Satisfaction", "Success", etc.
    not_self_warning: str = ""


# =============================================================================
# I Ching Models
# =============================================================================

class IChingData(BaseModel):
    """I Ching hexagram data for a specific day."""
    hexagram_number: int = Field(ge=1, le=64)
    hexagram_name: str
    trigram_above: str
    trigram_below: str
    
    # Wisdom
    judgment: str = ""
    image: str = ""
    changing_lines: List[int] = Field(default_factory=list)  # 1-6
    moving_to: Optional[int] = None  # Resulting hexagram
    
    # Daily application
    daily_wisdom: str = ""
    action_guidance: str = ""
    caution: str = ""


# =============================================================================
# Biorhythm Models
# =============================================================================

class BiorhythmData(BaseModel):
    """Biorhythm cycle data for a specific day."""
    # Cycle values (-100 to +100)
    physical: float = Field(ge=-100, le=100)
    emotional: float = Field(ge=-100, le=100)
    intellectual: float = Field(ge=-100, le=100)
    
    # Cycle phases
    physical_phase: str = ""      # "Peak", "Rising", "Critical", etc.
    emotional_phase: str = ""
    intellectual_phase: str = ""
    
    # Critical day warnings
    physical_critical: bool = False
    emotional_critical: bool = False
    intellectual_critical: bool = False
    
    # Composite analysis
    overall_energy: str = ""      # "High", "Moderate", "Low", "Mixed"
    best_for: List[str] = Field(default_factory=list)
    challenging_for: List[str] = Field(default_factory=list)
    
    # Timing recommendations
    peak_physical_hours: str = ""
    peak_mental_hours: str = ""
    rest_recommended: str = ""


# =============================================================================
# Risk Analysis Models
# =============================================================================

class RiskWarning(BaseModel):
    """Individual risk warning."""
    domain: str                   # "Spiritual", "Emotional", "Physical"
    source: str                   # What triggered the warning
    message: str                  # Advice
    severity: str                 # "Caution", "Warning", "Alert"


class RiskAnalysisData(BaseModel):
    """Complete risk analysis for a day."""
    spiritual_risk: int = Field(ge=0, le=10)
    emotional_risk: int = Field(ge=0, le=10)
    physical_risk: int = Field(ge=0, le=10)
    
    overall_risk_level: str = ""  # "Low", "Moderate", "Elevated", "High"
    risk_score: float = Field(ge=0, le=100)
    
    warnings: List[RiskWarning] = Field(default_factory=list)
    protective_practices: List[str] = Field(default_factory=list)
    grounding_techniques: List[str] = Field(default_factory=list)


# =============================================================================
# Wellness Models
# =============================================================================

class ExerciseRecommendation(BaseModel):
    """Exercise recommendation for a day."""
    exercise_type: str            # "Strength", "Cardio", "Yoga", "Rest"
    intensity: str                # "High", "Moderate", "Low", "Recovery"
    optimal_time: str             # "Morning", "Midday", "Evening"
    duration_minutes: int = Field(ge=0)
    specific_activities: List[str] = Field(default_factory=list)
    avoid_today: List[str] = Field(default_factory=list)
    rationale: str = ""


class NourishmentGuidance(BaseModel):
    """Nourishment guidance for a day."""
    element_focus: str            # Based on moon sign element
    foods_emphasized: List[str] = Field(default_factory=list)
    foods_minimize: List[str] = Field(default_factory=list)
    hydration_focus: str = ""
    meal_timing: str = ""
    
    # Specific meals
    breakfast_suggestion: str = ""
    lunch_suggestion: str = ""
    dinner_suggestion: str = ""
    snack_suggestions: List[str] = Field(default_factory=list)


# =============================================================================
# Practice Models
# =============================================================================

class MorningRitualData(BaseModel):
    """Morning ritual recommendations."""
    wake_time_suggestion: str = ""
    intention_setting: str = ""
    breathwork: str = ""
    movement: str = ""
    duration_minutes: int = Field(default=15, ge=0)


class MeditationPractice(BaseModel):
    """Meditation practice for a day."""
    technique: str                # "Breath awareness", "Body scan", etc.
    duration_minutes: int = Field(ge=0)
    optimal_time: str             # "Dawn", "Midday", "Dusk"
    focus_theme: str = ""
    mantra: Optional[str] = None
    visualization: Optional[str] = None


class JournalingPrompt(BaseModel):
    """Journaling prompts for a day."""
    morning_prompt: str = ""
    evening_prompt: str = ""
    theme_exploration: str = ""
    gratitude_focus: str = ""


class SpiritualReading(BaseModel):
    """Daily spiritual reading."""
    source_type: str              # "book", "scripture", "quote", "poetry"
    tradition: str                # "Taoist", "Stoic", "Sufi", etc.
    source_title: str             # "Tao Te Ching", "Meditations", etc.
    source_author: str
    chapter_or_verse: str = ""
    reading_text: str = ""
    daily_relevance: str = ""
    contemplation_question: str = ""
    embodiment_practice: str = ""


class EveningRitualData(BaseModel):
    """Evening ritual recommendations."""
    wind_down_time: str = ""
    screen_cutoff: str = ""
    reflection_practice: str = ""
    sleep_preparation: str = ""
    optimal_sleep_time: str = ""


# =============================================================================
# Synthesis Models
# =============================================================================

class PowerHour(BaseModel):
    """Optimal time period for activities."""
    time_range: str               # "9:00 AM - 11:00 AM"
    optimal_for: List[str] = Field(default_factory=list)
    energy_type: str = ""


class CautionPeriod(BaseModel):
    """Time period requiring extra awareness."""
    time_range: str               # "2:00 PM - 4:00 PM"
    reason: str = ""
    avoid: List[str] = Field(default_factory=list)
    instead_do: List[str] = Field(default_factory=list)
