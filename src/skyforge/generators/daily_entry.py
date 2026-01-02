"""
Daily entry generator for SkyForge.

Orchestrates all calculators and analyzers to produce complete
daily sovereign alignment guides.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from datetime import date
from typing import List

from ..models import (
    UserProfile,
    DailyPreparation,
    MoonData,
    NumerologyData,
    SolarTransitData,
    HumanDesignData,
    GateData,
    IChingData,
    BiorhythmData,
    RiskAnalysisData,
    PowerHour,
    CautionPeriod,
    SpiritualReading,
)
from ..calculators import (
    calculate_moon_data,
    calculate_numerology_for_day,
    calculate_biorhythm_for_day,
    calculate_life_path,
)
from ..analyzers import (
    calculate_risk_analysis,
    generate_exercise_recommendation,
    generate_nourishment_guidance,
    generate_morning_ritual,
    generate_meditation_practice,
    generate_evening_ritual,
    generate_journaling_prompts,
)


def generate_solar_transit(target_date: date, profile: UserProfile) -> SolarTransitData:
    """
    Generate solar transit data for a day.
    
    This is a simplified version. Full implementation would use
    Swiss Ephemeris for accurate solar return calculations.
    
    Args:
        target_date: Date to calculate for.
        profile: User profile with birth data.
    
    Returns:
        SolarTransitData: Solar transit information.
    """
    from ..calculators.moon import ZODIAC_SIGNS, SIGN_ELEMENTS
    
    # Simple sun sign calculation based on date
    # This is approximate; production would use ephemeris
    month = target_date.month
    day = target_date.day
    
    sun_signs = [
        (1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 20, "Pisces"),
        (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"),
        (7, 22, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"),
        (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"),
    ]
    
    sun_sign = "Capricorn"
    for end_month, end_day, sign in sun_signs:
        if month < end_month or (month == end_month and day <= end_day):
            sun_sign = sign
            break
    
    # Simple house focus based on day of year
    day_of_year = target_date.timetuple().tm_yday
    house_focus = ((day_of_year - 1) // 30) % 12 + 1
    
    house_themes = {
        1: "Self & Identity",
        2: "Resources & Values",
        3: "Communication & Learning",
        4: "Home & Foundation",
        5: "Creativity & Joy",
        6: "Health & Service",
        7: "Partnerships & Relationships",
        8: "Transformation & Shared Resources",
        9: "Expansion & Philosophy",
        10: "Career & Public Image",
        11: "Community & Aspirations",
        12: "Spirituality & Release",
    }
    
    return SolarTransitData(
        sun_sign=sun_sign,
        house_focus=house_focus,
        house_theme=house_themes[house_focus],
        planetary_aspects=[],  # Would be calculated with ephemeris
        transit_message=f"Focus on {house_themes[house_focus].lower()} matters today",
    )


def generate_human_design(target_date: date, profile: UserProfile) -> HumanDesignData:
    """
    Generate Human Design data for a day.
    
    Simplified version - full implementation would calculate
    actual gate transits from planetary positions.
    
    Args:
        target_date: Date to calculate for.
        profile: User profile with birth data.
    
    Returns:
        HumanDesignData: Human Design information.
    """
    # Default HD type if not calculated (would be from birth chart)
    hd_type = profile.human_design_type or "Generator"
    
    # Strategy and authority by type
    strategies = {
        "Generator": "Wait to respond",
        "Manifesting Generator": "Wait to respond, then inform",
        "Projector": "Wait for the invitation",
        "Manifestor": "Inform before acting",
        "Reflector": "Wait a lunar cycle",
    }
    
    authorities = {
        "Generator": "Sacral",
        "Manifesting Generator": "Sacral",
        "Projector": "Splenic or Emotional",
        "Manifestor": "Emotional or Splenic",
        "Reflector": "Lunar",
    }
    
    signatures = {
        "Generator": "Satisfaction",
        "Manifesting Generator": "Satisfaction",
        "Projector": "Success",
        "Manifestor": "Peace",
        "Reflector": "Surprise",
    }
    
    not_self = {
        "Generator": "Watch for frustration if forcing actions",
        "Manifesting Generator": "Watch for frustration and anger if not responding",
        "Projector": "Watch for bitterness if not recognized",
        "Manifestor": "Watch for anger if meeting resistance",
        "Reflector": "Watch for disappointment if rushing decisions",
    }
    
    # Simple gate calculation based on day of year
    day_of_year = target_date.timetuple().tm_yday
    base_gate = ((day_of_year * 7) % 64) + 1
    
    active_gates = [
        GateData(
            gate_number=base_gate,
            gate_name=f"Gate {base_gate}",
            line=(day_of_year % 6) + 1,
            planet="Sun",
            theme="Daily activation",
        )
    ]
    
    return HumanDesignData(
        type=hd_type,
        strategy=strategies.get(hd_type, "Wait to respond"),
        authority=profile.human_design_authority or authorities.get(hd_type, "Sacral"),
        active_gates=active_gates,
        active_channels=[],
        defined_centers_today=[],
        decision_cue=f"Trust your {authorities.get(hd_type, 'inner')} response",
        energy_management="Honor your energy type's natural rhythm",
        signature_theme=signatures.get(hd_type, "Satisfaction"),
        not_self_warning=not_self.get(hd_type, "Watch for frustration"),
    )


def generate_i_ching(human_design: HumanDesignData) -> IChingData:
    """
    Generate I Ching data based on Human Design gates.
    
    The 64 Human Design gates correspond to the 64 I Ching hexagrams.
    
    Args:
        human_design: Human Design data with active gates.
    
    Returns:
        IChingData: I Ching hexagram information.
    """
    # Get primary hexagram from Sun gate
    sun_gate = next(
        (g for g in human_design.active_gates if g.planet == "Sun"),
        human_design.active_gates[0] if human_design.active_gates else None
    )
    
    hexagram_num = sun_gate.gate_number if sun_gate else 1
    
    # Simplified hexagram data (full data would be in JSON file)
    hexagram_names = {
        1: "The Creative",
        2: "The Receptive",
        # ... abbreviated, full list in data file
    }
    
    hexagram_name = hexagram_names.get(hexagram_num, f"Hexagram {hexagram_num}")
    
    # Trigram mapping (simplified)
    upper_trigrams = ["Heaven", "Earth", "Thunder", "Water", "Mountain", "Wind", "Fire", "Lake"]
    lower_trigrams = upper_trigrams.copy()
    
    upper = upper_trigrams[(hexagram_num - 1) // 8]
    lower = lower_trigrams[(hexagram_num - 1) % 8]
    
    return IChingData(
        hexagram_number=hexagram_num,
        hexagram_name=hexagram_name,
        trigram_above=upper,
        trigram_below=lower,
        judgment="Contemplate the day's energy and act accordingly",
        image="The wise one aligns with natural rhythms",
        changing_lines=[sun_gate.line] if sun_gate else [],
        moving_to=None,
        daily_wisdom="Flow with today's energy rather than against it",
        action_guidance="Take aligned action when the moment is right",
        caution="Avoid forcing outcomes",
    )


def generate_spiritual_reading(
    moon_data: MoonData,
    numerology_data: NumerologyData,
    day_of_year: int,
) -> SpiritualReading:
    """
    Generate spiritual reading for the day.
    
    Selects from curated texts based on daily energies.
    
    Args:
        moon_data: Moon phase and sign data.
        numerology_data: Numerology data.
        day_of_year: Day number in the year.
    
    Returns:
        SpiritualReading: Daily spiritual reading.
    """
    element = moon_data.sign_element
    
    # Source selection by element
    sources = {
        "Fire": ("Meditations", "Marcus Aurelius", "Stoic", "book"),
        "Earth": ("Tao Te Ching", "Lao Tzu", "Taoist", "book"),
        "Air": ("Dhammapada", "Buddha", "Buddhist", "scripture"),
        "Water": ("Poetry Collection", "Rumi", "Sufi", "poetry"),
    }
    
    source_title, author, tradition, source_type = sources.get(
        element, ("Tao Te Ching", "Lao Tzu", "Taoist", "book")
    )
    
    # Sample texts (full implementation would load from JSON)
    sample_texts = {
        "Stoic": '"Begin each day by telling yourself: Today I shall meet people who are meddling, ungrateful, arrogant, dishonest, jealous, and surly."',
        "Taoist": '"The Tao that can be told is not the eternal Tao. The name that can be named is not the eternal name."',
        "Buddhist": '"Mind is the forerunner of all actions. All deeds are led by mind, created by mind."',
        "Sufi": '"Out beyond ideas of wrongdoing and rightdoing, there is a field. I will meet you there."',
    }
    
    return SpiritualReading(
        source_type=source_type,
        tradition=tradition,
        source_title=source_title,
        source_author=author,
        chapter_or_verse=f"Day {day_of_year} selection",
        reading_text=sample_texts.get(tradition, "Wisdom awaits in stillness."),
        daily_relevance=f"This {tradition} wisdom aligns with today's {element} energy",
        contemplation_question=f"How does this ancient wisdom apply to {moon_data.energy_theme.lower()}?",
        embodiment_practice="Pause three times today to recall this wisdom",
    )


def synthesize_daily_theme(
    moon_data: MoonData,
    numerology_data: NumerologyData,
    human_design: HumanDesignData,
) -> str:
    """
    Synthesize the daily theme from multiple domains.
    
    Args:
        moon_data: Moon data.
        numerology_data: Numerology data.
        human_design: Human Design data.
    
    Returns:
        str: Synthesized daily theme.
    """
    moon_theme = moon_data.energy_theme
    num_theme = numerology_data.day_theme.split(" & ")[0]  # First part
    
    return f"{moon_theme} with {num_theme}"


def generate_power_hours(
    biorhythm_data: BiorhythmData,
    moon_data: MoonData,
) -> List[PowerHour]:
    """
    Calculate optimal power hours for the day.
    
    Args:
        biorhythm_data: Biorhythm data.
        moon_data: Moon data.
    
    Returns:
        List[PowerHour]: List of power hour periods.
    """
    hours = []
    
    # Physical peak hours
    if biorhythm_data.physical > 30:
        hours.append(PowerHour(
            time_range="7:00 AM - 10:00 AM",
            optimal_for=["Exercise", "Physical tasks", "Active work"],
            energy_type="Physical energy peak",
        ))
    
    # Mental peak hours
    if biorhythm_data.intellectual > 30:
        hours.append(PowerHour(
            time_range="10:00 AM - 1:00 PM",
            optimal_for=["Complex thinking", "Important decisions", "Learning"],
            energy_type="Mental clarity peak",
        ))
    
    # Creative hours (emotional + intellectual)
    if biorhythm_data.emotional > 20 and biorhythm_data.intellectual > 20:
        hours.append(PowerHour(
            time_range="3:00 PM - 6:00 PM",
            optimal_for=["Creative projects", "Collaboration", "Expression"],
            energy_type="Creative synthesis",
        ))
    
    if not hours:
        hours.append(PowerHour(
            time_range="When energy feels best",
            optimal_for=["Routine tasks", "Self-paced work"],
            energy_type="Moderate energy day",
        ))
    
    return hours


def generate_caution_periods(
    moon_data: MoonData,
    biorhythm_data: BiorhythmData,
) -> List[CautionPeriod]:
    """
    Calculate caution periods for the day.
    
    Args:
        moon_data: Moon data.
        biorhythm_data: Biorhythm data.
    
    Returns:
        List[CautionPeriod]: List of caution periods.
    """
    cautions = []
    
    # Moon VOC period
    if moon_data.moon_void_of_course and moon_data.voc_start:
        cautions.append(CautionPeriod(
            time_range=f"VOC: {moon_data.voc_start.strftime('%I:%M %p')} - {moon_data.voc_end.strftime('%I:%M %p') if moon_data.voc_end else 'end of day'}",
            reason="Moon Void of Course",
            avoid=["Starting new projects", "Major purchases", "Important decisions"],
            instead_do=["Routine tasks", "Review work", "Rest"],
        ))
    
    # Intellectual low period
    if biorhythm_data.intellectual < -20:
        cautions.append(CautionPeriod(
            time_range="Afternoon (1:00 PM - 4:00 PM)",
            reason="Mental energy low",
            avoid=["Complex analysis", "Important negotiations"],
            instead_do=["Physical tasks", "Routine work"],
        ))
    
    return cautions


def generate_affirmation(daily_theme: str, moon_data: MoonData) -> str:
    """Generate daily affirmation."""
    element = moon_data.sign_element
    
    affirmations = {
        "Fire": "I embrace my power and shine brightly",
        "Earth": "I build my dreams with patient, steady hands",
        "Air": "I welcome new ideas and connections with an open mind",
        "Water": "I flow with life's currents and trust my intuition",
    }
    
    return affirmations.get(element, "I am aligned with my highest path")


def generate_mantra(i_ching: IChingData) -> str:
    """Generate daily mantra from I Ching."""
    return f"I embody the wisdom of {i_ching.hexagram_name}"


def generate_daily_entry(
    target_date: date,
    profile: UserProfile,
) -> DailyPreparation:
    """
    Generate complete daily preparation entry.
    
    This is the main orchestration function that brings together
    all calculators and analyzers to produce a full daily guide.
    
    Args:
        target_date: Date to generate for.
        profile: User profile with birth data.
    
    Returns:
        DailyPreparation: Complete daily sovereign alignment guide.
    """
    # Calculate life path if not cached
    if profile.life_path_number is None:
        profile.life_path_number = calculate_life_path(profile.birth_data.date)
    
    # ==========================================================================
    # Calculate all domain data
    # ==========================================================================
    
    # Moon
    moon_data = calculate_moon_data(target_date)
    
    # Numerology
    numerology_data = calculate_numerology_for_day(
        profile.birth_data.date,
        target_date,
        profile.life_path_number,
    )
    
    # Biorhythm
    biorhythm_data = calculate_biorhythm_for_day(
        profile.birth_data.date,
        target_date,
    )
    
    # Solar Transit
    solar_transit = generate_solar_transit(target_date, profile)
    
    # Human Design
    human_design = generate_human_design(target_date, profile)
    
    # I Ching
    i_ching = generate_i_ching(human_design)
    
    # ==========================================================================
    # Run analyzers
    # ==========================================================================
    
    # Risk Analysis
    risk_analysis = calculate_risk_analysis(
        moon_data,
        biorhythm_data,
        numerology_data,
    )
    
    # Exercise
    exercise = generate_exercise_recommendation(biorhythm_data, moon_data)
    
    # Nourishment
    nourishment = generate_nourishment_guidance(moon_data, biorhythm_data)
    
    # ==========================================================================
    # Generate practices
    # ==========================================================================
    
    morning_ritual = generate_morning_ritual(moon_data, biorhythm_data)
    meditation = generate_meditation_practice(moon_data, biorhythm_data)
    journaling = generate_journaling_prompts(moon_data, biorhythm_data)
    spiritual_reading = generate_spiritual_reading(
        moon_data,
        numerology_data,
        target_date.timetuple().tm_yday,
    )
    evening_ritual = generate_evening_ritual(biorhythm_data)
    
    # ==========================================================================
    # Synthesize
    # ==========================================================================
    
    daily_theme = synthesize_daily_theme(moon_data, numerology_data, human_design)
    power_hours = generate_power_hours(biorhythm_data, moon_data)
    caution_periods = generate_caution_periods(moon_data, biorhythm_data)
    affirmation = generate_affirmation(daily_theme, moon_data)
    mantra = generate_mantra(i_ching)
    
    # Theme keywords
    keywords = [
        moon_data.sign_element,
        numerology_data.energy_quality,
        human_design.signature_theme,
    ]
    
    # Closing reflection
    closing = f"Rest well knowing you honored {moon_data.energy_theme.lower()} today"
    
    # Tomorrow preview (simplified)
    tomorrow_preview = "New energies await tomorrow - trust the unfolding"
    
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
        daily_theme=daily_theme,
        theme_keywords=keywords,
        power_hours=power_hours,
        caution_periods=caution_periods,
        affirmation=affirmation,
        daily_mantra=mantra,
        closing_reflection=closing,
        tomorrow_preview=tomorrow_preview,
    )
