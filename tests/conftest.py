import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def auth_client():
    client = TestClient(app)


    client.post("/auth/register", json={
        "username": "tester",
        "email": "tester@example.com",
        "password": "senha123"
    })


    response = client.post("/auth/login", data={
        "username": "adminuser",
        "password": "admin123",
        "grant_type": "password"
    })

    token = response.json().get("access_token")
    assert token, "Token JWT não foi retornado"


    client.headers.update({"Authorization": f"Bearer {token}"})

    print("Token:", token)
    print("Headers:", client.headers)

    return client

