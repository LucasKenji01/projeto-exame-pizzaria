from pydantic import BaseModel

class EnderecoCreate(BaseModel):
    rua: str
    numero: str
    complemento: str | None = None
    bairro: str
    cidade: str
    estado: str
    cep: str
    favorito: bool = False

class EnderecoOut(EnderecoCreate):
    id: int
