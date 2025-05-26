from fastapi import FastAPI
from app.routers import client, auth, product, order
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


app = FastAPI(
    title="LuEstilo API",
    description="API para gerenciamento de clientes, produtos e pedidos da empresa Lu Estilo.",
    version="1.0.0"
)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(auth.router)
app.include_router(client.router)
app.include_router(order.router)
app.include_router(product.router)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API da Lu Estilo!"}
