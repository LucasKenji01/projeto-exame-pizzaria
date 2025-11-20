from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg import models
from pizzaria_api_pkg.schemas.pagamentos import PagamentoCreate, PagamentoOut
from pizzaria_api_pkg.auth.rbac import role_required

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])

@router.post("/", response_model=PagamentoOut)
def registrar_pagamento(
    pagamento: PagamentoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("admin", "funcionario"))
):
    pedido = db.get(models.Pedido, pagamento.pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    novo_pagamento = models.Pagamento(
        pedido_id=pagamento.pedido_id,
        forma_pagamento=pagamento.forma_pagamento,
        valor=pagamento.valor,
        data_pagamento=datetime.utcnow()
    )
    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)

    pedido.status = "pago"
    db.commit()

    return novo_pagamento
