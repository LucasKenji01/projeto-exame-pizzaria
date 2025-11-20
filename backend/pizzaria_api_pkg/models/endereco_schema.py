from pydantic import BaseModel

class EnderecoCreate(BaseModel):
    apelido: str = "Casa"  # Compatibilidade: se não informado, usa "Casa"
    rua: str  # Será mapeado para logradouro
    numero: str
    complemento: str | None = None
    bairro: str
    cidade: str
    estado: str
    cep: str
    favorito: bool = False  # Será mapeado para padrao
    
    # Campos opcionais da tabela real
    referencia: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class EnderecoOut(BaseModel):
    id: int
    apelido: str
    rua: str  # Vem de logradouro via property
    numero: str
    complemento: str | None
    bairro: str
    cidade: str
    estado: str
    cep: str
    favorito: bool  # Vem de padrao via property
    
    class Config:
        from_attributes = True
