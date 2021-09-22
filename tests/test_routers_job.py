from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# ************************************
# ********** Jobs Tests **************
# ************************************


def test_routes_read_jobs():
    response = client.get("/jobs/?token=jessica", headers={"X-Token": "fake-super-secret-token"})
    assert response.status_code == 200
    assert response.json() == {"7f644301-e3f1-4752-90d5-99fbfad95uh8": {
                "id": "7f644301-e3f1-4752-90d5-99fbfad95uh8",
                "active" : True,
                "assigned" : False,
                "client_id" : 'client_guid',
                "date_required" : "01/01/22",
                "time_required" : "13:45",
                "assigned_to" : "",
                "assigned_on" : "",
                "worksheet" : "",
                },
               "7f644301-e3f1-4752-90d5-99fbfad99xx9":{
                "id": "7f644301-e3f1-4752-90d5-99fbfad99xx9",
                "active" : True,
                "assigned" : True,
                "client_id" : 'client_guid',
                "date_required" : "01/01/22",
                "time_required" : "13:45",
                "assigned_to" : "customer_guid",
                "assigned_on" : "10/10/21",
                "worksheet" : "7f644301-e3f1-4752-90d5-99fbabc12xx3",
               }}

def test_routes_read_jobs_err_token():
    response = client.get("jobs/?token=jess")
    assert response.status_code == 400
    assert response.json() == {'detail': 'No Jessica token provided'}
  