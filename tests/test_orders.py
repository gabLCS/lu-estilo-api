
def test_create_order(auth_client):
    response = auth_client.post("/orders", json={
        "client_id": 3,
        "items": [
            {"product_id": 3, "quantity": 1}
        ]
    })
    assert response.status_code in [200, 201]


