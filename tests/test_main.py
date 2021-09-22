#!/usr/bin/env python3
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/?token=jessica")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Bigger Applications!"}
