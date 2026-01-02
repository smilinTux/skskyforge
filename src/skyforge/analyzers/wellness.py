"""
Wellness analyzer for SkyForge.

Generates exercise and nourishment recommendations based on
biorhythm and moon data.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from typing import List

from ..models.domains import (
    MoonData,
    BiorhythmData,
    ExerciseRecommendation,
    NourishmentGuidance,
    MorningRitualData,
    MeditationPractice,
    JournalingPrompt,
    EveningRitualData,
)


# Element-based exercise activities
ELEMENT_EXERCISES = {
    "Fire": ["HIIT", "Running", "Power yoga", "Boxing", "Dancing"],
    "Earth": ["Weight training", "Hiking", "Pilates", "Gardening", "Walking"],
    "Air": ["Dance", "Cycling", "Varied circuits", "Tennis", "Jump rope"],
    "Water": ["Swimming", "Flow yoga", "Tai chi", "Aqua aerobics", "Surfing"],
}

# Element-based nourishment guidance
ELEMENT_NOURISHMENT = {
    "Fire": {
        "focus": "Cooling and light",
        "emphasized": ["Fresh salads", "Fruits", "Cucumber", "Mint", "Coconut water"],
        "minimize": ["Heavy meats", "Spicy foods", "Alcohol", "Excessive caffeine"],
        "hydration": "Extra water and cooling beverages",
        "breakfast": "Fresh fruit smoothie with greens",
        "lunch": "Large colorful salad with light protein",
        "dinner": "Grilled fish with steamed vegetables",
        "snacks": ["Fresh fruit", "Coconut", "Cooling herbal tea"],
    },
    "Earth": {
        "focus": "Grounding and nourishing",
        "emphasized": ["Root vegetables", "Whole grains", "Legumes", "Nuts", "Mushrooms"],
        "minimize": ["Processed foods", "Excessive sugar", "Light/airy foods"],
        "hydration": "Warm herbal teas, room temperature water",
        "breakfast": "Warm oatmeal with nuts and seeds",
        "lunch": "Hearty grain bowl with roasted vegetables",
        "dinner": "Root vegetable stew with whole grain bread",
        "snacks": ["Trail mix", "Hummus with vegetables", "Whole grain crackers"],
    },
    "Air": {
        "focus": "Light and varied",
        "emphasized": ["Leafy greens", "Light proteins", "Seeds", "Sprouts", "Berries"],
        "minimize": ["Heavy, dense foods", "Large portions", "Fried foods"],
        "hydration": "Consistent hydration throughout day",
        "breakfast": "Light yogurt parfait with granola",
        "lunch": "Variety of small dishes, tapas style",
        "dinner": "Light stir-fry with diverse vegetables",
        "snacks": ["Seeds", "Light crackers", "Fresh berries"],
    },
    "Water": {
        "focus": "Warming and comforting",
        "emphasized": ["Soups", "Stews", "Ginger", "Cinnamon", "Warming spices"],
        "minimize": ["Cold foods", "Raw foods", "Excessive dairy", "Ice water"],
        "hydration": "Warm water, ginger tea, herbal infusions",
        "breakfast": "Warm porridge with cinnamon and honey",
        "lunch": "Nourishing soup with whole grain bread",
        "dinner": "Comforting stew or curry",
        "snacks": ["Warm spiced milk", "Baked apple", "Ginger cookies"],
    },
}


def generate_exercise_recommendation(
    biorhythm_data: BiorhythmData,
    moon_data: MoonData,
) -> ExerciseRecommendation:
    """
    Generate exercise recommendations based on biorhythm and moon.
    
    Args:
        biorhythm_data: Biorhythm cycle data.
        moon_data: Moon phase and sign data.
    
    Returns:
        ExerciseRecommendation: Personalized exercise guidance.
    """
    physical = biorhythm_data.physical
    element = moon_data.sign_element
    
    # Handle critical day first
    if biorhythm_data.physical_critical:
        return ExerciseRecommendation(
            exercise_type="Rest/Gentle Movement",
            intensity="Recovery",
            optimal_time="Listen to your body",
            duration_minutes=20,
            specific_activities=["Gentle stretching", "Short walk", "Restorative yoga"],
            avoid_today=["High intensity", "Heavy lifting", "Competitive sports"],
            rationale="Physical biorhythm at critical point - prioritize recovery",
        )
    
    # Determine base recommendations from physical level
    if physical > 70:
        exercise_type = "High Intensity Training"
        intensity = "High"
        duration = 45
        optimal_time = "Morning (7-9 AM)"
    elif physical > 40:
        exercise_type = "Strength Training"
        intensity = "Moderate-High"
        duration = 40
        optimal_time = "Morning (8-10 AM)"
    elif physical > 0:
        exercise_type = "Moderate Cardio"
        intensity = "Moderate"
        duration = 30
        optimal_time = "Mid-morning (9-11 AM)"
    elif physical > -40:
        exercise_type = "Light Activity"
        intensity = "Low-Moderate"
        duration = 25
        optimal_time = "Late morning or early evening"
    else:
        exercise_type = "Gentle Movement"
        intensity = "Low"
        duration = 20
        optimal_time = "When energy feels best"
    
    # Get element-specific activities
    activities = ELEMENT_EXERCISES.get(element, ELEMENT_EXERCISES["Earth"])[:3]
    
    # Determine what to avoid
    avoid = []
    if physical < -30:
        avoid.extend(["High-intensity cardio", "Heavy weights"])
    if biorhythm_data.emotional < -30:
        avoid.append("Competitive sports")
    if biorhythm_data.intellectual < -30:
        avoid.append("Complex new routines")
    if not avoid:
        avoid = ["Overexertion beyond energy levels"]
    
    rationale = f"Physical biorhythm at {physical:.0f}%, {element} moon energy favors {element.lower()}-aligned activities"
    
    return ExerciseRecommendation(
        exercise_type=exercise_type,
        intensity=intensity,
        optimal_time=optimal_time,
        duration_minutes=duration,
        specific_activities=activities,
        avoid_today=avoid[:3],
        rationale=rationale,
    )


def generate_nourishment_guidance(
    moon_data: MoonData,
    biorhythm_data: BiorhythmData,
) -> NourishmentGuidance:
    """
    Generate nourishment guidance based on moon element and biorhythm.
    
    Args:
        moon_data: Moon phase and sign data.
        biorhythm_data: Biorhythm cycle data.
    
    Returns:
        NourishmentGuidance: Personalized dietary guidance.
    """
    element = moon_data.sign_element
    guidance = ELEMENT_NOURISHMENT.get(element, ELEMENT_NOURISHMENT["Earth"])
    
    # Adjust meal timing based on biorhythm
    if biorhythm_data.physical < 0:
        meal_timing = "Earlier, lighter dinner recommended (by 6:30 PM)"
    elif biorhythm_data.overall_energy == "High":
        meal_timing = "Normal timing with adequate portions for activity"
    else:
        meal_timing = "Standard timing, moderate portions"
    
    return NourishmentGuidance(
        element_focus=guidance["focus"],
        foods_emphasized=guidance["emphasized"],
        foods_minimize=guidance["minimize"],
        hydration_focus=guidance["hydration"],
        meal_timing=meal_timing,
        breakfast_suggestion=guidance["breakfast"],
        lunch_suggestion=guidance["lunch"],
        dinner_suggestion=guidance["dinner"],
        snack_suggestions=guidance["snacks"],
    )


def generate_morning_ritual(
    moon_data: MoonData,
    biorhythm_data: BiorhythmData,
) -> MorningRitualData:
    """
    Generate morning ritual recommendations.
    
    Args:
        moon_data: Moon phase and sign data.
        biorhythm_data: Biorhythm cycle data.
    
    Returns:
        MorningRitualData: Morning ritual guidance.
    """
    element = moon_data.sign_element
    
    # Wake time based on overall energy
    if biorhythm_data.overall_energy == "High":
        wake_time = "6:00 AM - Rise with energy"
    elif biorhythm_data.overall_energy == "Low":
        wake_time = "7:00 AM - Gentle awakening"
    else:
        wake_time = "6:30 AM - Balanced start"
    
    # Breathwork by element
    breathwork_map = {
        "Fire": "Breath of Fire (Kapalabhati) - 3 minutes",
        "Earth": "4-7-8 Breathing for grounding - 5 minutes",
        "Air": "Alternate nostril breathing - 5 minutes",
        "Water": "Ocean breath (Ujjayi) - 5 minutes",
    }
    breathwork = breathwork_map.get(element, "Deep belly breathing - 5 minutes")
    
    # Movement by element
    movement_map = {
        "Fire": "Sun salutations - energizing flow",
        "Earth": "Grounding yoga poses - stability focus",
        "Air": "Dynamic stretching - varied movement",
        "Water": "Gentle flowing yoga - fluid motion",
    }
    movement = movement_map.get(element, "Gentle stretching - 10 minutes")
    
    # Intention based on moon sign theme
    intention = f"I embrace {moon_data.energy_theme.lower()} today"
    
    return MorningRitualData(
        wake_time_suggestion=wake_time,
        intention_setting=intention,
        breathwork=breathwork,
        movement=movement,
        duration_minutes=20,
    )


def generate_meditation_practice(
    moon_data: MoonData,
    biorhythm_data: BiorhythmData,
) -> MeditationPractice:
    """
    Generate meditation practice recommendations.
    
    Args:
        moon_data: Moon phase and sign data.
        biorhythm_data: Biorhythm cycle data.
    
    Returns:
        MeditationPractice: Meditation guidance.
    """
    element = moon_data.sign_element
    
    # Technique by element
    technique_map = {
        "Fire": "Candle gazing (Trataka)",
        "Earth": "Body scan meditation",
        "Air": "Mindfulness of thoughts",
        "Water": "Loving-kindness meditation",
    }
    technique = technique_map.get(element, "Breath awareness")
    
    # Duration based on intellectual biorhythm
    if biorhythm_data.intellectual > 50:
        duration = 25
        optimal_time = "Morning or midday"
    elif biorhythm_data.intellectual > 0:
        duration = 20
        optimal_time = "Midday"
    else:
        duration = 15
        optimal_time = "Evening (shorter, gentler)"
    
    # Mantra by element
    mantra_map = {
        "Fire": "I am powerful and radiant",
        "Earth": "I am grounded and secure",
        "Air": "I am clear and free",
        "Water": "I flow with life's currents",
    }
    mantra = mantra_map.get(element)
    
    # Focus theme from moon
    focus = moon_data.energy_theme
    
    return MeditationPractice(
        technique=technique,
        duration_minutes=duration,
        optimal_time=optimal_time,
        focus_theme=focus,
        mantra=mantra,
        visualization=None,
    )


def generate_evening_ritual(
    biorhythm_data: BiorhythmData,
) -> EveningRitualData:
    """
    Generate evening ritual recommendations.
    
    Args:
        biorhythm_data: Biorhythm cycle data.
    
    Returns:
        EveningRitualData: Evening ritual guidance.
    """
    # Timing based on energy
    if biorhythm_data.overall_energy == "Low":
        wind_down = "8:00 PM"
        screen_off = "8:30 PM"
        sleep_time = "9:30 PM"
    elif biorhythm_data.overall_energy == "High":
        wind_down = "9:00 PM"
        screen_off = "9:30 PM"
        sleep_time = "10:30 PM"
    else:
        wind_down = "8:30 PM"
        screen_off = "9:00 PM"
        sleep_time = "10:00 PM"
    
    return EveningRitualData(
        wind_down_time=wind_down,
        screen_cutoff=screen_off,
        reflection_practice="Review three wins from today",
        sleep_preparation="Warm bath or shower, dim lights, gratitude practice",
        optimal_sleep_time=sleep_time,
    )


def generate_journaling_prompts(
    moon_data: MoonData,
    biorhythm_data: BiorhythmData,
) -> JournalingPrompt:
    """
    Generate journaling prompts aligned with daily energies.
    
    Args:
        moon_data: Moon phase and sign data.
        biorhythm_data: Biorhythm cycle data.
    
    Returns:
        JournalingPrompt: Daily journaling prompts.
    """
    element = moon_data.sign_element
    
    # Morning prompts by element
    morning_prompts = {
        "Fire": "What bold action can I take today?",
        "Earth": "What practical step can I take toward my goals?",
        "Air": "What new perspective can I explore today?",
        "Water": "What emotional truth wants to be acknowledged?",
    }
    
    # Evening prompts by element
    evening_prompts = {
        "Fire": "Where did I express my authentic power today?",
        "Earth": "What did I build or accomplish today?",
        "Air": "What new idea or connection emerged today?",
        "Water": "What feelings flowed through me today?",
    }
    
    # Deep inquiry based on moon sign
    sign_inquiries = {
        "Aries": "Where am I holding back from starting something new?",
        "Taurus": "What do I truly value and how am I honoring that?",
        "Gemini": "What am I curious about that I haven't explored?",
        "Cancer": "What does my inner child need right now?",
        "Leo": "How can I express my creativity more fully?",
        "Virgo": "What small improvement would make a big difference?",
        "Libra": "Where do I need more balance in my life?",
        "Scorpio": "What am I ready to release and transform?",
        "Sagittarius": "What adventure is calling to me?",
        "Capricorn": "What legacy am I building?",
        "Aquarius": "How can I contribute to something larger than myself?",
        "Pisces": "What does my intuition want me to know?",
    }
    
    # Gratitude focus based on biorhythm
    if biorhythm_data.overall_energy == "Low":
        gratitude = "Simple blessings and basic comforts"
    elif biorhythm_data.overall_energy == "High":
        gratitude = "Opportunities and energy for action"
    else:
        gratitude = "Balance and present moment awareness"
    
    return JournalingPrompt(
        morning_prompt=morning_prompts.get(element, "What is my intention for today?"),
        evening_prompt=evening_prompts.get(element, "What am I grateful for today?"),
        theme_exploration=sign_inquiries.get(moon_data.zodiac_sign, "What wants to emerge today?"),
        gratitude_focus=gratitude,
    )
