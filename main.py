from api import usuarios, pedidos, pagamentos, auth
from fastapi import FastAPI
from infrastructure.database import engine, Base
# É esta linha abaixo que avisa o Python que existem tabelas novas para criar!
from domain import models

# 1. Nova linha: Importamos a nossa janelinha de usuários!
from api import usuarios 

# ESSA É A LINHA MÁGICA: Ela vai no MySQL e cria as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Raízes do Nordeste", version="1.0.0")

# 2. Nova linha: Ligamos a janelinha no restaurante!
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(pedidos.router)
app.include_router(pagamentos.router)

@app.get("/")
def teste_inicial():
    return {"mensagem": "Bem-vindo ao restaurante Raizes do Nordeste!"}