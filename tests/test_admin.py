from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_read_admin():
    response = client.post("/admin/?token=jessica", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Admin getting schwifty"
    }

def test_read_admin_err_token():
    response = client.post("/admin/?token=jess", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'No Jessica token provided'}

def test_read_admin_err_header():
    response = client.post("/admin/?token=jessica", headers={"X-Token": "fake-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'X-Token header invalid'}