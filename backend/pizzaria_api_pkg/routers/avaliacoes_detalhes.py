from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.core_models import Avaliacao  # Certifique-se de que está importado corretamente

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])

@router.get("/detalhes")
def detalhes_avaliador(autor: str = Query(...), db: Session = Depends(get_db)):
    avaliacoes = db.query(Avaliacao).filter(Avaliacao.autor == autor).all()
    
    if not avaliacoes:
        raise HTTPException(status_code=404, detail="Nenhuma avaliação encontrada para esse autor")
    
    return {
        "autor": autor,
        "avaliacoes": [
            {
                "comentario": a.comentario,
                "nota": a.nota,
                "data": a.data
            } for a in avaliacoes
        ]
    }
