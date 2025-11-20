from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.core_models import Avaliacao

router = APIRouter(prefix="/avaliacoes", tags=["Relatórios de Avaliações"])

@router.get("/media")
def media_avaliacoes(cliente_id: int = Query(...), db: Session = Depends(get_db)):
    avaliacoes = db.query(Avaliacao).filter(Avaliacao.cliente_id == cliente_id).all()
    if not avaliacoes:
        raise HTTPException(status_code=404, detail="Nenhuma avaliação encontrada para este cliente.")
    media = round(sum(a.nota for a in avaliacoes) / len(avaliacoes), 2)
    return {
        "cliente_id": cliente_id,
        "media_nota": media,
        "total_avaliacoes": len(avaliacoes)
    }

@router.get("/estatisticas")
def estatisticas_avaliacoes(db: Session = Depends(get_db)):
    total = db.query(func.count(Avaliacao.id)).scalar()
    media = db.query(func.avg(Avaliacao.nota)).scalar()
    mais_recente = db.query(Avaliacao).order_by(Avaliacao.data_avaliacao.desc()).first()
    mais_negativa = db.query(Avaliacao).order_by(Avaliacao.nota.asc()).first()

    return {
        "media_geral": round(media or 0, 2),
        "total_avaliacoes": total,
        "mais_recente": {
            "cliente_id": mais_recente.cliente_id,
            "comentario": mais_recente.comentario,
            "nota": mais_recente.nota,
            "data": mais_recente.data_avaliacao,
            "produto_id": mais_recente.produto_id
        } if mais_recente else None,
        "mais_negativa": {
            "cliente_id": mais_negativa.cliente_id,
            "comentario": mais_negativa.comentario,
            "nota": mais_negativa.nota,
            "data": mais_negativa.data_avaliacao,
            "produto_id": mais_negativa.produto_id
        } if mais_negativa else None
    }

@router.get("/produto/{produto_id}")
def avaliacoes_por_produto(produto_id: int, db: Session = Depends(get_db)):
    avaliacoes = db.query(Avaliacao).filter(Avaliacao.produto_id == produto_id).all()
    if not avaliacoes:
        raise HTTPException(status_code=404, detail="Nenhuma avaliação encontrada para este produto.")
    return [
        {
            "cliente_id": a.cliente_id,
            "nota": a.nota,
            "comentario": a.comentario,
            "data": a.data_avaliacao
        } for a in avaliacoes
    ]
