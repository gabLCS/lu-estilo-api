from fastapi.testclient import TestClient
from app.main import app

def test_register_and_login_users():
    client = TestClient(app)

    # Registrar cliente
    response = client.post("/auth/register", json={
        "username": "clienteuser",
        "email": "cliente@luestilo.com",
        "password": "cliente123",
        "is_admin": False
    })
    assert response.status_code in [200, 400]

    # Registrar admin
    response = client.post("/auth/register", json={
        "username": "adminuser",
        "email": "admin@luestilo.com",
        "password": "admin123",
        "is_admin": True
    })
    assert response.status_code in [200, 400]

    # Login cliente 
    response = client.post("/auth/login", data={
        "username": "clienteuser",
        "password": "cliente123",
        "grant_type": "password"
    })
    assert response.status_code == 200, f"Erro login cliente: {response.text}"
    token_cliente = response.json().get("access_token")
    assert token_cliente is not None

    # Login admin 
    response = client.post("/auth/login", data={
        "username": "adminuser",  
        "password": "admin123",
        "grant_type": "password"
    })
    assert response.status_code == 200, f"Erro login admin: {response.text}"
    token_admin = response.json().get("access_token")
    assert token_admin is not None
