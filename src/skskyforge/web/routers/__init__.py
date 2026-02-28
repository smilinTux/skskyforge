"""
SKSkyforge FastAPI routes — REST API for calendar generation.

Endpoints:
  POST /api/generate/daily       — single day entry
  POST /api/generate/range       — date range of entries
  CRUD /api/profiles             — profile management
  POST /api/export/{fmt}         — PDF / CSV / Excel export

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin

This file is part of SKSkyforge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from __future__ import annotations

import tempfile
from datetime import date, timedelta
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from ...generators import generate_daily_entry
from ...exporters import export_csv, export_excel, export_pdf
from ...models import (
    BirthData,
    BirthTimeRange,
    DailyPreparation,
    Location,
    UserProfile,
)

router = APIRouter()

# ---------------------------------------------------------------------------
# Default profiles directory
# ---------------------------------------------------------------------------
_PROFILES_DIR = Path.home() / ".skskyforge" / "profiles"


# ===================================================================
# Request / response schemas
# ===================================================================

class LocationIn(BaseModel):
    city: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    timezone: str = "UTC"


class BirthDataIn(BaseModel):
    date: date
    time: Optional[str] = None  # "HH:MM" string
    time_range: str = "unknown"
    location: Optional[LocationIn] = None


class ProfileIn(BaseModel):
    name: str
    birth_data: BirthDataIn
    current_location: Optional[LocationIn] = None
    human_design_type: Optional[str] = None
    human_design_strategy: Optional[str] = None
    human_design_authority: Optional[str] = None


class ProfileOut(BaseModel):
    name: str
    birth_date: date
    birth_time: Optional[str] = None
    time_range: str
    location: Optional[LocationIn] = None
    life_path_number: Optional[int] = None
    human_design_type: Optional[str] = None

    @classmethod
    def from_profile(cls, p: UserProfile) -> "ProfileOut":
        loc = None
        if p.birth_data.location:
            loc = LocationIn(
                city=p.birth_data.location.city,
                latitude=p.birth_data.location.latitude,
                longitude=p.birth_data.location.longitude,
                timezone=p.birth_data.location.timezone,
            )
        return cls(
            name=p.name,
            birth_date=p.birth_data.date,
            birth_time=p.birth_data.time.isoformat() if p.birth_data.time else None,
            time_range=p.birth_data.time_range.value,
            location=loc,
            life_path_number=p.life_path_number,
            human_design_type=p.human_design_type,
        )


class DailyRequest(BaseModel):
    date: date
    profile_name: str


class RangeRequest(BaseModel):
    start_date: date
    end_date: date
    profile_name: str


class ExportRequest(BaseModel):
    start_date: date
    end_date: date
    profile_name: str


# ===================================================================
# Helpers
# ===================================================================

def _build_location(loc: Optional[LocationIn]) -> Optional[Location]:
    if loc is None:
        return None
    return Location(
        city=loc.city,
        latitude=loc.latitude,
        longitude=loc.longitude,
        timezone=loc.timezone,
    )


def _build_birth_data(bd: BirthDataIn) -> BirthData:
    from datetime import time as dt_time

    birth_time = None
    if bd.time:
        parts = bd.time.split(":")
        birth_time = dt_time(int(parts[0]), int(parts[1]))

    return BirthData(
        date=bd.date,
        time=birth_time,
        time_range=BirthTimeRange(bd.time_range),
        location=_build_location(bd.location),
    )


def _load_profile(name: str) -> UserProfile:
    try:
        return UserProfile.load_by_name(name, _PROFILES_DIR)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Profile '{name}' not found")


def _generate_entries(profile: UserProfile, start: date, end: date) -> List[DailyPreparation]:
    entries: List[DailyPreparation] = []
    current = start
    while current <= end:
        entries.append(generate_daily_entry(current, profile))
        current += timedelta(days=1)
    return entries


# ===================================================================
# Generation routes
# ===================================================================

@router.post("/generate/daily")
def generate_daily(req: DailyRequest):
    """Generate a single daily alignment entry."""
    profile = _load_profile(req.profile_name)
    entry = generate_daily_entry(req.date, profile)
    return entry.model_dump(mode="json")


@router.post("/generate/range")
def generate_range(req: RangeRequest):
    """Generate entries for a date range."""
    if req.end_date < req.start_date:
        raise HTTPException(status_code=422, detail="end_date must be >= start_date")
    days = (req.end_date - req.start_date).days + 1
    if days > 366:
        raise HTTPException(status_code=422, detail="Range must not exceed 366 days")

    profile = _load_profile(req.profile_name)
    entries = _generate_entries(profile, req.start_date, req.end_date)
    return [e.model_dump(mode="json") for e in entries]


# ===================================================================
# Profile CRUD
# ===================================================================

@router.get("/profiles", response_model=List[ProfileOut])
def list_profiles():
    """List all saved profiles."""
    _PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    profiles = []
    for path in sorted(_PROFILES_DIR.glob("*.yaml")):
        try:
            profiles.append(ProfileOut.from_profile(UserProfile.load(path)))
        except Exception:
            continue
    return profiles


@router.get("/profiles/{name}", response_model=ProfileOut)
def get_profile(name: str):
    """Get a profile by name."""
    profile = _load_profile(name)
    return ProfileOut.from_profile(profile)


@router.post("/profiles", response_model=ProfileOut, status_code=201)
def create_profile(req: ProfileIn):
    """Create a new profile."""
    filepath = _PROFILES_DIR / f"{req.name}.yaml"
    if filepath.exists():
        raise HTTPException(status_code=409, detail=f"Profile '{req.name}' already exists")

    profile = UserProfile(
        name=req.name,
        birth_data=_build_birth_data(req.birth_data),
        current_location=_build_location(req.current_location),
        human_design_type=req.human_design_type,
        human_design_strategy=req.human_design_strategy,
        human_design_authority=req.human_design_authority,
    )
    profile.save(_PROFILES_DIR)
    return ProfileOut.from_profile(profile)


@router.put("/profiles/{name}", response_model=ProfileOut)
def update_profile(name: str, req: ProfileIn):
    """Update an existing profile."""
    existing = _load_profile(name)

    # If renaming, remove old file
    if req.name != name:
        old_path = _PROFILES_DIR / f"{name}.yaml"
        old_path.unlink(missing_ok=True)

    updated = UserProfile(
        name=req.name,
        birth_data=_build_birth_data(req.birth_data),
        current_location=_build_location(req.current_location),
        human_design_type=req.human_design_type or existing.human_design_type,
        human_design_strategy=req.human_design_strategy or existing.human_design_strategy,
        human_design_authority=req.human_design_authority or existing.human_design_authority,
        life_path_number=existing.life_path_number,
        metadata=existing.metadata,
    )
    updated.save(_PROFILES_DIR)
    return ProfileOut.from_profile(updated)


@router.delete("/profiles/{name}", status_code=204)
def delete_profile(name: str):
    """Delete a profile."""
    filepath = _PROFILES_DIR / f"{name}.yaml"
    if not filepath.exists():
        raise HTTPException(status_code=404, detail=f"Profile '{name}' not found")
    filepath.unlink()


# ===================================================================
# Export routes
# ===================================================================

@router.post("/export/pdf")
def export_to_pdf(req: ExportRequest):
    """Export date range as PDF."""
    profile = _load_profile(req.profile_name)
    entries = _generate_entries(profile, req.start_date, req.end_date)

    out = Path(tempfile.mktemp(suffix=".pdf"))
    export_pdf(entries, out)
    return FileResponse(
        out,
        media_type="application/pdf",
        filename=f"skyforge_{req.profile_name}_{req.start_date}_{req.end_date}.pdf",
    )


@router.post("/export/csv")
def export_to_csv(req: ExportRequest):
    """Export date range as CSV."""
    profile = _load_profile(req.profile_name)
    entries = _generate_entries(profile, req.start_date, req.end_date)

    out = Path(tempfile.mktemp(suffix=".csv"))
    export_csv(entries, out)
    return FileResponse(
        out,
        media_type="text/csv",
        filename=f"skyforge_{req.profile_name}_{req.start_date}_{req.end_date}.csv",
    )


@router.post("/export/excel")
def export_to_excel(req: ExportRequest):
    """Export date range as Excel workbook."""
    profile = _load_profile(req.profile_name)
    entries = _generate_entries(profile, req.start_date, req.end_date)

    out = Path(tempfile.mktemp(suffix=".xlsx"))
    export_excel(entries, out)
    return FileResponse(
        out,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"skyforge_{req.profile_name}_{req.start_date}_{req.end_date}.xlsx",
    )
