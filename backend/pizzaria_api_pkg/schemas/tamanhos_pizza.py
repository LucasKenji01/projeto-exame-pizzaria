from pydantic import BaseModel
from typing import Optional

class TamanhoPizzaCreate(BaseModel):
    nome: str
    descricao: Optional[str]
    preco: float

class TamanhoPizzaOut(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    preco: float
    produto_id: int

    model_config = {
        "from_attributes": True
    }
