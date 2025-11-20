from pydantic import BaseModel
from datetime import datetime

class AvaliacaoCreate(BaseModel):
    pedido_id: int
    nota: int
    comentario: str

class AvaliacaoOut(BaseModel):
    nota: int
    cliente_id: int
    pedido_id: int
    comentario: str
    data_avaliacao: datetime

    model_config = {
        "from_attributes": True
    }
