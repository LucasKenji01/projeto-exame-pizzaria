from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import Counter
from pizzaria_api_pkg.core_models import Pedido

def relatorio_vendas(db: Session):
    total = db.query(func.sum(Pedido.valor_total)).scalar() or 0
    pedidos = db.query(func.count(Pedido.id)).scalar() or 0
    return {
        "total_vendido": round(total, 2),
        "total_pedidos": pedidos
    }

def nomes_pizzas_mais_vendidas(db: Session):
    pedidos = db.query(Pedido).all()
    contador = Counter()

    for pedido in pedidos:
        for item in pedido.itens:
            if item.produto and item.produto.nome:
                contador[item.produto.nome] += item.quantidade
            elif item.produto_personalizado and item.produto_personalizado.nome:
                contador[item.produto_personalizado.nome] += item.quantidade

    mais_vendidas = [nome for nome, _ in contador.most_common(30)]
    return mais_vendidas
