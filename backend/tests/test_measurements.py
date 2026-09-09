from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_measurement():
    payload = {
        "device_id": "SCOUT-01",
        "zone_id": "ZONE-B03",
        "ssid": "SiteLink_AP_01",
        "bssid": "AA:BB:CC:DD:EE:FF",
        "rssi": -64,
        "channel": 6,
    }

    response = client.post(
        "/api/v1/measurements",
        json=payload,
    )

    assert response.status_code == 201

    body = response.json()

    assert body["device_id"] == "SCOUT-01"
    assert body["zone_id"] == "ZONE-B03"
    assert body["rssi"] == -64
    assert "id" in body
    assert "received_at" in body


def test_list_measurements():
    response = client.get(
        "/api/v1/measurements"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
