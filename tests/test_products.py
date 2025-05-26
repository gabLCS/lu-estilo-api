import uuid

def test_create_product(auth_client):
    unique_barcode = f"PROD-TENIS-{uuid.uuid4().hex[:6]}"
    response = auth_client.post("/products", data={
    "description": "Tênis Esportivo",
    "sale_price": 199.90,
    "barcode": unique_barcode,
    "section": "Calçados",
    "stock": 20
})
    assert response.status_code in [200, 201, 400], f"Erro ao criar produto: {response.text}"
    data = response.json()
    
    if response.status_code in [200, 201]:
        assert "id" in data
        assert data["description"] == "Tênis Esportivo"

def test_list_products(auth_client):
    response = auth_client.get("/products")
    assert response.status_code == 200, f"Erro ao listar produtos: {response.text}"
    assert isinstance(response.json(), list)
