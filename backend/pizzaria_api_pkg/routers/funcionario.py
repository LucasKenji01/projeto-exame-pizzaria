from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.core_models import Entrega
from pizzaria_api_pkg.auth.rbac import role_required

router = APIRouter(prefix="/funcionario", tags=["Funcionário"])

@router.get("/entregas/me")
def listar_minhas_entregas(usuario=Depends(role_required("funcionario")), db: Session = Depends(get_db)):
    return db.query(Entrega).filter_by(funcionario_id=usuario["usuario_id"]).all()

@router.put("/entregas/{id}/status")
def atualizar_status(id: int, novo_status: str, usuario=Depends(role_required("funcionario")), db: Session = Depends(get_db)):
    entrega = db.query(Entrega).filter_by(id=id, funcionario_id=usuario["usuario_id"]).first()
    if not entrega:
        raise HTTPException(404, "Entrega não encontrada")
    entrega.status = novo_status
    db.commit()
    return {"msg": "Status atualizado"}
