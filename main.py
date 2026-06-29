from api import usuarios, pedidos, pagamentos, auth
from fastapi import FastAPI
from infrastructure.database import engine, Base
from domain import models

# 1. Usuarios
from api import usuarios 

# 2. Cria as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Raízes do Nordeste", version="1.0.0")

# 3. API
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)

@app.get("/")
def teste_inicial():
    return {"mensagem": "Bem-vindo ao restaurante Raizes do Nordeste!"}