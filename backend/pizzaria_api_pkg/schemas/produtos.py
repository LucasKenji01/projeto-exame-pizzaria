from pydantic import BaseModel
from typing import Optional, List
from pizzaria_api_pkg.schemas.tamanhos_pizza import TamanhoPizzaCreate, TamanhoPizzaOut

class Produto(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    preco: float
    categoria_id: Optional[int]
    imagem_url: Optional[str] = None
    tamanhos: Optional[List[TamanhoPizzaOut]] = None
    model_config = {
        "from_attributes": True
    }

class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str]
    preco: float
    categoria_id: Optional[int]
    tipo: str
    imagem_url: Optional[str] = None
    tamanhos: Optional[List[TamanhoPizzaCreate]] = None

    model_config = {
        "from_attributes": True
    }
