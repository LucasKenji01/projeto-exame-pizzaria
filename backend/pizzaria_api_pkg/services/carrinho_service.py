from sqlalchemy.orm import Session
from pizzaria_api_pkg.core_models import Carrinho, Produto, PizzaPersonalizada

def adicionar_item_carrinho(db: Session, cliente_id: int, produto_id: int = None, produto_personalizado_id: int = None, quantidade: int = 1):
    if quantidade <= 0:
        raise ValueError("Quantidade deve ser maior que zero")

    if not produto_id and not produto_personalizado_id:
        raise ValueError("Produto ou pizza personalizada deve ser informado")

    if produto_id:
        if not db.query(Produto).filter_by(id=produto_id, ativo=True).first():
            raise ValueError("Produto não encontrado ou inativo")

    if produto_personalizado_id:
        if not db.query(PizzaPersonalizada).filter_by(id=produto_personalizado_id).first():
            raise ValueError("Pizza personalizada não encontrada")

    item = Carrinho(
        cliente_id=cliente_id,
        produto_id=produto_id,
        produto_personalizado_id=produto_personalizado_id,
        quantidade=quantidade
    )
    db.add(item)
    db.commit()
    return item
