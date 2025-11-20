from sqlalchemy.orm import Session
from pizzaria_api_pkg.core_models import Carrinho, ItemPedido, Pedido

VALID_STATUSES = {"pendente", "em_preparo", "em_entrega", "finalizado", "cancelado"}

def atualizar_status_pedido(db: Session, pedido_id: int, novo_status: str):
    if novo_status not in VALID_STATUSES:
        raise ValueError("Status inválido")

    pedido = db.query(Pedido).filter_by(id=pedido_id).first()
    if not pedido:
        return None
    pedido.status = novo_status
    db.commit()
    return pedido

def gerar_pedido_do_carrinho(db: Session, cliente_id: int, email: str):
    itens_carrinho = db.query(Carrinho).filter_by(cliente_id=cliente_id).all()
    if not itens_carrinho:
        raise ValueError("Carrinho vazio")

    valor_total = 0
    quantidade_total = 0
    itens_pedido = []

    for item in itens_carrinho:
        preco = item.produto.preco if item.produto else item.produto_personalizado.preco_base
        valor_item = preco * item.quantidade
        valor_total += valor_item
        quantidade_total += item.quantidade
        itens_pedido.append(ItemPedido(
            produto_id=item.produto_id,
            produto_personalizado_id=item.produto_personalizado_id,
            quantidade=item.quantidade,
            preco_unitario=preco,
            preco_total=valor_item
        ))

    pedido = Pedido(
        cliente_id=cliente_id,
        email=email,
        descricao="Pedido gerado automaticamente",
        quantidade=quantidade_total,
        valor_total=valor_total,
        status="pendente"
    )
    db.add(pedido)
    db.flush()

    for item in itens_pedido:
        item.pedido_id = pedido.id
        db.add(item)

    db.query(Carrinho).filter_by(cliente_id=cliente_id).delete()
    db.commit()
    return pedido
