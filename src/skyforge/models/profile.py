"""
User profile models for SkyForge.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import yaml
from pydantic import BaseModel, Field

from .birth_data import BirthData, Location


class ProfileMetadata(BaseModel):
    """Metadata about a user profile."""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    notes: Optional[str] = None


class UserProfile(BaseModel):
    """
    Complete user profile with birth data and computed values.
    
    Attributes:
        name: Unique profile identifier
        birth_data: User's birth information
        current_location: Current location (for relocated charts)
        life_path_number: Numerology life path (auto-calculated)
        human_design_type: HD type (auto-calculated)
        human_design_strategy: HD strategy (auto-calculated)
        human_design_authority: HD authority (auto-calculated)
        personal_year_cache: Cached personal year numbers by year
        metadata: Profile metadata (creation date, notes, etc.)
    """
    name: str
    birth_data: BirthData
    current_location: Optional[Location] = None
    
    # Auto-calculated fields
    life_path_number: Optional[int] = None
    human_design_type: Optional[str] = None
    human_design_strategy: Optional[str] = None
    human_design_authority: Optional[str] = None
    
    # Cache for computed values
    personal_year_cache: Dict[int, int] = Field(default_factory=dict)
    
    # Metadata
    metadata: ProfileMetadata = Field(default_factory=ProfileMetadata)
    
    def save(self, profiles_dir: Path) -> None:
        """
        Save profile to YAML file.
        
        Args:
            profiles_dir: Directory to save profile in.
        """
        profiles_dir.mkdir(parents=True, exist_ok=True)
        filepath = profiles_dir / f"{self.name}.yaml"
        
        # Update metadata
        now = datetime.now()
        if self.metadata.created_at is None:
            self.metadata.created_at = now
        self.metadata.updated_at = now
        
        # Convert to dict and save
        data = self.model_dump(mode='json')
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    @classmethod
    def load(cls, filepath: Path) -> "UserProfile":
        """
        Load profile from YAML file.
        
        Args:
            filepath: Path to the profile YAML file.
            
        Returns:
            UserProfile: Loaded profile instance.
            
        Raises:
            FileNotFoundError: If profile file doesn't exist.
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Profile not found: {filepath}")
        
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        
        return cls.model_validate(data)
    
    @classmethod
    def load_by_name(cls, name: str, profiles_dir: Path) -> "UserProfile":
        """
        Load profile by name from profiles directory.
        
        Args:
            name: Profile name.
            profiles_dir: Directory containing profile files.
            
        Returns:
            UserProfile: Loaded profile instance.
        """
        filepath = profiles_dir / f"{name}.yaml"
        return cls.load(filepath)
    
    def get_personal_year(self, year: int) -> int:
        """
        Get personal year number, using cache if available.
        
        Args:
            year: Target year.
            
        Returns:
            int: Personal year number (1-9 or master number).
        """
        if year not in self.personal_year_cache:
            from ..calculators.numerology import calculate_personal_year
            self.personal_year_cache[year] = calculate_personal_year(
                self.birth_data.date, year
            )
        return self.personal_year_cache[year]
