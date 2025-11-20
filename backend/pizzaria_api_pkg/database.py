from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv
from dotenv import load_dotenv
import os

load_dotenv()

# Usar caminho absoluto para o banco de dados
db_path = getenv("DATABASE_URL")
if not db_path or db_path.startswith("sqlite"):
    # Se não houver DATABASE_URL ou for sqlite, usar caminho relativo ao backend
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_file = os.path.join(backend_dir, "pizzaria.db")
    DATABASE_URL = f"sqlite:///{db_file}"
else:
    DATABASE_URL = db_path

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
