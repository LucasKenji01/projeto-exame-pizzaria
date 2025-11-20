from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class EntregaOut(BaseModel):
    id: int
    endereco_entrega: str
    data_prevista: date
    data_entrega: Optional[datetime] = None
    status: str
    pedido_id: int
    funcionario_id: Optional[int] = None

    class Config:
        from_attributes = True
