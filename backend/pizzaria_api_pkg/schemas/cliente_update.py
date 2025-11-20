from pydantic import BaseModel
from typing import Optional

class ClienteUpdate(BaseModel):
    telefone: Optional[str] = None
    endereco: Optional[str] = None

class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: Optional[str]
    endereco: Optional[str]
    
    model_config = {"from_attributes": True}
