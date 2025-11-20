from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.core_models import Ingrediente as IngredienteModel
from pizzaria_api_pkg.auth.rbac import role_required
from pizzaria_api_pkg.schemas.ingredientes import Ingrediente, IngredienteCreate

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

@router.get("/", response_model=list[Ingrediente])
def listar_ingredientes(db: Session = Depends(get_db)):
    return db.query(IngredienteModel).all()

@router.post("/", response_model=Ingrediente)
def criar_ingrediente(
    ingrediente: IngredienteCreate,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("admin", "funcionario"))
):
    ingrediente_existente = db.query(IngredienteModel).filter(
        IngredienteModel.nome.ilike(ingrediente.nome)
    ).first()
    if ingrediente_existente:
        raise HTTPException(status_code=400, detail="Ingrediente já cadastrado")

    novo_ingrediente = IngredienteModel(**ingrediente.dict())
    db.add(novo_ingrediente)
    db.commit()
    db.refresh(novo_ingrediente)
    return novo_ingrediente

@router.delete("/excluir/{ingrediente_id}", response_model=dict)
def excluir_ingrediente(
    ingrediente_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("admin"))
):
    ingrediente = db.query(IngredienteModel).filter(IngredienteModel.id == ingrediente_id).first()
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente não encontrado")
    db.delete(ingrediente)
    db.commit()
    return {"mensagem": "Ingrediente excluído com sucesso"}
