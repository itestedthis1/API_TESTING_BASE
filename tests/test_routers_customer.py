import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
# ************************************
# ******** Customer Tests ************
# ************************************


@pytest.mark.skip("Continually adding Customers - Bug")
def test_routes_read_customers():
    response = client.get("/customers/?token=jessica",
                          headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    print(f"ALL CUSTOMERS : {response.json()}")
    assert response.json() == {
        'profile': {
            'password': 'Secret_Pa55w0rd',
            'signup_ts': 1632390306.988766,
            'RegisteredAddress': 'DT1 1SS',
            'joined': 'Thu Sep 23 10:45:06 2021',
            'services': [1, 3, 4], 'AreasCovered': ['DT1', 'DT2'],
            'id': '47bfc611-872d-4f4f-b2f2-7d9e505646ec',
            'CompanyReg': '0921343',
            'WorkingDays': [1, 2, 3, 4, 5, 6, 0]},
        'query': '\n    match (customer:CUSTOMER) return customer as clt\n    '
        }


def test_routes_read_customers_err_token():
    response = client.get("/customers/?token=jess",
                          headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'No Jessica token provided'}


def test_routes_read_customers_err_header():
    response = client.get("/customers/?token=jessica",
                          headers={"X-Token": "fake-secret-token"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'X-Token header invalid'}


def test_read_customer_profile():
    id = "47bfc611-872d-4f4f-b2f2-7d9e505646ec"
    response = client.get("/customers/"+id+"?token=jessica",
                          headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    print(f"CUSTOMER : {response.json()}")
    assert response.json() == {
        '47bfc611-872d-4f4f-b2f2-7d9e505646ec': {
            'password': 'Secret_Pa55w0rd',
            'signup_ts': 1632390306.988766,
            'RegisteredAddress': 'DT1 1SS',
            'joined': 'Thu Sep 23 10:45:06 2021',
            'services': [1, 3, 4],
            'AreasCovered': ['DT1', 'DT2'],
            'id': '47bfc611-872d-4f4f-b2f2-7d9e505646ec',
            'CompanyReg': '0921343',
            'WorkingDays': [1, 2, 3, 4, 5, 6, 0]}
        }
