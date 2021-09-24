from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
# ************************************
# ******** Clients  Tests ************
# ************************************


def test_routes_read_clients():
    response = client.get("/clients/?token=jessica",
                          headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    print(f"\n\nAll Clients = {response.json()}")
    assert response.json() == {
        'profile':
            {'password': 'Secret_Pa55w0rd',
                'signup_ts': 1632390306.911037,
                'joined': 'Thu Sep 23 10:45:06 2021',
                'name': 'Jane Doe', 'houseNumber': 23,
                'location': 'DT1 1SS', 'JobSheet': [],
                'id': '478ea65d-afc4-434f-800a-bb50cecb90eb',
                'status': True},
        'query': '\n    match (client:CLIENT) return client as clt\n    '
    }


def test_routes_find_clients():
    id = '478ea65d-afc4-434f-800a-bb50cecb90eb'
    response = client.get("/clients/"+id+"?token=jessica",
                          headers={"X-Token": "fake-super-secret-token"})
    print(f"JSON = {response.json()}")
    assert response.status_code == 200
    assert response.json() == {
        '478ea65d-afc4-434f-800a-bb50cecb90eb':
            {'password': 'Secret_Pa55w0rd',
             'signup_ts': 1632390306.911037,
             'joined': 'Thu Sep 23 10:45:06 2021',
             'name': 'Jane Doe', 'houseNumber': 23,
             'location': 'DT1 1SS', 'JobSheet': [],
             'id': '478ea65d-afc4-434f-800a-bb50cecb90eb',
             'status': True}
    }


def test_routes_read_clients_err_token():
    response = client.get("/clients/?token=jess",
                          headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'No Jessica token provided'}


def test_routes_read_clients_err_header():
    response = client.get("/clients/?token=jessica",
                          headers={"X-Token": "fake-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'X-Token header invalid'}


def test_routes_register_clients():
    response = client.post("/clients/registration/?token=jessica",
                           headers={"X-Token": "fake-secret-token"})
)
