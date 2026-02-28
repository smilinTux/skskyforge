"""
Tests for SkyForge FastAPI routes.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin
"""

import pytest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from skskyforge.models import BirthData, UserProfile
from skskyforge.web import create_app


@pytest.fixture
def profiles_dir(tmp_path):
    d = tmp_path / "profiles"
    d.mkdir()
    return d


@pytest.fixture
def sample_profile(profiles_dir):
    profile = UserProfile(
        name="alice",
        birth_data=BirthData(date=date(1990, 6, 15)),
    )
    profile.save(profiles_dir)
    return profile


@pytest.fixture
def client(profiles_dir):
    app = create_app()
    with patch("skskyforge.web.routers._PROFILES_DIR", profiles_dir):
        yield TestClient(app)


# -------------------------------------------------------------------
# Profile CRUD
# -------------------------------------------------------------------

class TestProfileRoutes:

    def test_list_profiles_empty(self, client):
        resp = client.get("/api/profiles")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_create_profile(self, client):
        resp = client.post("/api/profiles", json={
            "name": "bob",
            "birth_data": {"date": "1985-03-22", "time_range": "morning"},
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "bob"
        assert data["birth_date"] == "1985-03-22"
        assert data["time_range"] == "morning"

    def test_create_duplicate_profile(self, client, sample_profile):
        resp = client.post("/api/profiles", json={
            "name": "alice",
            "birth_data": {"date": "1990-06-15"},
        })
        assert resp.status_code == 409

    def test_get_profile(self, client, sample_profile):
        resp = client.get("/api/profiles/alice")
        assert resp.status_code == 200
        assert resp.json()["name"] == "alice"

    def test_get_profile_not_found(self, client):
        resp = client.get("/api/profiles/nobody")
        assert resp.status_code == 404

    def test_update_profile(self, client, sample_profile):
        resp = client.put("/api/profiles/alice", json={
            "name": "alice",
            "birth_data": {"date": "1990-06-15"},
            "human_design_type": "Projector",
        })
        assert resp.status_code == 200
        assert resp.json()["human_design_type"] == "Projector"

    def test_delete_profile(self, client, sample_profile):
        resp = client.delete("/api/profiles/alice")
        assert resp.status_code == 204
        # Verify gone
        resp = client.get("/api/profiles/alice")
        assert resp.status_code == 404

    def test_delete_profile_not_found(self, client):
        resp = client.delete("/api/profiles/nobody")
        assert resp.status_code == 404

    def test_list_profiles_after_create(self, client):
        client.post("/api/profiles", json={
            "name": "carol",
            "birth_data": {"date": "2000-01-01"},
        })
        resp = client.get("/api/profiles")
        assert resp.status_code == 200
        names = [p["name"] for p in resp.json()]
        assert "carol" in names


# -------------------------------------------------------------------
# Generation routes
# -------------------------------------------------------------------

class TestGenerateRoutes:

    def test_generate_daily(self, client, sample_profile):
        resp = client.post("/api/generate/daily", json={
            "date": "2026-03-01",
            "profile_name": "alice",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["date"] == "2026-03-01"
        assert "daily_theme" in data
        assert "moon" in data

    def test_generate_daily_profile_not_found(self, client):
        resp = client.post("/api/generate/daily", json={
            "date": "2026-03-01",
            "profile_name": "nobody",
        })
        assert resp.status_code == 404

    def test_generate_range(self, client, sample_profile):
        resp = client.post("/api/generate/range", json={
            "start_date": "2026-03-01",
            "end_date": "2026-03-03",
            "profile_name": "alice",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0]["date"] == "2026-03-01"
        assert data[2]["date"] == "2026-03-03"

    def test_generate_range_invalid_order(self, client, sample_profile):
        resp = client.post("/api/generate/range", json={
            "start_date": "2026-03-05",
            "end_date": "2026-03-01",
            "profile_name": "alice",
        })
        assert resp.status_code == 422

    def test_generate_range_too_long(self, client, sample_profile):
        resp = client.post("/api/generate/range", json={
            "start_date": "2026-01-01",
            "end_date": "2028-01-01",
            "profile_name": "alice",
        })
        assert resp.status_code == 422


# -------------------------------------------------------------------
# Export routes
# -------------------------------------------------------------------

class TestExportRoutes:

    def test_export_csv(self, client, sample_profile):
        resp = client.post("/api/export/csv", json={
            "start_date": "2026-03-01",
            "end_date": "2026-03-02",
            "profile_name": "alice",
        })
        assert resp.status_code == 200
        assert "text/csv" in resp.headers["content-type"]
        assert resp.content.startswith(b"date,")

    def test_export_pdf(self, client, sample_profile):
        resp = client.post("/api/export/pdf", json={
            "start_date": "2026-03-01",
            "end_date": "2026-03-01",
            "profile_name": "alice",
        })
        assert resp.status_code == 200
        assert resp.content[:5] == b"%PDF-"

    def test_export_excel(self, client, sample_profile):
        resp = client.post("/api/export/excel", json={
            "start_date": "2026-03-01",
            "end_date": "2026-03-01",
            "profile_name": "alice",
        })
        assert resp.status_code == 200
        assert "spreadsheetml" in resp.headers["content-type"]

    def test_export_profile_not_found(self, client):
        resp = client.post("/api/export/csv", json={
            "start_date": "2026-03-01",
            "end_date": "2026-03-01",
            "profile_name": "nobody",
        })
        assert resp.status_code == 404
