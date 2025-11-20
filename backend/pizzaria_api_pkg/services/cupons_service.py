from sqlalchemy.orm import Session
from pizzaria_api_pkg.core_models import Pedido, Cupom
from datetime import date

def aplicar_cupom(db: Session, pedido_id: int, cliente_id: int, codigo: str):
    pedido = db.query(Pedido).filter_by(id=pedido_id, cliente_id=cliente_id).first()
    if not pedido:
        return None, "Pedido não encontrado"

    cupom = db.query(Cupom).filter_by(codigo=codigo, ativo=True).first()
    if not cupom or (cupom.validade and cupom.validade < date.today()):
        return None, "Cupom inválido ou expirado"

    desconto = pedido.valor_total * (cupom.percentual_desconto / 100)
    pedido.valor_total -= desconto
    db.commit()
    return pedido, None
