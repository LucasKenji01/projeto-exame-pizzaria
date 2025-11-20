from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.services.entregas_service import listar_entregas_funcionario
from pizzaria_api_pkg.auth.rbac import role_required
from pizzaria_api_pkg.schemas.entregas import EntregaOut
from pizzaria_api_pkg.core_models import Entrega, Pedido, Cliente

router = APIRouter(prefix="/entregas", tags=["Entregas"])

@router.get("/funcionario", response_model=List[EntregaOut])
def entregas_funcionario(
    usuario=Depends(role_required("funcionario")),
    db: Session = Depends(get_db)
):
    return listar_entregas_funcionario(db, usuario["usuario_id"])

@router.get("/pedido/{pedido_id}", response_model=EntregaOut)
def consultar_entrega_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("cliente", "funcionario", "admin"))
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    if usuario["tipo_usuario"] == "cliente":
        cliente = db.query(Cliente).filter(
            Cliente.usuario_id == usuario["usuario_id"]
        ).first()
        
        if not cliente or pedido.cliente_id != cliente.id:
            raise HTTPException(status_code=403, detail="Acesso negado a este pedido")
    
    entrega = db.query(Entrega).filter(Entrega.pedido_id == pedido_id).first()
    
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega não encontrada para este pedido")
    
    return entrega
