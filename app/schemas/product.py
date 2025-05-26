from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date

class ProductBase(BaseModel):
    description: str
    sale_price: float
    barcode: str
    section: str
    stock: int
    expiration_date: Optional[date] = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
