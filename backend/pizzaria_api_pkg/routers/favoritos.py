from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.services.favoritos_service import adicionar_favorito, listar_favoritos
from pizzaria_api_pkg.schemas.favoritos_schema import FavoritoCreate, FavoritoOut
from pizzaria_api_pkg.dependencies import get_usuario_logado

router = APIRouter(prefix="/favoritos", tags=["Favoritos"])

@router.post("/", response_model=FavoritoOut)
def adicionar(dados: FavoritoCreate, db: Session = Depends(get_db), usuario=Depends(get_usuario_logado)):
    return adicionar_favorito(db, usuario["usuario_id"], dados.produto_id)

@router.get("/", response_model=list[FavoritoOut])
def listar(db: Session = Depends(get_db), usuario=Depends(get_usuario_logado)):
    return listar_favoritos(db, usuario["usuario_id"])
