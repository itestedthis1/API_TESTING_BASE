#!/usr/bin/env python3
from .gdb.data_models.client import User

client_data = {
    "id": "7f644301-e3f1-4752-90d5-99fbfad91ab4",
    "name" : 'John Doe',
    "houseNumbber" : 23,
    "location" : "DT1 1SS",
    "password" : "Secret_Pa55w0rd",
    "signup_ts": None,
    "JobSheet": ["79dc3d3a-c40b-47e8-8cf4-207c2de7e36","c85a5633-2803-4826-ae5a-82474c238d5","0348ae36-202a-4bfc-a92d-849607fd541" ]
}

def test_client_model():
    user = User(**client_data)

    assert client_data["id"] == user.id
    assert client_data["JobSheet"] == user.JobSheet    