from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.core_models import Cupom
from pizzaria_api_pkg.schemas.cupons import CupomCreate, CupomOut

router = APIRouter(prefix="/cupons", tags=["Cupons"])

@router.post("/", response_model=CupomOut)
def criar_cupom(cupom: CupomCreate, db: Session = Depends(get_db)):
    existente = db.query(Cupom).filter(Cupom.codigo == cupom.codigo).first()
    if existente:
        raise HTTPException(status_code=400, detail="Código de cupom já existente")

    novo = Cupom(**cupom.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=list[CupomOut])
def listar_cupons(db: Session = Depends(get_db)):
    return db.query(Cupom).all()


@router.get("/{cupom_id}", response_model=CupomOut)
def obter_cupom(cupom_id: int, db: Session = Depends(get_db)):
    cupom = db.query(Cupom).filter(Cupom.id == cupom_id).first()
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return cupom


@router.delete("/{cupom_id}")
def deletar_cupom(cupom_id: int, db: Session = Depends(get_db)):
    cupom = db.query(Cupom).filter(Cupom.id == cupom_id).first()
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    db.delete(cupom)
    db.commit()
    return {"mensagem": "Cupom removido com sucesso"}
