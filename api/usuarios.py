from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from domain import models, schemas
from passlib.context import CryptContext

# Criamos um "balcão" exclusivo para atender assuntos de usuários
router = APIRouter()

# Ferramenta que vai criptografar a senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/usuarios")
def criar_usuario(usuario: schemas.UsuarioCriar, db: Session = Depends(get_db)):
    senha_criptografada= pwd_context.hash(usuario.senha)

  
    # 1. Pegamos o bilhetinho do cliente e transformamos no Molde do Banco de Dados
    novo_usuario = models.Usuario(
        nome=usuario.nome,
        cpf=usuario.cpf,
        senha_hash=senha_criptografada, # salvando o hash e não a senha real
        perfil_role=usuario.perfil_role,
        consentimento=usuario.consentimento
    )
    
    # 2. Mandamos o banco de dados salvar!
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    # 3. Devolvemos a resposta de sucesso
    return {"mensagem": "Usuário criado com sucesso!", "id_gerado": novo_usuario.id_usuario}