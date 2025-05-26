from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(BaseModel):
    client_id: int
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    client_id: int
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)

def test_create_order(auth_client):
    response = auth_client.post("/orders", json={
        "client_id": 1,
        "items": [
            {"product_id": 1, "quantity": 1}
        ]
    })
    assert response.status_code in [200, 201]
