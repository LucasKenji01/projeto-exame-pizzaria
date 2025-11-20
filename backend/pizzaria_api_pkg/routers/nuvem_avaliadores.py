from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.core_models import Avaliacao, Cliente, Pedido, ItemPedido, Produto

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/nuvem-avaliadores-json")
def nuvem_avaliadores_json(db: Session = Depends(get_db)):
    resultados = (
        db.query(Avaliacao.autor, func.count(Avaliacao.id).label("total"))
        .group_by(Avaliacao.autor)
        .all()
    )

    frequencias = {autor: total for autor, total in resultados if autor}

    if not frequencias:
        return []

    return [{"autor": nome, "peso": peso} for nome, peso in frequencias.items()]
