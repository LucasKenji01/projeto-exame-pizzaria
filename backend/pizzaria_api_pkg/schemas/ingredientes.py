from pydantic import BaseModel

class Ingrediente(BaseModel):
    id: int
    nome: str
    preco: float
    disponivel: bool

    class Config:
        from_attributes = True

class IngredienteCreate(BaseModel):
    nome: str
    preco: float = 0.0
