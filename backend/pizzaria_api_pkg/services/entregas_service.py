from sqlalchemy.orm import Session
from pizzaria_api_pkg.core_models import Entrega

def listar_entregas_funcionario(db: Session, funcionario_id: int):
    return db.query(Entrega).filter_by(funcionario_id=funcionario_id).all()
