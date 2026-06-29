from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from domain import models, schemas
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Chave secreta para assinar o token (Em projetos reais, ficaria escondida)
SECRET_KEY = "chave_secreta_projeto_raizes" 

@router.post("/auth/login")
def login(requisicao: schemas.LoginRequest, db: Session = Depends(get_db)):
    
    # 1. Procura o usuário pelo CPF no banco
    usuario = db.query(models.Usuario).filter(models.Usuario.cpf == requisicao.cpf).first()
    
    # 2. Verifica se o usuário existe e se a senha bate com o Hash
    if not usuario or not pwd_context.verify(requisicao.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="CPF ou senha inválidos.") # Erro 401 exigido no manual
        
    # 3. Criando o Token JWT válido, inserindo a Role (perfil) dentro dele
    expiracao = datetime.utcnow() + timedelta(hours=2)
    payload = {
        "sub": usuario.cpf,
        "role": usuario.perfil_role, # Verificação de Perfis (Roles)
        "exp": expiracao
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    # Retorno exato no formato exigido pelo manual do projeto
    return {
        "accessToken": token,
        "tokenType": "Bearer",
        "user": {
            "id": usuario.id_usuario,
            "nome": usuario.nome,
            "perfil": usuario.perfil_role
        }
    }
@router.get("/admin/relatorios")
def relatorio_gerencial(authorization: str = Header(default=None)):
    
    # 1. Se não mandar token nenhum, dá Erro 401 (Teste T03)
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido.")
    
    try:
        # Limpa o texto "Bearer " para ler só o código do Token
        token = authorization.replace("Bearer ", "")
        
        # 2. Descriptografa o token e descobre qual é o perfil (role) da pessoa
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        perfil_usuario = payload.get("role")
        
        # 3. REGRA DE PERMISSÃO: Se não for Gerente ou Admin, dá Erro 403 (Teste T04)
        if perfil_usuario not in ["GERENTE", "ADMIN"]:
            raise HTTPException(status_code=403, detail="Acesso negado. Apenas gerentes podem ver isso.")
            
        return {"mensagem": "Bem-vindo à área gerencial! Aqui estão os relatórios."}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido.")