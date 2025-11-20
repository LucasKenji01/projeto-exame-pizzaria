from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.core_models import Produto, ItemPedido

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/nuvem-sabores-json")
def nuvem_sabores_json(db: Session = Depends(get_db)):
    # Consulta os sabores com vendas
    vendidos = (
        db.query(Produto.id, Produto.nome, func.count(ItemPedido.id).label("total"))
        .join(ItemPedido, ItemPedido.produto_id == Produto.id)
        .filter(Produto.ativo == True)
        .group_by(Produto.id, Produto.nome)
        .all()
    )

    # Monta dicionário com (id, nome) como chave e total como peso
    frequencias = { (id, nome): total for id, nome, total in vendidos if total > 0 }

    # ✅ CORREÇÃO: fallback com id e nome, não apenas nome
    if not frequencias:
        ativos = db.query(Produto.id, Produto.nome).filter(Produto.ativo == True).all()
        frequencias = { (id, nome): 1 for id, nome in ativos }

    # Retorna lista de objetos para o frontend
    return [{"id": id, "sabor": nome, "peso": peso} for (id, nome), peso in frequencias.items()]
