"""
Risk analysis for SkyForge.

Calculates multi-domain risk scores based on biorhythm, moon, and other factors.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from typing import List

from ..models.domains import (
    MoonData,
    BiorhythmData,
    NumerologyData,
    RiskAnalysisData,
    RiskWarning,
)


# Risk factor weights
RISK_WEIGHTS = {
    "moon_voc": 3,
    "biorhythm_critical": 4,
    "biorhythm_low": 2,
    "challenging_numerology": 2,
}

# Protective practices by domain
PROTECTIVE_PRACTICES = {
    "spiritual": [
        "Morning grounding meditation",
        "Protective visualization",
        "Energy clearing",
        "Intention setting",
    ],
    "emotional": [
        "Journaling",
        "Breathwork",
        "Self-compassion practice",
        "Connecting with supportive people",
    ],
    "physical": [
        "Gentle stretching",
        "Adequate hydration",
        "Extra rest",
        "Mindful movement",
    ],
}

# Grounding techniques by risk level
GROUNDING_TECHNIQUES = {
    "Low": ["5-minute breathing", "Brief nature walk"],
    "Moderate": ["10-minute meditation", "Grounding visualization", "Body scan"],
    "Elevated": ["20-minute meditation", "Earth connection exercise", "Cold water on wrists"],
    "High": ["Extended meditation", "Nature immersion", "Digital detox", "Early bedtime"],
}


def calculate_risk_analysis(
    moon_data: MoonData,
    biorhythm_data: BiorhythmData,
    numerology_data: NumerologyData,
) -> RiskAnalysisData:
    """
    Calculate multi-domain risk analysis.
    
    Evaluates potential risks in spiritual, emotional, and physical domains
    based on biorhythm cycles, moon phases, and numerology.
    
    Args:
        moon_data: Moon phase and sign data.
        biorhythm_data: Biorhythm cycle data.
        numerology_data: Numerology data for the day.
    
    Returns:
        RiskAnalysisData: Complete risk analysis with warnings and recommendations.
    """
    spiritual_risk = 0
    emotional_risk = 0
    physical_risk = 0
    warnings: List[RiskWarning] = []
    
    # ==========================================================================
    # Moon Void of Course Risk
    # ==========================================================================
    if moon_data.moon_void_of_course:
        spiritual_risk += RISK_WEIGHTS["moon_voc"]
        emotional_risk += RISK_WEIGHTS["moon_voc"]
        warnings.append(RiskWarning(
            domain="Spiritual",
            source="Moon Void of Course",
            message="Avoid initiating new projects or making major decisions",
            severity="Caution"
        ))
    
    # ==========================================================================
    # Biorhythm Risk Factors
    # ==========================================================================
    
    # Physical critical day
    if biorhythm_data.physical_critical:
        physical_risk += RISK_WEIGHTS["biorhythm_critical"]
        warnings.append(RiskWarning(
            domain="Physical",
            source="Physical Biorhythm Critical",
            message="Take extra care with physical activities; accident risk elevated",
            severity="Warning"
        ))
    
    # Physical low
    if biorhythm_data.physical < -50:
        physical_risk += RISK_WEIGHTS["biorhythm_low"]
        warnings.append(RiskWarning(
            domain="Physical",
            source="Physical Biorhythm Low",
            message="Energy is depleted; prioritize rest over exertion",
            severity="Caution"
        ))
    
    # Emotional critical day
    if biorhythm_data.emotional_critical:
        emotional_risk += RISK_WEIGHTS["biorhythm_critical"]
        warnings.append(RiskWarning(
            domain="Emotional",
            source="Emotional Biorhythm Critical",
            message="Emotional sensitivity heightened; practice extra self-care",
            severity="Warning"
        ))
    
    # Emotional low
    if biorhythm_data.emotional < -50:
        emotional_risk += RISK_WEIGHTS["biorhythm_low"]
        warnings.append(RiskWarning(
            domain="Emotional",
            source="Emotional Biorhythm Low",
            message="Emotional resilience reduced; avoid difficult conversations",
            severity="Caution"
        ))
    
    # Intellectual critical day
    if biorhythm_data.intellectual_critical:
        spiritual_risk += 2  # Affects mental clarity
        warnings.append(RiskWarning(
            domain="Spiritual",
            source="Intellectual Biorhythm Critical",
            message="Mental clarity fluctuating; double-check important decisions",
            severity="Caution"
        ))
    
    # Intellectual low
    if biorhythm_data.intellectual < -50:
        spiritual_risk += 1
        warnings.append(RiskWarning(
            domain="Spiritual",
            source="Intellectual Biorhythm Low",
            message="Mental energy depleted; postpone complex analysis",
            severity="Caution"
        ))
    
    # ==========================================================================
    # Numerology Risk Factors
    # ==========================================================================
    
    # Challenging numerology days
    challenging_numbers = {4, 7, 9}  # Numbers with introspective/ending energy
    if numerology_data.personal_day in challenging_numbers:
        if numerology_data.personal_day == 7:
            spiritual_risk += 1  # Need for solitude
        elif numerology_data.personal_day == 9:
            emotional_risk += 1  # Endings/release
        elif numerology_data.personal_day == 4:
            physical_risk += 1  # Need for structure
    
    # ==========================================================================
    # Calculate Overall Risk
    # ==========================================================================
    
    # Cap individual risks at 10
    spiritual_risk = min(spiritual_risk, 10)
    emotional_risk = min(emotional_risk, 10)
    physical_risk = min(physical_risk, 10)
    
    # Calculate composite score (0-100)
    total_risk = (spiritual_risk + emotional_risk + physical_risk) / 3
    risk_score = round(total_risk * 10, 1)
    
    # Determine risk level
    if risk_score < 25:
        overall_level = "Low"
    elif risk_score < 50:
        overall_level = "Moderate"
    elif risk_score < 75:
        overall_level = "Elevated"
    else:
        overall_level = "High"
    
    # ==========================================================================
    # Get Protective Practices and Grounding Techniques
    # ==========================================================================
    
    protective = []
    
    # Add practices based on which domains have elevated risk
    if spiritual_risk >= 3:
        protective.extend(PROTECTIVE_PRACTICES["spiritual"][:2])
    if emotional_risk >= 3:
        protective.extend(PROTECTIVE_PRACTICES["emotional"][:2])
    if physical_risk >= 3:
        protective.extend(PROTECTIVE_PRACTICES["physical"][:2])
    
    # If no specific risks, add general recommendation
    if not protective:
        protective = ["Standard self-care practices", "Mindful awareness"]
    
    # Get grounding techniques based on overall level
    grounding = GROUNDING_TECHNIQUES.get(overall_level, GROUNDING_TECHNIQUES["Low"])
    
    return RiskAnalysisData(
        spiritual_risk=spiritual_risk,
        emotional_risk=emotional_risk,
        physical_risk=physical_risk,
        overall_risk_level=overall_level,
        risk_score=risk_score,
        warnings=warnings,
        protective_practices=protective[:4],  # Limit to 4
        grounding_techniques=grounding,
    )
