from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ************************************
# ******** Customer Tests ************
# ************************************

def test_routes_read_customers():
    response = client.get("/customers/?token=jessica", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    print(f"ALL CUSTOMERS : {response.json()}")
    assert response.json() == {'profile': {'password': 'Secret_Pa55w0rd', 'signup_ts': 1627660300.9757571, 'RegisteredAddress': 'DT1 1SS', 'joined': 'Fri Jul 30 16:51:40 2021', 'services': [1, 3, 4], 'AreasCovered': ['DT1', 'DT2'], 'id': '64703c74-4663-4e97-9038-7b74754555eb', 'CompanyReg': '0921343', 'WorkingDays': [1, 2, 3, 4, 5, 6, 0]}, 'query': '\n    match (customer:CUSTOMER) return customer as clt\n    '}

def test_routes_read_customers_err_token():
    response = client.get("/customers/?token=jess", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'No Jessica token provided'}

def test_routes_read_customers_err_header():
    response = client.get("/customers/?token=jessica", headers={"X-Token": "fake-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'X-Token header invalid'}


def test_read_customer_profile():
    id = "64703c74-4663-4e97-9038-7b74754555eb"
    response = client.get("/customers/"+id+"?token=jessica", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    print(f"CUSTOMER : {response.json()}")
    assert response.json() == {'64703c74-4663-4e97-9038-7b74754555eb': {'password': 'Secret_Pa55w0rd', 'signup_ts': 1627660300.9757571, 'RegisteredAddress': 'DT1 1SS', 'joined': 'Fri Jul 30 16:51:40 2021', 'services': [1, 3, 4], 'AreasCovered': ['DT1', 'DT2'], 'id': '64703c74-4663-4e97-9038-7b74754555eb', 'CompanyReg': '0921343', 'WorkingDays': [1, 2, 3, 4, 5, 6, 0]}}
    