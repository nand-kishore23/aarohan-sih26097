from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Aarohan backend is healthy"}

def test_api_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Aarohan backend is healthy"}


def test_cors_allows_aarohan_vercel_origins():
    for origin in (
        "https://aarohan-sih26097.vercel.app",
        "https://aarohan-sih26097-q7mhmrkrp-anvesh10.vercel.app",
    ):
        response = client.get("/health", headers={"Origin": origin})
        assert response.headers["access-control-allow-origin"] == origin


def test_cors_rejects_unrelated_vercel_origins():
    response = client.get("/health", headers={"Origin": "https://unrelated.vercel.app"})
    assert "access-control-allow-origin" not in response.headers
