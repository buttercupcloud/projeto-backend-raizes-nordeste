from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. A "string de conexão" com o seu MySQL.
# ATENÇÃO: Altere 'sua_senha' para a senha real do seu MySQL Workbench!
# (Se o seu banco não tiver senha, deixe vazio assim: root:@localhost)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/raizes_db"

# 2. Criando o "motor" que conecta o Python ao banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Criando a "fábrica" de conversas com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. A classe base que vai nos ajudar a desenhar as tabelas depois
Base = declarative_base()

# 5. Função para abrir a porta do banco, usar e fechar em segurança
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()