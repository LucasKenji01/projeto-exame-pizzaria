from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.services.relatorios_service import (
    relatorio_vendas,
    nomes_pizzas_mais_vendidas
)
from pizzaria_api_pkg.services.relatorios_service import vendas_por_mes
from fastapi import Body
from typing import List
from datetime import datetime
from pizzaria_api_pkg.core_models import Produto, Pedido, ItemPedido
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from sqlalchemy import func

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/vendas")
def vendas(db: Session = Depends(get_db)):
    return relatorio_vendas(db)

# ✅ Mantido para compatibilidade com frontend
@router.get("/nuvem-sabores-lista-json")
def nuvem_sabores(db: Session = Depends(get_db)):
    return nomes_pizzas_mais_vendidas(db)


@router.get("/vendas-mes")
def vendas_mes(ano: int | None = None, db: Session = Depends(get_db)):
    """Retorna uma lista com 12 números representando quantidade de pizzas vendidas por mês no ano indicado (ou ano atual)."""
    return vendas_por_mes(db, ano)


@router.post('/seed-vendas')
def seed_vendas(
    ano: int | None = None,
    valores: List[int] | None = Body(default=None),
    replace: bool = False,
    db: Session = Depends(get_db)
):
    """Popula a base com pedidos de teste distribuídos por mês.

    Body `valores` (opcional): lista de 12 inteiros com vendas por mês.
    Se não informado, usa valores exemplo.
    """
    if ano is None:
        ano = datetime.now().year

    # valores padrão (meses Jan..Dec)
    default = [120, 95, 110, 150, 200, 180, 170, 160, 140, 130, 125, 190]
    counts = valores if (valores and len(valores) == 12) else default

    # se replace=True, remover pedidos de seed anteriores para tornar o seed idempotente
    if replace:
        try:
            deleted = db.query(Pedido).filter(Pedido.email == 'seed@example.com').delete(synchronize_session=False)
            db.commit()
        except Exception:
            db.rollback()

    # garantir alguns produtos de exemplo
    produtos = db.query(Produto).limit(5).all()
    if len(produtos) < 3:
        exemplos = [
            {'nome': 'Margherita', 'preco': 25.0},
            {'nome': 'Calabresa', 'preco': 30.0},
            {'nome': 'Portuguesa', 'preco': 32.5},
        ]
        for ex in exemplos:
            p = Produto(nome=ex['nome'], preco=ex['preco'], descricao='', ativo=True)
            db.add(p)
        db.commit()
        produtos = db.query(Produto).limit(5).all()

    resumo = []
    for month_index, target in enumerate(counts, start=1):
        created = 0
        for i in range(target):
            # escolher um produto cíclico
            prod = produtos[(i) % len(produtos)]
            # criar pedido
            dia = min(28, (i % 27) + 1)
            data = datetime(ano, month_index, dia, 12, 0, 0)
            pedido = Pedido(
                descricao=f'Pedido seed {ano}-{month_index:02d}',
                quantidade=1,
                valor_total=prod.preco,
                email='seed@example.com',
                data_pedido=data,
                status='Finalizado'
            )
            db.add(pedido)
            db.flush()  # para obter pedido.id

            item = ItemPedido(
                pedido_id=pedido.id,
                produto_id=prod.id,
                quantidade=1,
                preco_unitario=prod.preco,
                preco_total=prod.preco
            )
            db.add(item)
            created += 1

        db.commit()
        resumo.append({'mes': month_index, 'created': created})

    return {'ano': ano, 'resumo': resumo}
