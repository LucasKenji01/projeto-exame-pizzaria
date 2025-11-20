from sqlalchemy.orm import Session
from pizzaria_api_pkg.core_models import Pagamento, Pedido

def registrar_pagamento(db: Session, pedido_id: int, forma_pagamento: str, valor: float):
    pedido = db.query(Pedido).filter_by(id=pedido_id).first()
    if not pedido:
        raise ValueError("Pedido não encontrado")

    if valor <= 0 or valor != pedido.valor_total:
        raise ValueError("Valor inválido")

    pagamento = Pagamento(
        pedido_id=pedido_id,
        forma_pagamento=forma_pagamento,
        valor=valor,
        status="confirmado"
    )
    db.add(pagamento)
    db.commit()
    return pagamento
