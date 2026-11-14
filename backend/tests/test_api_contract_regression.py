"""Hardware-free FastAPI contract regression tests.

No ESP32, network scan, site measurement, or hardware control.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID = {
    "device_id": "SCOUT-TEST-01",
    "zone_id": "ZONE-TEST",
    "ssid": "Lab-Test",
    "bssid": "AA:BB:CC:DD:EE:FF",
    "rssi": -64,
    "channel": 6,
}

def test_root_contract():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "SiteLink Scout API"

def test_health_contract():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "sitelink-scout-api"}

def test_measurement_missing_required_fields_is_rejected():
    response = client.post("/api/v1/measurements", json={})
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.parametrize("field,value", [
    ("rssi", -128), ("rssi", 1), ("channel", 0), ("channel", 15),
    ("device_id", ""), ("zone_id", ""), ("ssid", ""), ("bssid", ""),
])
def test_measurement_contract_rejects_invalid_input(field, value):
    payload = {**VALID, field: value}
    response = client.post("/api/v1/measurements", json=payload)
    assert response.status_code == 422, (field, value, response.text)
