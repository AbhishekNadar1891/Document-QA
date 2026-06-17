import os
import tempfile
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_invalid_extension():
    with tempfile.NamedTemporaryFile(suffix=".exe") as tmp:
        tmp.write(b"test")
        tmp.flush()
        response = client.post(
            "/documents/upload",
            files={"file": ("test.exe", open(tmp.name, "rb"), "application/octet-stream")},
        )
    assert response.status_code == 415
