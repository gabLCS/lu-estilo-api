from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.models.product import Product
from app.models.user import User
from typing import List, Optional
from sqlalchemy import and_
from app.core.dependencies import get_current_user
import os
from app.core.dependencies import require_admin
from datetime import date
import shutil
router = APIRouter(prefix="/products", tags=["Products"])
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/{id}", response_model=ProductResponse)
def get_product(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.query(Product).get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.put("/{id}", response_model=ProductResponse)
def update_product(id: int, updated: ProductUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.query(Product).get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in updated.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    product = db.query(Product).get(id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(product)
    db.commit()
    return {"detail": "Produto removido com sucesso"}


@router.get("/", response_model=List[ProductResponse])
def list_products(
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    section: Optional[str] = Query(None),
    in_stock: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = db.query(Product)

    if min_price is not None:
        query = query.filter(Product.sale_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.sale_price <= max_price)
    if section:
        query = query.filter(Product.section.ilike(f"%{section}%"))
    if in_stock is not None:
        if in_stock:
            query = query.filter(Product.stock > 0)
        else:
            query = query.filter(Product.stock <= 0)

    return query.all()

@router.post("/", response_model=ProductResponse)
def create_product_upload(
    description: str = Form(...),
    sale_price: float = Form(...),
    barcode: str = Form(...),
    section: str = Form(...),
    stock: int = Form(...),
    expiration_date: Optional[date] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(require_admin)
):
    image_url = None
    if image:
        image_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/{UPLOAD_DIR}/{image.filename}"

    product = Product(
        description=description,
        sale_price=sale_price,
        barcode=barcode,
        section=section,
        stock=stock,
        expiration_date=expiration_date,
        image_url=image_url
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product