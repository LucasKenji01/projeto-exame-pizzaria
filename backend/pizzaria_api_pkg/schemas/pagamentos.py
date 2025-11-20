from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PagamentoCreate(BaseModel):
    pedido_id: int
    forma_pagamento: str
    valor: float

class PagamentoOut(BaseModel):
    id: int
    pedido_id: int
    forma_pagamento: str
    valor: float
    data_pagamento: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
