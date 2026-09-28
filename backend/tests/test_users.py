from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_homepage():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "msg": "Welcome user!"
    }