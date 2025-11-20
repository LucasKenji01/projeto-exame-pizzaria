from sqlalchemy.orm import Session
from pizzaria_api_pkg import models

def get_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()
