from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_devices():
    response = client.get("/api/v1/devices")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_unknown_device():
    response = client.get(
        "/api/v1/devices/DOES-NOT-EXIST"
    )

    assert response.status_code == 404
