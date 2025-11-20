from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.services.endereco_service import adicionar_endereco, listar_enderecos
from pizzaria_api_pkg.schemas.endereco_schema import EnderecoCreate, EnderecoOut
from pizzaria_api_pkg.dependencies import get_usuario_logado

router = APIRouter(prefix="/enderecos", tags=["Endereços"])

@router.post("/", response_model=EnderecoOut)
def adicionar(dados: EnderecoCreate, db: Session = Depends(get_db), usuario=Depends(get_usuario_logado)):
    return adicionar_endereco(db, usuario["usuario_id"], dados)

@router.get("/", response_model=list[EnderecoOut])
def listar(db: Session = Depends(get_db), usuario=Depends(get_usuario_logado)):
    return listar_enderecos(db, usuario["usuario_id"])
