from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. String de conexão MySQL.
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/raizes_db"

# 2. Conecta o Python ao banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Conversas com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. A classe base 
Base = declarative_base()

# 5. Função para porta do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()