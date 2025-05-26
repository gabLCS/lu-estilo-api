from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    phone_number: Optional[str] = None

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    phone_number: Optional[str] = None

class ClientResponse(ClientBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
