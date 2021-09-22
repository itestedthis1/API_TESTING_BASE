from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ************************************
# ******** Clients  Tests ************
# ************************************

def test_routes_read_clients():
    response = client.get("/clients/?token=jessica", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    print(f"\n\nAll Clients = {response.json()}")
    assert response.json() == {'profile': {'password': 'Secret_Pa55w0rd', 'signup_ts': 1627660300.8488379, 'joined': 'Fri Jul 30 16:51:40 2021', 'name': 'Jane Doe', 'houseNumber': 23, 'location': 'DT1 1SS', 'JobSheet': [], 'id': 'ec86adf9-a0dd-4026-bc2d-d4e61728e0e4', 'status': True}, 'query': '\n    match (client:CLIENT) return client as clt\n    '}

def test_routes_find_clients():
    id='ec86adf9-a0dd-4026-bc2d-d4e61728e0e4'
    response = client.get("/clients/"+id+"?token=jessica", headers={"X-Token": "fake-super-secret-token"})
    print(f"JSON = {response.json()}")
    assert response.status_code == 200
    assert response.json() == {'ec86adf9-a0dd-4026-bc2d-d4e61728e0e4': {'password': 'Secret_Pa55w0rd', 'signup_ts': 1627660300.8488379, 'joined': 'Fri Jul 30 16:51:40 2021', 'name': 'Jane Doe', 'houseNumber': 23, 'location': 'DT1 1SS', 'JobSheet': [], 'id': 'ec86adf9-a0dd-4026-bc2d-d4e61728e0e4', 'status': True}}
                                              
def test_routes_read_clients_err_token():
    response = client.get("/clients/?token=jess", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'No Jessica token provided'}

def test_routes_read_clients_err_header():
    response = client.get("/clients/?token=jessica", headers={"X-Token": "fake-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'X-Token header invalid'}
