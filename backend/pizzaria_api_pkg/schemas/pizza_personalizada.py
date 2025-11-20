from pydantic import BaseModel
from typing import List

class PizzaCreate(BaseModel):
    nome: str
    ingredientes: List[int]

class PizzaOut(BaseModel):
    id: int
    nome: str
    preco_base: float
    cliente_id: int

    class Config:
        from_attributes = True

class TamanhoPizza(BaseModel):
    tamanho: str
    preco: float

    class Config:
        from_attributes = True
