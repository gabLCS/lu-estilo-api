from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.client import ClientCreate, ClientResponse
from app.models.client import Client
from app.database import SessionLocal, get_db
from typing import List, Optional
from app.core.dependencies import get_current_user
from app.models.user import User
router = APIRouter(prefix="/clients", tags=["Clients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[ClientResponse])
def list_clients(
    name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    query = db.query(Client)

    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))

    return query.all()

@router.post("/", response_model=ClientResponse, status_code=201)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if db.query(Client).filter(Client.email == client.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if db.query(Client).filter(Client.cpf == client.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    new_client = Client(**client.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client