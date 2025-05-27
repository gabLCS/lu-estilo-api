from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderResponse
from typing import List, Optional
from datetime import date
from app.models.user import User
from app.core.dependencies import get_current_user
from app.services.whatsapp import send_whatsapp_message
from app.models.client import Client

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    items = []
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produto {item.product_id} não encontrado")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para o produto {product.description}")
        product.stock -= item.quantity
        db.add(product)
        items.append(OrderItem(product_id=product.id, quantity=item.quantity, unit_price=product.sale_price))

    order = Order(client_id=order_data.client_id, items=items)
    db.add(order)
    db.commit()
    client = db.query(Client).filter(Client.id == order.client_id).first()
    if client and client.phone_number:
        try:
            send_whatsapp_message(
                to_number=client.phone_number,
                message=f"Olá {client.name}, seu pedido #{order.id} foi recebido com sucesso! 🛒")
        except Exception as e:
            print(f"[WhatsApp] Falha ao enviar mensagem: {e}")
    db.refresh(order)
    return order

@router.get("/", response_model=List[OrderResponse])
def list_orders(
    client_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = db.query(Order)

    if client_id:
        query = query.filter(Order.client_id == client_id)
    if status:
        query = query.filter(Order.status.ilike(status))
    if start_date:
        query = query.filter(Order.created_at >= start_date)
    if end_date:
        query = query.filter(Order.created_at <= end_date)

    return query.all()