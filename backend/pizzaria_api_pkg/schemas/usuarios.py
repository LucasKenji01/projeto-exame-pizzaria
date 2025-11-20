from pydantic import BaseModel, constr
from pydantic import ConfigDict

class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    tipo_usuario: str

    model_config = ConfigDict(from_attributes=True)

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    tipo_usuario: str

class UsuarioClienteCreate(BaseModel):
    nome: str
    email: str
    senha: str
    telefone: constr(min_length=10, max_length=15)
    endereco: str
