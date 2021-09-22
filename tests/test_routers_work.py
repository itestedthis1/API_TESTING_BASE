from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ************************************
# ********* Works Tests **************
# ************************************



def test_routes_read_item():
    response = client.get("/works/?token=jessica", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == {
  "plumbus": {
    "name": "Plumbus"
  },
  "gun": {
    "name": "Portal Gun"
  }
}

def test_routes_read_item_err_token():
    response = client.get("/works/?token=jesa", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'No Jessica token provided'}

def test_routes_read_item_err_header():
    response = client.get("/works/?token=jessica", headers={"X-Token": "fake-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'X-Token header invalid'}
