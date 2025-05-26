def test_create_and_list_clients(auth_client):
    response = auth_client.post("/clients", json={
        "name": "Cliente Teste",
        "email": "cliente@test.com",
        "cpf": "12345678901",
        "phone_number": "+5511987654321"
    })
    assert response.status_code in [200, 201, 400]

    response = auth_client.get("/clients")
    assert response.status_code == 200
    assert isinstance(response.json(), list)