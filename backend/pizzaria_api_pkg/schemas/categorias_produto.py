from pydantic import BaseModel
from typing import Optional

class CategoriaProduto(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]

class CategoriaProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str]

    model_config = {
        "from_attributes": True
    }
