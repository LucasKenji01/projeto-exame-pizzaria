from sqlalchemy.orm import Session
from sqlalchemy import func
from pizzaria_api_pkg.models import Pedido, ItemPedido, Produto

def vendas_por_periodo(db: Session, periodo: str):
    """✅ CORRIGIDO: Retorna lista de dicts consistente"""
    trunc_map = {
        "diario": "day",
        "semanal": "week",
        "mensal": "month",
        "anual": "year"
    }
    trunc = trunc_map.get(periodo, "month")

    # Query corrigida
    resultados = db.query(
        Produto.nome.label("pizza"),
        func.date_trunc(trunc, Pedido.data_pedido).label("periodo"),
        func.sum(ItemPedido.quantidade).label("quantidade")
    ).select_from(ItemPedido)\
     .join(Pedido, ItemPedido.pedido_id == Pedido.id)\
     .join(Produto, ItemPedido.produto_id == Produto.id)\
     .filter(Pedido.status != 'cancelado')\
     .group_by(Produto.nome, func.date_trunc(trunc, Pedido.data_pedido))\
     .order_by(func.date_trunc(trunc, Pedido.data_pedido).desc())\
     .all()
    
    # ✅ SEMPRE retornar lista de dicts
    return [
        {
            "pizza": r.pizza,
            "periodo": r.periodo.strftime("%Y-%m-%d") if r.periodo else "Sem data",
            "quantidade": int(r.quantidade) if r.quantidade else 0
        }
        for r in resultados if r.periodo is not None
    ]
