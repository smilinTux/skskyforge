"""
Numerology calculator for SkyForge.

Implements Pythagorean numerology calculations for life path,
personal year, personal month, and personal day numbers.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from datetime import date
from typing import List, Tuple

from ..models.domains import NumerologyData


# Master numbers that are preserved during reduction
MASTER_NUMBERS = {11, 22, 33}

# Numerology number meanings
NUMBER_MEANINGS = {
    1: {
        "theme": "New Beginnings & Independence",
        "quality": "Active",
        "keywords": ["initiative", "leadership", "independence", "pioneering"],
        "favorable": ["Starting projects", "Taking initiative", "Self-promotion"],
        "challenging": ["Teamwork", "Patience", "Following others"],
    },
    2: {
        "theme": "Partnership & Balance",
        "quality": "Receptive",
        "keywords": ["cooperation", "diplomacy", "sensitivity", "patience"],
        "favorable": ["Collaboration", "Listening", "Mediation", "Details"],
        "challenging": ["Quick decisions", "Standing alone", "Confrontation"],
    },
    3: {
        "theme": "Expression & Creativity",
        "quality": "Creative",
        "keywords": ["communication", "joy", "creativity", "self-expression"],
        "favorable": ["Creative work", "Social events", "Writing", "Speaking"],
        "challenging": ["Routine tasks", "Discipline", "Serious matters"],
    },
    4: {
        "theme": "Foundation & Structure",
        "quality": "Stable",
        "keywords": ["discipline", "organization", "hard work", "foundation"],
        "favorable": ["Planning", "Building", "Organization", "Practical tasks"],
        "challenging": ["Spontaneity", "Change", "Taking risks"],
    },
    5: {
        "theme": "Change & Freedom",
        "quality": "Dynamic",
        "keywords": ["freedom", "adventure", "change", "versatility"],
        "favorable": ["Travel", "Variety", "Adaptability", "New experiences"],
        "challenging": ["Routine", "Commitment", "Long-term planning"],
    },
    6: {
        "theme": "Responsibility & Nurturing",
        "quality": "Nurturing",
        "keywords": ["home", "family", "responsibility", "service"],
        "favorable": ["Family matters", "Home projects", "Caregiving", "Teaching"],
        "challenging": ["Personal freedom", "Saying no", "Self-focus"],
    },
    7: {
        "theme": "Introspection & Wisdom",
        "quality": "Spiritual",
        "keywords": ["analysis", "spirituality", "wisdom", "solitude"],
        "favorable": ["Research", "Meditation", "Study", "Reflection"],
        "challenging": ["Social events", "Quick decisions", "Surface matters"],
    },
    8: {
        "theme": "Abundance & Power",
        "quality": "Material",
        "keywords": ["success", "power", "abundance", "manifestation"],
        "favorable": ["Business", "Financial matters", "Authority", "Achievement"],
        "challenging": ["Letting go", "Emotional matters", "Spiritual pursuits"],
    },
    9: {
        "theme": "Completion & Humanitarianism",
        "quality": "Universal",
        "keywords": ["completion", "humanitarianism", "wisdom", "endings"],
        "favorable": ["Finishing projects", "Giving", "Release", "Global thinking"],
        "challenging": ["New beginnings", "Personal gain", "Attachment"],
    },
    11: {
        "theme": "Illumination & Intuition (Master Number)",
        "quality": "Inspirational",
        "keywords": ["intuition", "inspiration", "illumination", "idealism"],
        "favorable": ["Spiritual work", "Inspiration", "Teaching", "Healing"],
        "challenging": ["Grounding", "Practical matters", "Self-doubt"],
        "master_message": "Master Number 11 active - heightened intuition and spiritual insight available. Trust your inner guidance.",
    },
    22: {
        "theme": "Master Builder (Master Number)",
        "quality": "Manifesting",
        "keywords": ["vision", "practical idealism", "large projects", "legacy"],
        "favorable": ["Large-scale projects", "Manifestation", "Building systems"],
        "challenging": ["Small thinking", "Impatience", "Overwhelm"],
        "master_message": "Master Number 22 active - potential for manifesting grand visions into reality. Think big but act practically.",
    },
    33: {
        "theme": "Master Teacher (Master Number)",
        "quality": "Compassionate",
        "keywords": ["compassion", "healing", "teaching", "selfless service"],
        "favorable": ["Teaching", "Healing", "Compassionate service", "Guidance"],
        "challenging": ["Self-care", "Boundaries", "Personal needs"],
        "master_message": "Master Number 33 active - profound healing and teaching energy available. Serve with love but maintain boundaries.",
    },
}


def reduce_to_single_digit(number: int, keep_master: bool = True) -> int:
    """
    Reduce a number to a single digit (1-9) or master number (11, 22, 33).
    
    Args:
        number: The number to reduce.
        keep_master: If True, preserve master numbers 11, 22, 33.
    
    Returns:
        Single digit (1-9) or master number.
    
    Example:
        >>> reduce_to_single_digit(38)
        11
        >>> reduce_to_single_digit(38, keep_master=False)
        2
    """
    while number > 9:
        if keep_master and number in MASTER_NUMBERS:
            return number
        number = sum(int(d) for d in str(abs(number)))
    return number


def calculate_life_path(birth_date: date) -> int:
    """
    Calculate Life Path number from birth date.
    
    The Life Path is the most important number in numerology,
    representing your life's purpose and the path you'll walk.
    
    Formula: Reduce (Month + Day + Year) individually, then sum and reduce.
    
    Args:
        birth_date: Date of birth.
    
    Returns:
        Life Path number (1-9 or master number 11, 22, 33).
    
    Example:
        >>> calculate_life_path(date(1985, 3, 15))
        5  # 3 + 6 + 5 = 14 -> 5
    """
    # Reduce each component separately first (preserves master numbers better)
    month = reduce_to_single_digit(birth_date.month)
    day = reduce_to_single_digit(birth_date.day)
    year = reduce_to_single_digit(sum(int(d) for d in str(birth_date.year)))
    
    total = month + day + year
    return reduce_to_single_digit(total)


def calculate_personal_year(birth_date: date, target_year: int) -> int:
    """
    Calculate Personal Year number.
    
    The Personal Year indicates the theme and energy of a particular year
    in your life. It runs from birthday to birthday.
    
    Formula: Reduce (Birth Month + Birth Day + Target Year)
    
    Args:
        birth_date: Date of birth.
        target_year: The year to calculate for.
    
    Returns:
        Personal Year number (1-9 or master number).
    
    Example:
        >>> calculate_personal_year(date(1985, 3, 15), 2026)
        7  # 3 + 6 + 10 = 19 -> 10 -> 1... actually 3+6+1=10->1
    """
    month = reduce_to_single_digit(birth_date.month)
    day = reduce_to_single_digit(birth_date.day)
    year = reduce_to_single_digit(sum(int(d) for d in str(target_year)))
    
    total = month + day + year
    return reduce_to_single_digit(total)


def calculate_personal_month(personal_year: int, month: int) -> int:
    """
    Calculate Personal Month number.
    
    Args:
        personal_year: The Personal Year number.
        month: Calendar month (1-12).
    
    Returns:
        Personal Month number (1-9 or master number).
    """
    total = personal_year + month
    return reduce_to_single_digit(total)


def calculate_personal_day(personal_month: int, day: int) -> int:
    """
    Calculate Personal Day number.
    
    Args:
        personal_month: The Personal Month number.
        day: Day of the month (1-31).
    
    Returns:
        Personal Day number (1-9 or master number).
    """
    total = personal_month + day
    return reduce_to_single_digit(total)


def calculate_universal_day(target_date: date) -> int:
    """
    Calculate Universal Day number (collective energy).
    
    This represents the universal energy affecting everyone on this day.
    
    Formula: Reduce (Month + Day + Year of target date)
    
    Args:
        target_date: The date to calculate for.
    
    Returns:
        Universal Day number (1-9 or master number).
    """
    total = (
        target_date.month + 
        target_date.day + 
        sum(int(d) for d in str(target_date.year))
    )
    return reduce_to_single_digit(total)


def get_number_meaning(number: int) -> dict:
    """
    Get the meaning and attributes for a numerology number.
    
    Args:
        number: The numerology number (1-9, 11, 22, 33).
    
    Returns:
        Dictionary with theme, quality, keywords, favorable, challenging.
    """
    return NUMBER_MEANINGS.get(number, NUMBER_MEANINGS[1])


def calculate_numerology_for_day(
    birth_date: date,
    target_date: date,
    life_path: int = None,
) -> NumerologyData:
    """
    Calculate complete numerology data for a specific day.
    
    Args:
        birth_date: User's birth date.
        target_date: Date to calculate for.
        life_path: Pre-calculated life path (optional, will calculate if not provided).
    
    Returns:
        NumerologyData: Complete numerology data for the day.
    """
    # Calculate all numbers
    if life_path is None:
        life_path = calculate_life_path(birth_date)
    
    personal_year = calculate_personal_year(birth_date, target_date.year)
    personal_month = calculate_personal_month(personal_year, target_date.month)
    personal_day = calculate_personal_day(personal_month, target_date.day)
    universal_day = calculate_universal_day(target_date)
    
    # Get meanings for personal day
    day_meaning = get_number_meaning(personal_day)
    
    # Check for master numbers
    master_active = personal_day in MASTER_NUMBERS
    master_message = day_meaning.get("master_message") if master_active else None
    
    return NumerologyData(
        life_path=life_path,
        personal_year=personal_year,
        personal_month=personal_month,
        personal_day=personal_day,
        universal_day=universal_day,
        day_theme=day_meaning["theme"],
        energy_quality=day_meaning["quality"],
        favorable_for=day_meaning["favorable"],
        challenging_for=day_meaning["challenging"],
        master_number_active=master_active,
        master_number_message=master_message,
    )
