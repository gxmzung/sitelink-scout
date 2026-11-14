"""Hardware-free HTTP contract smoke checks.

This uses the existing FastAPI TestClient; it does not scan Wi-Fi or
establish an ESP32 link.
"""
from fastapi.testclient import TestClient

from app.main import app


def test_root_contract():
    response = TestClient(app).get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "SiteLink Scout API"


def test_health_contract():
    response = TestClient(app).get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "sitelink-scout-api",
    }


def test_measurement_missing_required_fields_is_rejected():
    response = TestClient(app).post("/api/v1/measurements", json={})
    assert response.status_code == 422
    assert "detail" in response.json()
