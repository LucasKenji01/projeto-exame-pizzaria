from pydantic import BaseModel, constr

class ClienteCreate(BaseModel):
    nome: str
    email: str
    telefone: constr(min_length=10, max_length=15)
    endereco: str

class Cliente(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    usuario_id: int
    endereco: str

    model_config = {
        "from_attributes": True
    }
