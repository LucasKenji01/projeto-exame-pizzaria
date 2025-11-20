from sqlalchemy.orm import Session
from pizzaria_api_pkg.core_models import Pedido

def relatorio_pedidos_cliente(db: Session, cliente_id: int):
    return db.query(Pedido).filter_by(cliente_id=cliente_id).all()
