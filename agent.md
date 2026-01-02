# AGENT.MD - SkyForge Sovereign Alignment Calendar System

> **Tagline**: "Forge your sovereign path through the cosmos"

This document provides comprehensive instructions for AI coding agents working on the SkyForge project. It contains all specifications, algorithms, data models, and coding guidelines needed to build and maintain this system.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Development Environment Setup](#2-development-environment-setup)
3. [Architecture & File Structure](#3-architecture--file-structure)
4. [Data Models](#4-data-models)
5. [Domain Calculation Specifications](#5-domain-calculation-specifications)
6. [API & CLI Specifications](#6-api--cli-specifications)
7. [Output Generation](#7-output-generation)
8. [Testing Requirements](#8-testing-requirements)
9. [Code Style & Conventions](#9-code-style--conventions)
10. [Security & Data Privacy](#10-security--data-privacy)
11. [Reference Data](#11-reference-data)

---

## 1. Project Overview

### 1.1 Purpose

SkyForge is a Python-based system that generates **fully integrated daily sovereign alignment calendars** for any year and any user. It combines **10 domains** of guidance into a unified daily preparation system for **optimal performance**.

### 1.2 Core Features

- **Year-Agnostic**: Generate calendars for any year (2025, 2026, 2027, etc.)
- **Multi-User Profiles**: Support multiple users with saved birth data
- **10 Domain Integration**: Comprehensive daily guidance from multiple wisdom systems
- **Multiple Output Formats**: PDF, Excel/CSV, JSON, Web Dashboard

### 1.3 The 10 Domains

| # | Domain | Description |
|---|--------|-------------|
| 1 | 🌓 Moon Phase & Sign | Lunar phase, zodiac position, void-of-course periods |
| 2 | 🔢 Numerology | Life path, personal year/month/day calculations |
| 3 | 🌞 Solar Return | Annual chart, house focus, planetary transits |
| 4 | 🧬 Human Design | Type, strategy, authority, daily gate activations |
| 5 | ☯️ I Ching | Daily hexagram overlay with wisdom guidance |
| 6 | 📈 Biorhythm | Physical, emotional, intellectual cycle tracking |
| 7 | ⚠️ Risk Analysis | Multi-domain risk scoring and warnings |
| 8 | 🧘 Exercise & Embodiment | Physical activity recommendations |
| 9 | 🥣 Nourishment | Element-based dietary guidance |
| 10 | 📖 Spiritual Reading | Daily wisdom texts from curated library |

Plus: Meditation practices, journaling prompts, morning/evening rituals.

---

## 2. Development Environment Setup

### 2.1 Prerequisites

- Python 3.10 or later
- pip or poetry for dependency management
- Git for version control

### 2.2 Installation

```bash
# Clone the repository
git clone <repository_url>
cd skyforge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Download Swiss Ephemeris data files
python -m skyforge.setup_ephemeris
```

### 2.3 Environment Variables

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Required variables:

```env
# Geocoding (optional - for city name lookup)
GEOCODING_API_KEY=your_api_key_here

# Output directory
SKYFORGE_OUTPUT_DIR=./output

# Default profile name
SKYFORGE_DEFAULT_PROFILE=default

# Swiss Ephemeris data path
SWISSEPH_PATH=./ephe
```

### 2.4 Swiss Ephemeris Setup

The system requires Swiss Ephemeris data files for accurate astronomical calculations:

```bash
# The setup script downloads required ephemeris files
python -m skyforge.setup_ephemeris

# Files are stored in ./ephe directory:
# - sepl_18.se1 (planets 1800-2400)
# - semo_18.se1 (moon 1800-2400)
# - seas_18.se1 (asteroids)
```

---

## 3. Architecture & File Structure

### 3.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUTS                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ Target   │  │ Birth    │  │ Birth    │  │ Birth Location   │ │
│  │ Year     │  │ Date     │  │ Time     │  │ (City/Coords)    │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬─────────┘ │
└───────┼─────────────┼─────────────┼──────────────────┼──────────┘
        │             │             │                  │
        v             v             v                  v
┌─────────────────────────────────────────────────────────────────┐
│                     LOCATION SERVICES                            │
│  ┌─────────────────────┐    ┌─────────────────────────────────┐ │
│  │ City Name Geocoder  │───>│ Timezone Detection              │ │
│  │ (geopy)             │    │ (timezonefinder)                │ │
│  └─────────────────────┘    └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────────┐
│                      CORE ENGINES                                │
│  ┌─────────────────┐ ┌─────────────────┐ ┌───────────────────┐  │
│  │ Swiss Ephemeris │ │ Numerology      │ │ Biorhythm         │  │
│  │ (pyswisseph)    │ │ Engine          │ │ Engine            │  │
│  └────────┬────────┘ └────────┬────────┘ └─────────┬─────────┘  │
└───────────┼───────────────────┼─────────────────────┼───────────┘
            │                   │                     │
            v                   v                     v
┌─────────────────────────────────────────────────────────────────┐
│                   10 DOMAIN PROCESSORS                           │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │ Moon Phase │ │ Numerology │ │ Solar      │ │ Human      │   │
│  │ & Sign     │ │ Theme      │ │ Return     │ │ Design     │   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │ I Ching    │ │ Biorhythm  │ │ Risk       │ │ Exercise & │   │
│  │ Hexagrams  │ │ Curves     │ │ Analysis   │ │ Nourishment│   │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘   │
│  ┌────────────┐ ┌────────────┐                                  │
│  │ Meditation │ │ Spiritual  │                                  │
│  │ & Journal  │ │ Reading    │                                  │
│  └────────────┘ └────────────┘                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              v
┌─────────────────────────────────────────────────────────────────┐
│                     OUTPUT GENERATORS                            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐ │
│  │ PDF         │ │ Excel/CSV   │ │ JSON        │ │ Web       │ │
│  │ (ReportLab) │ │ (OpenPyXL)  │ │ Export      │ │ Dashboard │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └───────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 File Structure

```
skyforge/
├── agent.md                      # AI agent instructions (THIS FILE)
├── prd.txt                       # Product requirements document
├── requirements.txt              # Python dependencies
├── README.md                     # User documentation
├── pyproject.toml                # Project metadata & CLI entry point
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore patterns
│
├── config/
│   ├── settings.yaml             # Global settings
│   └── profiles/
│       └── default.yaml          # Default user profile
│
├── src/
│   └── skyforge/
│       ├── __init__.py
│       ├── cli.py                # Click-based CLI
│       ├── main.py               # Entry point
│       │
│       ├── models/               # Pydantic data models
│       │   ├── __init__.py
│       │   ├── birth_data.py     # BirthData, BirthTimeRange, Location
│       │   ├── profile.py        # UserProfile
│       │   ├── calendar_request.py
│       │   ├── daily_entry.py    # DailyPreparation and all sub-models
│       │   ├── moon.py           # MoonData
│       │   ├── numerology.py     # NumerologyData
│       │   ├── solar_return.py   # SolarTransitData
│       │   ├── human_design.py   # HumanDesignData, GateData
│       │   ├── i_ching.py        # IChingData
│       │   ├── biorhythm.py      # BiorhythmData
│       │   ├── risk.py           # RiskAnalysisData, RiskWarning
│       │   ├── wellness.py       # Exercise, Nourishment models
│       │   ├── practices.py      # Meditation, Journaling, Rituals
│       │   └── spiritual.py      # SpiritualReading, SpiritualLibrary
│       │
│       ├── services/             # External service integrations
│       │   ├── __init__.py
│       │   ├── geocoding.py      # City to coordinates
│       │   └── timezone.py       # Timezone detection
│       │
│       ├── calculators/          # Domain calculation engines
│       │   ├── __init__.py
│       │   ├── ephemeris.py      # Swiss Ephemeris wrapper
│       │   ├── moon.py           # Moon phase and zodiac sign
│       │   ├── numerology.py     # Life path, personal year/day
│       │   ├── biorhythm.py      # Physical/emotional/intellectual
│       │   ├── solar_return.py   # Annual chart analysis
│       │   ├── human_design.py   # Gates, channels, type
│       │   └── i_ching.py        # 64 hexagram mappings
│       │
│       ├── analyzers/            # Composite analysis
│       │   ├── __init__.py
│       │   ├── risk.py           # Multi-domain risk scoring
│       │   ├── wellness.py       # Exercise/nourishment rules
│       │   └── spiritual.py      # Spiritual reading selector
│       │
│       ├── generators/           # Output generation
│       │   ├── __init__.py
│       │   ├── calendar.py       # Full calendar orchestrator
│       │   ├── daily_entry.py    # Single day aggregator
│       │   ├── pdf_export.py     # ReportLab PDF generation
│       │   ├── excel_export.py   # OpenPyXL spreadsheet
│       │   └── json_export.py    # JSON serialization
│       │
│       ├── data/                 # Static reference data
│       │   ├── gates_hexagrams.json    # HD 64 gates to I Ching mapping
│       │   ├── zodiac_signs.json       # Sign characteristics
│       │   ├── moon_phases.json        # Phase interpretations
│       │   ├── numerology_meanings.json
│       │   ├── wellness_rules.json     # Recommendation engine rules
│       │   └── spiritual_library/      # Curated wisdom texts
│       │       ├── tao_te_ching.json
│       │       ├── meditations_aurelius.json
│       │       ├── rumi_poetry.json
│       │       ├── dhammapada.json
│       │       ├── bhagavad_gita.json
│       │       ├── proverbs_wisdom.json
│       │       ├── hafiz_poetry.json
│       │       ├── zen_koans.json
│       │       └── wisdom_quotes.json
│       │
│       └── web/                  # FastAPI dashboard
│           ├── __init__.py
│           ├── app.py
│           ├── routers/
│           │   ├── __init__.py
│           │   ├── calendar.py
│           │   └── profiles.py
│           └── templates/
│               ├── base.html
│               ├── index.html
│               └── daily.html
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── test_calculators/
│   │   ├── __init__.py
│   │   ├── test_moon.py
│   │   ├── test_numerology.py
│   │   ├── test_biorhythm.py
│   │   ├── test_human_design.py
│   │   └── test_i_ching.py
│   ├── test_generators/
│   │   ├── __init__.py
│   │   ├── test_daily_entry.py
│   │   └── test_exports.py
│   └── test_integration.py
│
├── ephe/                         # Swiss Ephemeris data files
│   └── .gitkeep
│
└── output/                       # Generated calendars
    └── .gitkeep
```

---

## 4. Data Models

### 4.1 User Input Models

```python
from enum import Enum
from datetime import date, time, datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field, field_validator


class BirthTimeRange(str, Enum):
    """When exact birth time is unknown, use approximate range."""
    EXACT = "exact"           # Known precise time
    MORNING = "morning"       # 6:00 AM - 11:59 AM → midpoint 9:00 AM
    AFTERNOON = "afternoon"   # 12:00 PM - 5:59 PM → midpoint 3:00 PM
    EVENING = "evening"       # 6:00 PM - 9:59 PM → midpoint 8:00 PM
    NIGHT = "night"           # 10:00 PM - 5:59 AM → midpoint 2:00 AM
    UNKNOWN = "unknown"       # Use noon (12:00 PM) default


class Location(BaseModel):
    """Geographic location for astrological calculations."""
    city: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    timezone: str = "UTC"
    
    @field_validator('timezone')
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """Validate timezone string."""
        import pytz
        if v not in pytz.all_timezones:
            raise ValueError(f"Invalid timezone: {v}")
        return v


class BirthData(BaseModel):
    """User's birth information for calculations."""
    date: date                                    # REQUIRED
    time: Optional[time] = None                   # Exact time if known
    time_range: BirthTimeRange = BirthTimeRange.UNKNOWN
    location: Optional[Location] = None
    
    def get_effective_time(self) -> time:
        """Return the time to use for calculations."""
        if self.time is not None:
            return self.time
        
        # Midpoint mapping for time ranges
        midpoints = {
            BirthTimeRange.EXACT: time(12, 0),      # Shouldn't happen
            BirthTimeRange.MORNING: time(9, 0),     # 6-12 midpoint
            BirthTimeRange.AFTERNOON: time(15, 0),  # 12-18 midpoint
            BirthTimeRange.EVENING: time(20, 0),    # 18-22 midpoint
            BirthTimeRange.NIGHT: time(2, 0),       # 22-6 midpoint
            BirthTimeRange.UNKNOWN: time(12, 0),    # Noon default
        }
        return midpoints.get(self.time_range, time(12, 0))


class UserProfile(BaseModel):
    """Complete user profile with birth data and computed values."""
    name: str
    birth_data: BirthData
    current_location: Optional[Location] = None
    
    # Auto-calculated fields (populated after creation)
    life_path_number: Optional[int] = None
    human_design_type: Optional[str] = None
    human_design_authority: Optional[str] = None


class CalendarRequest(BaseModel):
    """Request to generate a calendar."""
    target_year: int = Field(..., ge=1900, le=2100)
    profile: UserProfile
    start_date: Optional[date] = None   # Default: Jan 1 of target_year
    end_date: Optional[date] = None     # Default: Dec 31 of target_year
    output_formats: List[str] = ["json"]
    
    @field_validator('output_formats')
    @classmethod
    def validate_formats(cls, v: List[str]) -> List[str]:
        valid = {"json", "pdf", "excel", "csv"}
        for fmt in v:
            if fmt.lower() not in valid:
                raise ValueError(f"Invalid format: {fmt}. Valid: {valid}")
        return [f.lower() for f in v]
```

### 4.2 Daily Entry Models

```python
class DailyPreparation(BaseModel):
    """Complete daily sovereign alignment guide for optimal performance."""
    
    # Header
    date: date
    day_of_week: str
    day_of_year: int
    
    # 1. COSMIC ALIGNMENT
    moon: "MoonData"
    solar_transit: "SolarTransitData"
    
    # 2. PERSONAL NUMBERS
    numerology: "NumerologyData"
    
    # 3. DESIGN & WISDOM
    human_design: "HumanDesignData"
    i_ching: "IChingData"
    
    # 4. BIORHYTHM CYCLES
    biorhythm: "BiorhythmData"
    
    # 5. RISK AWARENESS
    risk_analysis: "RiskAnalysisData"
    
    # 6. DAILY PRACTICES
    morning_ritual: "MorningRitualData"
    exercise: "ExerciseRecommendation"
    nourishment: "NourishmentGuidance"
    meditation: "MeditationPractice"
    journaling: "JournalingPrompt"
    spiritual_reading: "SpiritualReading"
    evening_ritual: "EveningRitualData"
    
    # 7. SYNTHESIS
    daily_theme: str
    theme_keywords: List[str]
    power_hours: List["PowerHour"]
    caution_periods: List["CautionPeriod"]
    affirmation: str
    daily_mantra: str
    closing_reflection: str
    tomorrow_preview: str
```

### 4.3 Domain-Specific Models

See Section 5 for complete model definitions for each domain.

---

## 5. Domain Calculation Specifications

### 5.1 Moon Phase & Sign Calculator

**File**: `src/skyforge/calculators/moon.py`

**Algorithm**:

```python
import swisseph as swe
from datetime import datetime
from typing import Tuple

def calculate_moon_data(target_date: datetime, timezone: str = "UTC") -> dict:
    """
    Calculate moon phase and zodiac sign for a given date.
    
    Args:
        target_date: The date to calculate for
        timezone: Timezone string (e.g., "America/New_York")
    
    Returns:
        Dictionary with moon phase, sign, and related data
    """
    # Convert to Julian Day
    jd = swe.julday(
        target_date.year,
        target_date.month,
        target_date.day,
        target_date.hour + target_date.minute / 60.0
    )
    
    # Get Moon position
    moon_pos = swe.calc_ut(jd, swe.MOON)[0]
    moon_longitude = moon_pos[0]  # Ecliptic longitude
    
    # Get Sun position for phase calculation
    sun_pos = swe.calc_ut(jd, swe.SUN)[0]
    sun_longitude = sun_pos[0]
    
    # Calculate phase angle (Moon - Sun)
    phase_angle = (moon_longitude - sun_longitude) % 360
    
    # Determine phase name and percentage
    phase_name, phase_pct = get_phase_from_angle(phase_angle)
    
    # Determine zodiac sign (30 degrees per sign)
    sign_index = int(moon_longitude / 30)
    sign_names = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    zodiac_sign = sign_names[sign_index]
    
    # Get sign properties
    elements = ["Fire", "Earth", "Air", "Water"]
    modalities = ["Cardinal", "Fixed", "Mutable"]
    
    return {
        "phase": phase_name,
        "phase_percentage": phase_pct,
        "zodiac_sign": zodiac_sign,
        "sign_element": elements[sign_index % 4],
        "sign_modality": modalities[sign_index % 3],
        "longitude": moon_longitude,
    }


def get_phase_from_angle(angle: float) -> Tuple[str, float]:
    """Convert phase angle to phase name and illumination percentage."""
    # Illumination percentage (0 at new moon, 100 at full)
    illumination = (1 - abs(180 - angle) / 180) * 100
    
    # Phase names based on angle ranges
    if angle < 22.5 or angle >= 337.5:
        return "New Moon", illumination
    elif angle < 67.5:
        return "Waxing Crescent", illumination
    elif angle < 112.5:
        return "First Quarter", illumination
    elif angle < 157.5:
        return "Waxing Gibbous", illumination
    elif angle < 202.5:
        return "Full Moon", illumination
    elif angle < 247.5:
        return "Waning Gibbous", illumination
    elif angle < 292.5:
        return "Last Quarter", illumination
    else:
        return "Waning Crescent", illumination


def calculate_void_of_course(target_date: datetime) -> dict:
    """
    Calculate Void of Course Moon periods.
    
    VOC occurs from the Moon's last major aspect in a sign
    until it enters the next sign.
    
    Returns:
        Dictionary with is_voc, voc_start, voc_end times
    """
    # Implementation uses Swiss Ephemeris to find:
    # 1. When Moon makes its last major aspect (conjunction, sextile,
    #    square, trine, opposition) to a planet
    # 2. When Moon enters the next sign
    # The period between these is VOC
    pass  # Full implementation in actual code
```

**Data Model**:

```python
class MoonData(BaseModel):
    """Moon phase and sign data for a specific day."""
    phase: str                    # "New Moon", "Waxing Crescent", etc.
    phase_percentage: float       # 0.0 to 100.0 illumination
    zodiac_sign: str              # "Aries", "Taurus", etc.
    sign_element: str             # "Fire", "Earth", "Air", "Water"
    sign_modality: str            # "Cardinal", "Fixed", "Mutable"
    moon_void_of_course: bool     # True if VOC period active
    voc_start: Optional[datetime] = None
    voc_end: Optional[datetime] = None
    energy_theme: str             # Interpretive theme
    optimal_activities: List[str]
    avoid_activities: List[str]
```

### 5.2 Numerology Calculator

**File**: `src/skyforge/calculators/numerology.py`

**Algorithms**:

```python
def reduce_to_single_digit(number: int, keep_master: bool = True) -> int:
    """
    Reduce a number to a single digit (1-9) or master number (11, 22, 33).
    
    Args:
        number: The number to reduce
        keep_master: If True, preserve master numbers 11, 22, 33
    
    Returns:
        Single digit or master number
    """
    while number > 9:
        if keep_master and number in (11, 22, 33):
            return number
        number = sum(int(d) for d in str(number))
    return number


def calculate_life_path(birth_date: date) -> int:
    """
    Calculate Life Path number from birth date.
    
    Formula: Reduce (Month + Day + Year) to single digit or master number
    
    Example: March 15, 1985
        Month: 3
        Day: 1 + 5 = 6
        Year: 1 + 9 + 8 + 5 = 23 → 2 + 3 = 5
        Total: 3 + 6 + 5 = 14 → 1 + 4 = 5
        Life Path: 5
    """
    month = reduce_to_single_digit(birth_date.month)
    day = reduce_to_single_digit(birth_date.day)
    year = reduce_to_single_digit(sum(int(d) for d in str(birth_date.year)))
    
    total = month + day + year
    return reduce_to_single_digit(total)


def calculate_personal_year(birth_date: date, target_year: int) -> int:
    """
    Calculate Personal Year number.
    
    Formula: Reduce (Birth Month + Birth Day + Target Year)
    
    Note: Personal Year runs birthday to birthday, not Jan 1 to Dec 31.
    """
    month = reduce_to_single_digit(birth_date.month)
    day = reduce_to_single_digit(birth_date.day)
    year = reduce_to_single_digit(sum(int(d) for d in str(target_year)))
    
    total = month + day + year
    return reduce_to_single_digit(total)


def calculate_personal_month(personal_year: int, month: int) -> int:
    """
    Calculate Personal Month number.
    
    Formula: Reduce (Personal Year + Calendar Month)
    """
    total = personal_year + month
    return reduce_to_single_digit(total)


def calculate_personal_day(personal_month: int, day: int) -> int:
    """
    Calculate Personal Day number.
    
    Formula: Reduce (Personal Month + Calendar Day)
    """
    total = personal_month + day
    return reduce_to_single_digit(total)


def calculate_universal_day(target_date: date) -> int:
    """
    Calculate Universal Day number (collective energy).
    
    Formula: Reduce (Month + Day + Year of target date)
    """
    total = target_date.month + target_date.day + sum(int(d) for d in str(target_date.year))
    return reduce_to_single_digit(total)
```

**Data Model**:

```python
class NumerologyData(BaseModel):
    """Numerological data for a specific day."""
    life_path: int                # Constant for the person (1-9, 11, 22, 33)
    personal_year: int            # Changes each birthday
    personal_month: int           # Changes each month
    personal_day: int             # Daily vibration
    universal_day: int            # Collective energy
    
    # Interpretations
    day_theme: str
    energy_quality: str           # "Reflective", "Action-oriented", etc.
    favorable_for: List[str]
    challenging_for: List[str]
    
    # Master number alerts
    master_number_active: bool
    master_number_message: Optional[str] = None
```

### 5.3 Biorhythm Calculator

**File**: `src/skyforge/calculators/biorhythm.py`

**Algorithm**:

```python
import math
from datetime import date

# Cycle lengths in days
PHYSICAL_CYCLE = 23
EMOTIONAL_CYCLE = 28
INTELLECTUAL_CYCLE = 33


def calculate_biorhythm(birth_date: date, target_date: date) -> dict:
    """
    Calculate biorhythm values for a given date.
    
    Formula: sin(2π × days_since_birth / cycle_length) × 100
    
    Returns values from -100 to +100 for each cycle.
    """
    days_alive = (target_date - birth_date).days
    
    physical = math.sin(2 * math.pi * days_alive / PHYSICAL_CYCLE) * 100
    emotional = math.sin(2 * math.pi * days_alive / EMOTIONAL_CYCLE) * 100
    intellectual = math.sin(2 * math.pi * days_alive / INTELLECTUAL_CYCLE) * 100
    
    return {
        "physical": round(physical, 1),
        "emotional": round(emotional, 1),
        "intellectual": round(intellectual, 1),
        "days_alive": days_alive,
    }


def get_cycle_phase(value: float, prev_value: float = None) -> str:
    """
    Determine the phase of a biorhythm cycle.
    
    Phases:
    - Peak: value > 80
    - Rising: value > 0 and increasing
    - Critical: value near 0 (crossing point) - within ±5
    - Falling: value > 0 and decreasing
    - Low: value < -80
    - Recovering: value < 0 and increasing
    - Declining: value < 0 and decreasing
    """
    if abs(value) <= 5:
        return "Critical"
    elif value > 80:
        return "Peak"
    elif value < -80:
        return "Low"
    elif value > 0:
        return "High" if value > 50 else "Rising"
    else:
        return "Low" if value < -50 else "Recovering"


def is_critical_day(birth_date: date, target_date: date, cycle_length: int) -> bool:
    """
    Check if target_date is a critical day for a cycle.
    
    Critical days occur when the cycle crosses zero (changes from
    positive to negative or vice versa).
    """
    days_alive = (target_date - birth_date).days
    # Critical when days_alive is a multiple of half the cycle
    half_cycle = cycle_length / 2
    position_in_cycle = days_alive % cycle_length
    
    # Critical if near 0 or half-cycle point (within 0.5 days)
    return position_in_cycle < 0.5 or abs(position_in_cycle - half_cycle) < 0.5
```

**Data Model**:

```python
class BiorhythmData(BaseModel):
    """Biorhythm cycle data for a specific day."""
    # Cycle values (-100 to +100)
    physical: float
    emotional: float
    intellectual: float
    
    # Cycle phases
    physical_phase: str           # "Peak", "Rising", "Critical", etc.
    emotional_phase: str
    intellectual_phase: str
    
    # Critical day warnings (crossing zero)
    physical_critical: bool
    emotional_critical: bool
    intellectual_critical: bool
    
    # Composite analysis
    overall_energy: str           # "High", "Moderate", "Low", "Mixed"
    best_for: List[str]
    challenging_for: List[str]
    
    # Timing recommendations
    peak_physical_hours: str
    peak_mental_hours: str
    rest_recommended: str
```

### 5.4 Solar Return Calculator

**File**: `src/skyforge/calculators/solar_return.py`

**Algorithm**:

```python
import swisseph as swe
from datetime import datetime

def calculate_solar_return(
    birth_date: date,
    birth_time: time,
    birth_location: Location,
    target_year: int
) -> dict:
    """
    Calculate Solar Return chart for a given year.
    
    Solar Return occurs when the Sun returns to its exact natal position.
    This happens within ~24 hours of the birthday each year.
    """
    # Get natal Sun position
    birth_dt = datetime.combine(birth_date, birth_time)
    natal_jd = swe.julday(
        birth_dt.year, birth_dt.month, birth_dt.day,
        birth_dt.hour + birth_dt.minute / 60.0
    )
    natal_sun = swe.calc_ut(natal_jd, swe.SUN)[0][0]  # Longitude
    
    # Find exact moment Sun returns to natal position in target year
    # Start searching from birthday in target year
    search_start = datetime(target_year, birth_date.month, birth_date.day)
    solar_return_jd = find_solar_return_moment(natal_sun, search_start)
    
    # Calculate house cusps for solar return moment
    houses = swe.houses(
        solar_return_jd,
        birth_location.latitude,
        birth_location.longitude,
        b'P'  # Placidus house system
    )
    
    # Get all planetary positions at solar return
    planets = calculate_all_planets(solar_return_jd)
    
    # Determine house placements
    house_placements = assign_planets_to_houses(planets, houses)
    
    return {
        "solar_return_datetime": jd_to_datetime(solar_return_jd),
        "houses": houses,
        "planets": planets,
        "house_placements": house_placements,
        "ascendant": houses[0][0],
        "midheaven": houses[0][9],
    }


def get_daily_house_focus(
    solar_return_data: dict,
    target_date: date,
    birth_date: date
) -> int:
    """
    Determine which house is emphasized on a given day.
    
    Uses profection method: Each day after solar return activates
    houses in sequence, completing the cycle over the year.
    """
    sr_date = solar_return_data["solar_return_datetime"].date()
    days_since_sr = (target_date - sr_date).days
    
    # 12 houses over ~365 days = ~30.4 days per house
    house_number = (days_since_sr // 30) % 12 + 1
    return house_number
```

**Data Model**:

```python
class SolarTransitData(BaseModel):
    """Solar return and transit data for a specific day."""
    sun_sign: str                 # Current zodiac sign of Sun
    house_focus: int              # 1-12 based on Solar Return
    house_theme: str              # "Self & Identity", "Resources", etc.
    planetary_aspects: List[str]  # Active aspects for the day
    transit_message: str          # Interpretive guidance
```

### 5.5 Human Design Calculator

**File**: `src/skyforge/calculators/human_design.py`

**Algorithm**:

Human Design maps planetary positions to 64 Gates (derived from I Ching hexagrams). Each gate corresponds to a specific degree range in the zodiac.

```python
# Gate to zodiac degree mapping (simplified - full data in gates_hexagrams.json)
# Each gate spans 5.625 degrees (360° / 64 gates)
GATE_DEGREE_MAP = {
    1: (13.875, 19.5),    # Gate 1: Leo 13°52'30" - 19°30'
    2: (73.875, 79.5),    # Gate 2: Gemini 13°52'30" - 19°30'
    # ... all 64 gates
}

def get_gate_from_longitude(longitude: float) -> int:
    """Convert zodiac longitude to Human Design gate number."""
    # Gates are arranged in a specific sequence around the wheel
    # This requires the full gate sequence data
    pass


def calculate_human_design_transits(target_date: datetime) -> dict:
    """
    Calculate which gates are activated by planetary transits.
    
    Each planet activates a gate based on its zodiac position.
    """
    jd = datetime_to_jd(target_date)
    
    planets = [
        (swe.SUN, "Sun"),
        (swe.EARTH, "Earth"),  # Opposite Sun
        (swe.MOON, "Moon"),
        (swe.MERCURY, "Mercury"),
        (swe.VENUS, "Venus"),
        (swe.MARS, "Mars"),
        (swe.JUPITER, "Jupiter"),
        (swe.SATURN, "Saturn"),
        (swe.URANUS, "Uranus"),
        (swe.NEPTUNE, "Neptune"),
        (swe.PLUTO, "Pluto"),
    ]
    
    active_gates = []
    for planet_id, planet_name in planets:
        pos = swe.calc_ut(jd, planet_id)[0][0]
        gate = get_gate_from_longitude(pos)
        line = get_line_from_longitude(pos)  # 1-6
        
        active_gates.append({
            "gate_number": gate,
            "line": line,
            "planet": planet_name,
            "gate_name": GATE_NAMES[gate],
            "theme": GATE_THEMES[gate],
        })
    
    return {"active_gates": active_gates}


def get_user_design(birth_data: BirthData) -> dict:
    """
    Calculate user's fixed Human Design chart.
    
    Requires:
    - Personality (conscious): Planetary positions at birth
    - Design (unconscious): Planetary positions ~88 days before birth
    """
    # Personality calculation (birth moment)
    birth_dt = datetime.combine(birth_data.date, birth_data.get_effective_time())
    personality_gates = calculate_gates_for_datetime(birth_dt)
    
    # Design calculation (88 degrees of solar arc before birth ≈ 88 days)
    design_dt = birth_dt - timedelta(days=88)
    design_gates = calculate_gates_for_datetime(design_dt)
    
    # Determine Type, Strategy, Authority based on defined centers
    defined_centers = calculate_defined_centers(personality_gates, design_gates)
    hd_type = determine_type(defined_centers)
    strategy = TYPE_STRATEGIES[hd_type]
    authority = determine_authority(defined_centers)
    
    return {
        "type": hd_type,
        "strategy": strategy,
        "authority": authority,
        "personality_gates": personality_gates,
        "design_gates": design_gates,
        "defined_centers": defined_centers,
    }
```

**Data Model**:

```python
class GateData(BaseModel):
    """Single gate activation data."""
    gate_number: int              # 1-64
    gate_name: str                # "The Creative", "The Receptive", etc.
    line: int                     # 1-6
    planet: str                   # "Sun", "Moon", etc.
    theme: str                    # Brief interpretation


class HumanDesignData(BaseModel):
    """Human Design data for a specific day."""
    # User's fixed design
    type: str                     # "Generator", "Projector", etc.
    strategy: str                 # "Wait to respond", etc.
    authority: str                # "Sacral", "Emotional", etc.
    
    # Daily transits
    active_gates: List[GateData]
    active_channels: List[str]    # When two gates form a channel
    defined_centers_today: List[str]
    
    # Decision guidance
    decision_cue: str
    energy_management: str
    signature_theme: str          # "Satisfaction", "Success", etc.
    not_self_warning: str         # What to watch for
```

### 5.6 I Ching Calculator

**File**: `src/skyforge/calculators/i_ching.py`

The I Ching integration derives from Human Design gates (which are based on the 64 hexagrams).

```python
# Each HD gate corresponds to an I Ching hexagram
GATE_TO_HEXAGRAM = {
    1: 1,   # Gate 1 = Hexagram 1 (The Creative)
    2: 2,   # Gate 2 = Hexagram 2 (The Receptive)
    # ... mapping for all 64
}

HEXAGRAM_DATA = {
    1: {
        "name": "The Creative",
        "chinese": "乾 (Qián)",
        "trigram_above": "Heaven",
        "trigram_below": "Heaven",
        "judgment": "The Creative works sublime success...",
        "image": "The movement of heaven is full of power...",
        "keywords": ["strength", "initiative", "creativity"],
    },
    # ... all 64 hexagrams
}


def get_daily_hexagram(human_design_data: HumanDesignData) -> dict:
    """
    Determine the primary I Ching hexagram for the day.
    
    Uses the Sun gate as the primary hexagram, with Moon gate
    as secondary influence.
    """
    sun_gate = next(
        (g for g in human_design_data.active_gates if g.planet == "Sun"),
        None
    )
    
    if sun_gate:
        hexagram_num = GATE_TO_HEXAGRAM[sun_gate.gate_number]
        hexagram = HEXAGRAM_DATA[hexagram_num]
        
        return {
            "hexagram_number": hexagram_num,
            "hexagram_name": hexagram["name"],
            "trigram_above": hexagram["trigram_above"],
            "trigram_below": hexagram["trigram_below"],
            "judgment": hexagram["judgment"],
            "image": hexagram["image"],
            "changing_lines": [sun_gate.line],
            "daily_wisdom": generate_daily_wisdom(hexagram, sun_gate.line),
            "action_guidance": generate_action_guidance(hexagram),
            "caution": generate_caution(hexagram),
        }
```

**Data Model**:

```python
class IChingData(BaseModel):
    """I Ching hexagram data for a specific day."""
    hexagram_number: int          # 1-64
    hexagram_name: str
    trigram_above: str
    trigram_below: str
    
    # Wisdom
    judgment: str
    image: str
    changing_lines: List[int]     # Active lines (1-6)
    moving_to: Optional[int] = None  # Resulting hexagram
    
    # Daily application
    daily_wisdom: str
    action_guidance: str
    caution: str
```

### 5.7 Risk Analysis

**File**: `src/skyforge/analyzers/risk.py`

```python
def calculate_risk_analysis(
    moon_data: MoonData,
    biorhythm_data: BiorhythmData,
    numerology_data: NumerologyData,
    human_design_data: HumanDesignData,
) -> RiskAnalysisData:
    """
    Calculate multi-domain risk scores.
    
    Risk factors:
    - Moon Void of Course: +3 to spiritual/emotional risk
    - Biorhythm critical days: +4 to relevant domain
    - Biorhythm low (<-50): +2 to relevant domain
    - Challenging numerology day: +2 to emotional risk
    - Not-self theme active: +2 to spiritual risk
    """
    spiritual_risk = 0
    emotional_risk = 0
    physical_risk = 0
    warnings = []
    
    # Moon VOC check
    if moon_data.moon_void_of_course:
        spiritual_risk += 3
        emotional_risk += 3
        warnings.append(RiskWarning(
            domain="Spiritual",
            source="Moon Void of Course",
            message="Avoid initiating new projects or making major decisions",
            severity="Caution"
        ))
    
    # Biorhythm checks
    if biorhythm_data.physical_critical:
        physical_risk += 4
        warnings.append(RiskWarning(
            domain="Physical",
            source="Biorhythm Critical Day",
            message="Take extra care with physical activities",
            severity="Warning"
        ))
    
    if biorhythm_data.physical < -50:
        physical_risk += 2
    
    if biorhythm_data.emotional_critical:
        emotional_risk += 4
        warnings.append(RiskWarning(
            domain="Emotional",
            source="Biorhythm Critical Day",
            message="Emotions may be unstable; practice self-care",
            severity="Warning"
        ))
    
    if biorhythm_data.emotional < -50:
        emotional_risk += 2
    
    if biorhythm_data.intellectual_critical:
        spiritual_risk += 2  # Mental clarity affects spiritual clarity
    
    # Calculate overall
    total_risk = (spiritual_risk + emotional_risk + physical_risk) / 3
    risk_score = min(total_risk * 10, 100)  # Scale to 0-100
    
    if risk_score < 25:
        overall_level = "Low"
    elif risk_score < 50:
        overall_level = "Moderate"
    elif risk_score < 75:
        overall_level = "Elevated"
    else:
        overall_level = "High"
    
    return RiskAnalysisData(
        spiritual_risk=min(spiritual_risk, 10),
        emotional_risk=min(emotional_risk, 10),
        physical_risk=min(physical_risk, 10),
        overall_risk_level=overall_level,
        risk_score=risk_score,
        warnings=warnings,
        protective_practices=get_protective_practices(warnings),
        grounding_techniques=get_grounding_techniques(overall_level),
    )
```

**Data Model**:

```python
class RiskWarning(BaseModel):
    """Individual risk warning."""
    domain: str                   # "Spiritual", "Emotional", "Physical"
    source: str                   # What triggered the warning
    message: str                  # Advice
    severity: str                 # "Caution", "Warning", "Alert"


class RiskAnalysisData(BaseModel):
    """Complete risk analysis for a day."""
    spiritual_risk: int           # 1-10
    emotional_risk: int           # 1-10
    physical_risk: int            # 1-10
    
    overall_risk_level: str       # "Low", "Moderate", "Elevated", "High"
    risk_score: float             # 0-100
    
    warnings: List[RiskWarning]
    protective_practices: List[str]
    grounding_techniques: List[str]
```

### 5.8 Wellness Analyzer

**File**: `src/skyforge/analyzers/wellness.py`

```python
def generate_exercise_recommendation(
    biorhythm_data: BiorhythmData,
    moon_data: MoonData,
) -> ExerciseRecommendation:
    """
    Generate exercise recommendations based on biorhythm and moon.
    
    Rules:
    - Physical biorhythm high (>50): Strength training, high intensity
    - Physical biorhythm low (<-50): Gentle yoga, stretching, rest
    - Physical critical: Light movement only
    - Earth moon sign: Grounding exercises, hiking
    - Fire moon sign: High energy cardio
    - Water moon sign: Swimming, flow yoga
    - Air moon sign: Dance, varied movement
    """
    physical = biorhythm_data.physical
    element = moon_data.sign_element
    
    if biorhythm_data.physical_critical:
        return ExerciseRecommendation(
            exercise_type="Rest/Gentle Movement",
            intensity="Recovery",
            optimal_time="Anytime - listen to body",
            duration_minutes=20,
            specific_activities=["Gentle stretching", "Short walk", "Restorative yoga"],
            avoid_today=["High intensity", "Heavy lifting", "Competitive sports"],
            rationale="Physical biorhythm at critical point - prioritize recovery"
        )
    
    if physical > 50:
        base_type = "Strength Training" if physical > 70 else "Moderate Cardio"
        intensity = "High" if physical > 70 else "Moderate"
        duration = 45 if physical > 70 else 30
    elif physical < -50:
        base_type = "Yoga/Stretching"
        intensity = "Low"
        duration = 20
    else:
        base_type = "Balanced Workout"
        intensity = "Moderate"
        duration = 30
    
    # Modify based on moon element
    element_activities = {
        "Fire": ["HIIT", "Running", "Power yoga"],
        "Earth": ["Weight training", "Hiking", "Pilates"],
        "Air": ["Dance", "Cycling", "Varied circuit"],
        "Water": ["Swimming", "Flow yoga", "Tai chi"],
    }
    
    return ExerciseRecommendation(
        exercise_type=base_type,
        intensity=intensity,
        optimal_time="Morning" if physical > 0 else "Evening",
        duration_minutes=duration,
        specific_activities=element_activities.get(element, []),
        avoid_today=get_avoid_activities(physical, element),
        rationale=f"Physical biorhythm at {physical:.0f}%, {element} moon energy"
    )


def generate_nourishment_guidance(
    moon_data: MoonData,
    biorhythm_data: BiorhythmData,
) -> NourishmentGuidance:
    """
    Generate dietary guidance based on moon element and biorhythm.
    
    Element-based eating:
    - Fire: Light, cooling foods; avoid heavy/spicy
    - Earth: Grounding root vegetables, whole grains
    - Air: Variety, light meals, good hydration
    - Water: Warming foods, soups, comfort foods
    """
    element = moon_data.sign_element
    
    element_guidance = {
        "Fire": {
            "focus": "Cooling and light",
            "emphasized": ["Fresh salads", "Fruits", "Cooling herbs (mint, cilantro)"],
            "minimize": ["Heavy meats", "Spicy foods", "Alcohol"],
            "hydration": "Extra water and cooling beverages",
        },
        "Earth": {
            "focus": "Grounding and nourishing",
            "emphasized": ["Root vegetables", "Whole grains", "Legumes"],
            "minimize": ["Processed foods", "Excessive sugar"],
            "hydration": "Warm herbal teas, room temperature water",
        },
        "Air": {
            "focus": "Light and varied",
            "emphasized": ["Variety of vegetables", "Light proteins", "Seeds/nuts"],
            "minimize": ["Heavy, dense foods", "Large portions"],
            "hydration": "Consistent hydration throughout day",
        },
        "Water": {
            "focus": "Warming and comforting",
            "emphasized": ["Soups", "Stews", "Warming spices (ginger, cinnamon)"],
            "minimize": ["Cold foods", "Raw foods", "Excessive dairy"],
            "hydration": "Warm water, herbal teas",
        },
    }
    
    guidance = element_guidance.get(element, element_guidance["Earth"])
    
    return NourishmentGuidance(
        element_focus=guidance["focus"],
        foods_emphasized=guidance["emphasized"],
        foods_minimize=guidance["minimize"],
        hydration_focus=guidance["hydration"],
        meal_timing="Earlier dinner recommended" if biorhythm_data.physical < 0 else "Normal timing",
        breakfast_suggestion=generate_meal_suggestion("breakfast", element),
        lunch_suggestion=generate_meal_suggestion("lunch", element),
        dinner_suggestion=generate_meal_suggestion("dinner", element),
        snack_suggestions=generate_snack_suggestions(element),
    )
```

### 5.9 Spiritual Reading Selector

**File**: `src/skyforge/analyzers/spiritual.py`

```python
def select_spiritual_reading(
    moon_data: MoonData,
    numerology_data: NumerologyData,
    i_ching_data: IChingData,
    day_of_year: int,
) -> SpiritualReading:
    """
    Select appropriate spiritual reading based on daily energies.
    
    Rotation logic:
    - Tao Te Ching: Earth days, introspective numerology
    - Marcus Aurelius: Fire days, action-oriented numerology
    - Rumi: Water days, emotional themes
    - Dhammapada: Air days, mental clarity themes
    - Rotate through others based on day_of_year
    """
    element = moon_data.sign_element
    personal_day = numerology_data.personal_day
    
    # Primary source selection based on element
    source_map = {
        "Earth": ("tao_te_ching", "Taoist"),
        "Fire": ("meditations_aurelius", "Stoic"),
        "Water": ("rumi_poetry", "Sufi"),
        "Air": ("dhammapada", "Buddhist"),
    }
    
    source_file, tradition = source_map.get(element, ("wisdom_quotes", "Universal"))
    
    # Load source data
    source_data = load_spiritual_source(source_file)
    
    # Select specific passage based on day_of_year and themes
    themes = get_daily_themes(i_ching_data, numerology_data)
    passage = select_matching_passage(source_data, themes, day_of_year)
    
    return SpiritualReading(
        source_type=passage["type"],
        tradition=tradition,
        source_title=passage["title"],
        source_author=passage["author"],
        chapter_or_verse=passage["reference"],
        reading_text=passage["text"],
        daily_relevance=generate_relevance(passage, themes),
        contemplation_question=generate_contemplation(passage, themes),
        embodiment_practice=generate_embodiment(passage, element),
    )
```

---

## 6. API & CLI Specifications

### 6.1 CLI Commands

**File**: `src/skyforge/cli.py`

```python
import click
from rich.console import Console

console = Console()


@click.group()
@click.version_option()
def cli():
    """SkyForge - Sovereign Alignment Calendar Generator"""
    pass


@cli.command()
@click.option("--year", "-y", required=True, type=int, help="Target year")
@click.option("--profile", "-p", default="default", help="Profile name")
@click.option("--month", "-m", type=int, help="Generate single month only")
@click.option("--format", "-f", multiple=True, default=["json"], 
              type=click.Choice(["json", "pdf", "excel", "csv"]))
@click.option("--output", "-o", type=click.Path(), help="Output directory")
def generate(year, profile, month, format, output):
    """Generate sovereign alignment calendar."""
    console.print(f"[bold green]Generating {year} calendar for profile: {profile}[/]")
    # Implementation


@cli.group()
def profile():
    """Manage user profiles."""
    pass


@profile.command("create")
@click.option("--name", "-n", required=True, help="Profile name")
@click.option("--birth-date", "-d", required=True, help="Birth date (YYYY-MM-DD)")
@click.option("--birth-time", "-t", help="Birth time (HH:MM)")
@click.option("--birth-time-range", type=click.Choice([
    "exact", "morning", "afternoon", "evening", "night", "unknown"
]), default="unknown")
@click.option("--birth-location", "-l", help="Birth location (city, state/country)")
def profile_create(name, birth_date, birth_time, birth_time_range, birth_location):
    """Create a new user profile."""
    # Implementation


@profile.command("list")
def profile_list():
    """List all profiles."""
    # Implementation


@profile.command("show")
@click.argument("name")
def profile_show(name):
    """Show profile details."""
    # Implementation


@cli.command()
@click.option("--date", "-d", required=True, help="Date to preview (YYYY-MM-DD)")
@click.option("--profile", "-p", default="default", help="Profile name")
def preview(date, profile):
    """Preview a single day's alignment."""
    # Implementation


if __name__ == "__main__":
    cli()
```

### 6.2 Web API Endpoints

**File**: `src/skyforge/web/app.py`

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI(
    title="SkyForge API",
    description="Sovereign Alignment Calendar API",
    version="1.0.0"
)


@app.get("/api/v1/calendar/{year}")
async def get_calendar(
    year: int,
    profile: str = "default",
    month: int = None,
    format: str = "json"
):
    """Generate and return calendar data."""
    pass


@app.get("/api/v1/day/{date}")
async def get_day(date: str, profile: str = "default"):
    """Get single day alignment data."""
    pass


@app.get("/api/v1/profiles")
async def list_profiles():
    """List all available profiles."""
    pass


@app.get("/api/v1/profiles/{name}")
async def get_profile(name: str):
    """Get profile details."""
    pass


@app.post("/api/v1/profiles")
async def create_profile(profile: UserProfile):
    """Create a new profile."""
    pass


@app.get("/api/v1/download/{filename}")
async def download_file(filename: str):
    """Download generated calendar file."""
    pass
```

---

## 7. Output Generation

### 7.1 Daily Entry Generator

**File**: `src/skyforge/generators/daily_entry.py`

```python
def generate_daily_entry(
    target_date: date,
    profile: UserProfile,
    solar_return_data: dict,
) -> DailyPreparation:
    """
    Generate complete daily preparation entry.
    
    Orchestrates all calculators and analyzers to produce
    the full daily sovereign alignment guide.
    """
    # 1. Calculate all domain data
    moon_data = calculate_moon_data(target_date)
    numerology_data = calculate_numerology(profile.birth_data, target_date)
    biorhythm_data = calculate_biorhythm(profile.birth_data.date, target_date)
    solar_transit = calculate_solar_transit(solar_return_data, target_date)
    human_design = calculate_human_design_transits(target_date, profile)
    i_ching = get_daily_hexagram(human_design)
    
    # 2. Run analyzers
    risk_analysis = calculate_risk_analysis(
        moon_data, biorhythm_data, numerology_data, human_design
    )
    exercise = generate_exercise_recommendation(biorhythm_data, moon_data)
    nourishment = generate_nourishment_guidance(moon_data, biorhythm_data)
    
    # 3. Generate practices
    morning_ritual = generate_morning_ritual(moon_data, numerology_data)
    meditation = generate_meditation_practice(moon_data, i_ching)
    journaling = generate_journaling_prompts(i_ching, numerology_data)
    spiritual_reading = select_spiritual_reading(
        moon_data, numerology_data, i_ching, target_date.timetuple().tm_yday
    )
    evening_ritual = generate_evening_ritual(biorhythm_data, moon_data)
    
    # 4. Synthesize
    daily_theme = synthesize_daily_theme(
        moon_data, numerology_data, i_ching, human_design
    )
    power_hours = calculate_power_hours(biorhythm_data, moon_data)
    caution_periods = calculate_caution_periods(moon_data, biorhythm_data)
    
    return DailyPreparation(
        date=target_date,
        day_of_week=target_date.strftime("%A"),
        day_of_year=target_date.timetuple().tm_yday,
        moon=moon_data,
        solar_transit=solar_transit,
        numerology=numerology_data,
        human_design=human_design,
        i_ching=i_ching,
        biorhythm=biorhythm_data,
        risk_analysis=risk_analysis,
        morning_ritual=morning_ritual,
        exercise=exercise,
        nourishment=nourishment,
        meditation=meditation,
        journaling=journaling,
        spiritual_reading=spiritual_reading,
        evening_ritual=evening_ritual,
        daily_theme=daily_theme["theme"],
        theme_keywords=daily_theme["keywords"],
        power_hours=power_hours,
        caution_periods=caution_periods,
        affirmation=generate_affirmation(daily_theme),
        daily_mantra=generate_mantra(i_ching),
        closing_reflection=generate_closing_reflection(daily_theme),
        tomorrow_preview=generate_tomorrow_preview(target_date, profile),
    )
```

### 7.2 PDF Export

**File**: `src/skyforge/generators/pdf_export.py`

Uses ReportLab to generate formatted PDF calendars with:
- Daily pages with all 10 domains
- Monthly overview pages
- Table of contents
- Cover page with user profile summary

### 7.3 Excel Export

**File**: `src/skyforge/generators/excel_export.py`

Uses OpenPyXL to generate spreadsheets with:
- One row per day
- Columns for each data field
- Conditional formatting for risk levels
- Charts for biorhythm curves

---

## 8. Testing Requirements

### 8.1 Test Structure

```
tests/
├── conftest.py                 # Shared fixtures
├── test_calculators/
│   ├── test_moon.py           # Moon phase calculations
│   ├── test_numerology.py     # Numerology algorithms
│   ├── test_biorhythm.py      # Biorhythm formulas
│   ├── test_human_design.py   # HD gate calculations
│   └── test_i_ching.py        # Hexagram mappings
├── test_analyzers/
│   ├── test_risk.py           # Risk scoring
│   └── test_wellness.py       # Recommendations
├── test_generators/
│   ├── test_daily_entry.py    # Full day generation
│   └── test_exports.py        # PDF/Excel output
└── test_integration.py        # End-to-end tests
```

### 8.2 Test Requirements

Each module must have tests covering:

1. **Expected use case** - Normal operation with valid inputs
2. **Edge cases** - Boundary conditions, special dates
3. **Failure cases** - Invalid inputs, error handling

### 8.3 Example Test

```python
# tests/test_calculators/test_numerology.py

import pytest
from datetime import date
from skyforge.calculators.numerology import (
    calculate_life_path,
    calculate_personal_year,
    calculate_personal_day,
    reduce_to_single_digit,
)


class TestReduceToSingleDigit:
    """Tests for digit reduction algorithm."""
    
    def test_single_digit_unchanged(self):
        """Single digits should remain unchanged."""
        assert reduce_to_single_digit(5) == 5
    
    def test_double_digit_reduced(self):
        """Double digits should reduce to single."""
        assert reduce_to_single_digit(14) == 5  # 1+4=5
    
    def test_master_number_preserved(self):
        """Master numbers 11, 22, 33 should be preserved."""
        assert reduce_to_single_digit(11, keep_master=True) == 11
        assert reduce_to_single_digit(22, keep_master=True) == 22
        assert reduce_to_single_digit(33, keep_master=True) == 33
    
    def test_master_number_reduced_when_disabled(self):
        """Master numbers should reduce when keep_master=False."""
        assert reduce_to_single_digit(11, keep_master=False) == 2


class TestLifePath:
    """Tests for Life Path calculation."""
    
    def test_known_life_path(self):
        """Test with known birth date and expected result."""
        # March 15, 1985 → Life Path 5
        birth = date(1985, 3, 15)
        assert calculate_life_path(birth) == 5
    
    def test_master_number_life_path(self):
        """Test birth date that produces master number."""
        # November 29, 1990 → 11+29+1990 → 11+11+19 → 11+11+1 → 23 → 5
        # Actually need to find a real master number date
        pass
    
    def test_leap_year_birth(self):
        """Test birth on Feb 29."""
        birth = date(2000, 2, 29)
        result = calculate_life_path(birth)
        assert 1 <= result <= 33


class TestPersonalDay:
    """Tests for Personal Day calculation."""
    
    def test_personal_day_range(self):
        """Personal day should be 1-9 or master number."""
        birth = date(1985, 3, 15)
        target = date(2026, 1, 15)
        personal_year = calculate_personal_year(birth, 2026)
        personal_month = (personal_year + 1) % 9 or 9
        result = calculate_personal_day(personal_month, 15)
        assert 1 <= result <= 33
```

### 8.4 Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=skyforge tests/

# Run specific test file
pytest tests/test_calculators/test_numerology.py

# Run with verbose output
pytest -v tests/
```

---

## 9. Code Style & Conventions

### 9.1 General Guidelines

- **Python Version**: 3.10+
- **Style Guide**: PEP 8
- **Formatter**: Black (line length 88)
- **Linter**: Ruff or Flake8
- **Type Hints**: Required for all functions

### 9.2 Docstrings

Use Google-style docstrings:

```python
def calculate_biorhythm(birth_date: date, target_date: date) -> dict:
    """
    Calculate biorhythm values for a given date.
    
    Uses sinusoidal functions with standard cycle lengths:
    - Physical: 23 days
    - Emotional: 28 days
    - Intellectual: 33 days
    
    Args:
        birth_date: User's date of birth.
        target_date: Date to calculate biorhythm for.
    
    Returns:
        Dictionary containing:
            - physical: float (-100 to 100)
            - emotional: float (-100 to 100)
            - intellectual: float (-100 to 100)
            - days_alive: int
    
    Raises:
        ValueError: If target_date is before birth_date.
    
    Example:
        >>> calculate_biorhythm(date(1985, 3, 15), date(2026, 1, 15))
        {'physical': 67.2, 'emotional': 23.1, 'intellectual': -12.4, 'days_alive': 14916}
    """
```

### 9.3 Import Order

```python
# Standard library
import math
from datetime import date, datetime, time
from typing import Dict, List, Optional

# Third-party
import swisseph as swe
from pydantic import BaseModel, Field

# Local
from skyforge.models import BirthData, Location
from skyforge.calculators.ephemeris import datetime_to_jd
```

### 9.4 Naming Conventions

- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

### 9.5 Error Handling

```python
class SkyForgeError(Exception):
    """Base exception for SkyForge."""
    pass


class ProfileNotFoundError(SkyForgeError):
    """Raised when a profile cannot be found."""
    pass


class CalculationError(SkyForgeError):
    """Raised when a calculation fails."""
    pass


# Usage
def load_profile(name: str) -> UserProfile:
    """Load a user profile by name."""
    profile_path = PROFILES_DIR / f"{name}.yaml"
    if not profile_path.exists():
        raise ProfileNotFoundError(f"Profile not found: {name}")
    # ...
```

---

## 10. Security & Data Privacy

### 10.1 Sensitive Data Handling

- **Birth Data**: Store locally only, never transmit to external services
- **API Keys**: Use environment variables, never commit to repository
- **Output Files**: Store in user-specified directory with appropriate permissions

### 10.2 Environment Variables

```python
# src/skyforge/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings from environment."""
    
    geocoding_api_key: str = ""
    output_dir: str = "./output"
    default_profile: str = "default"
    swisseph_path: str = "./ephe"
    
    class Config:
        env_prefix = "SKYFORGE_"
        env_file = ".env"
```

### 10.3 Input Validation

All user inputs are validated through Pydantic models before processing.

---

## 11. Reference Data

### 11.1 Data Files Location

All reference data is stored in `src/skyforge/data/`:

- `gates_hexagrams.json` - Human Design gates to I Ching mapping
- `zodiac_signs.json` - Sign characteristics and correspondences
- `moon_phases.json` - Phase interpretations and activities
- `numerology_meanings.json` - Number interpretations
- `wellness_rules.json` - Exercise and nourishment rules
- `spiritual_library/` - Curated wisdom texts

### 11.2 Zodiac Signs Reference

```json
{
  "aries": {
    "element": "Fire",
    "modality": "Cardinal",
    "ruler": "Mars",
    "keywords": ["initiative", "courage", "action"],
    "body_part": "head",
    "optimal_activities": ["starting projects", "physical activity", "competition"],
    "avoid_activities": ["detailed planning", "patience-required tasks"]
  }
}
```

### 11.3 Human Design Types

| Type | Population | Strategy | Signature | Not-Self |
|------|------------|----------|-----------|----------|
| Generator | 37% | Wait to respond | Satisfaction | Frustration |
| Manifesting Generator | 33% | Wait to respond, then inform | Satisfaction | Frustration/Anger |
| Projector | 20% | Wait for invitation | Success | Bitterness |
| Manifestor | 9% | Inform before acting | Peace | Anger |
| Reflector | 1% | Wait lunar cycle | Surprise | Disappointment |

### 11.4 Numerology Meanings

| Number | Theme | Energy | Keywords |
|--------|-------|--------|----------|
| 1 | New Beginnings | Active | Independence, leadership, initiative |
| 2 | Partnership | Receptive | Cooperation, balance, diplomacy |
| 3 | Expression | Creative | Communication, joy, creativity |
| 4 | Foundation | Stable | Structure, discipline, hard work |
| 5 | Change | Dynamic | Freedom, adventure, versatility |
| 6 | Responsibility | Nurturing | Home, family, service |
| 7 | Introspection | Spiritual | Analysis, wisdom, solitude |
| 8 | Abundance | Material | Power, success, manifestation |
| 9 | Completion | Universal | Humanitarianism, endings, wisdom |
| 11 | Illumination | Master | Intuition, inspiration, idealism |
| 22 | Master Builder | Master | Vision, practical idealism |
| 33 | Master Teacher | Master | Compassion, healing, guidance |

---

## Appendix: Sample Daily Output

```
╔══════════════════════════════════════════════════════════════════╗
║  SKYFORGE DAILY SOVEREIGN ALIGNMENT                              ║
║  Wednesday, January 15, 2026 (Day 15 of 365)                     ║
╠══════════════════════════════════════════════════════════════════╣
║  DAILY THEME: "Grounded Action with Emotional Wisdom"            ║
║  OVERALL ENERGY: Moderate-High | RISK LEVEL: Low                 ║
╚══════════════════════════════════════════════════════════════════╝

🌙 MOON: Waxing Gibbous (78%) in Taurus
   Element: Earth | Modality: Fixed
   Energy: Steady, sensual, focused on material security
   Optimal: Financial planning, nature walks, comfort foods
   Avoid: Rushing, sudden changes, skipping meals

🔢 NUMEROLOGY: Personal Day 5 (Universal Day 7)
   Theme: Change meets introspection
   Favorable: Adaptability, short trips, variety
   Challenge: Restlessness, scattered energy

☀️ SOLAR TRANSIT: Sun in Capricorn, 10th House Focus
   Theme: Career, public image, achievement
   Message: Practical steps toward long-term goals rewarded

🧬 HUMAN DESIGN: Gate 41 (Decrease) Active
   Strategy: Wait to respond
   Decision Cue: Trust gut feelings about opportunities
   Energy: Initiating energy for new experiences

☯️ I CHING: Hexagram 41 - Decrease
   Wisdom: "Decrease below, increase above"
   Action: Simplify to create space for growth
   Caution: Don't cling to what no longer serves

📊 BIORHYTHM:
   Physical: +67% (Peak) | Emotional: +23% (Rising) | Mental: -12% (Low)
   Best For: Physical activity, practical tasks
   Challenging: Complex analysis, detailed work

⚠️ RISK ANALYSIS: Low (Score: 22/100)
   No critical periods today
   Protective Practice: Morning grounding meditation

═══════════════════════════════════════════════════════════════════
                    DAILY PRACTICES FOR OPTIMAL PERFORMANCE
═══════════════════════════════════════════════════════════════════

🌅 MORNING RITUAL (6:30 AM suggested wake)
   • 5-min breathwork: 4-7-8 breathing pattern
   • Intention: "I move with steady purpose today"
   • Movement: 15-min stretching or yoga

💪 EXERCISE: Strength Training (Moderate-High Intensity)
   Time: Morning (7-9 AM) - Physical biorhythm peak
   Duration: 45 minutes
   Focus: Lower body, grounding exercises
   Avoid: High-impact cardio (save energy for mental afternoon)

🥗 NOURISHMENT (Earth Element Day):
   Breakfast: Warm oatmeal with nuts, root vegetable hash
   Lunch: Hearty grain bowl with roasted vegetables
   Dinner: Light - soup and salad (earlier, by 7 PM)
   Hydration: Warm herbal teas, room temperature water
   Minimize: Excessive caffeine, cold foods

🧘 MEDITATION: Body Scan Practice
   Time: Midday (12:00-12:20 PM)
   Duration: 20 minutes
   Focus: Grounding into physical sensations
   Mantra: "I am rooted and secure"

📝 JOURNALING:
   Morning: "What practical step can I take today toward my goals?"
   Evening: "Where did I experience stability and security today?"
   Deep Inquiry: "What am I ready to release to create space for growth?"

📖 SPIRITUAL READING: Tao Te Ching, Chapter 22 (Taoist)
   ┌─────────────────────────────────────────────────────────────┐
   │  "Yield and overcome;                                       │
   │   Bend and be straight;                                     │
   │   Empty and be full;                                        │
   │   Wear out and be new;                                      │
   │   Have little and gain;                                     │
   │   Have much and be confused."                               │
   │                                          — Lao Tzu          │
   └─────────────────────────────────────────────────────────────┘
   Daily Relevance: Aligns with today's I Ching theme of "Decrease" -
   letting go creates space for what truly matters.
   
   Contemplation: "Where in my life am I holding on too tightly?"
   
   Embodiment: Practice releasing tension in body during meditation;
   physically let go of one item you no longer need today.

🌙 EVENING RITUAL (Begin 8:30 PM):
   • Screen cutoff: 9:00 PM
   • Reflection: Review accomplishments, no matter how small
   • Sleep prep: Warm bath, lavender, gratitude list
   • Optimal sleep: 10:30 PM

═══════════════════════════════════════════════════════════════════

⚡ POWER HOURS:
   • 7:00-10:00 AM - Physical tasks, exercise, practical work
   • 4:00-6:00 PM - Creative projects, artistic expression

⏸️ CAUTION PERIODS:
   • 1:00-3:00 PM - Mental biorhythm low, avoid complex decisions
   
💫 TODAY'S AFFIRMATION:
   "I build my dreams with patient, steady hands."

🔮 TOMORROW PREVIEW:
   Moon enters Gemini - shift to mental agility and communication
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-02 | Initial agent.md creation |

---

*This document is maintained as the authoritative guide for AI coding agents working on the SkyForge project. Update this file when making significant architectural changes or adding new features.*
