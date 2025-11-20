from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.auth.rbac import role_required
from pizzaria_api_pkg.core_models import (  # ✅ CORREÇÃO: import correto
    Carrinho, Pedido, Produto, Ingrediente, Cupom, Usuario, Pagamento
)
from pydantic import BaseModel
from datetime import date
from pizzaria_api_pkg.schemas.admin import *

router = APIRouter(prefix="/admin", tags=["Admin"])

class ProdutoInput(BaseModel):
    nome: str
    preco: float
    descricao: str | None = None

class IngredienteInput(BaseModel):
    nome: str
    preco: float = 0.0

class CupomInput(BaseModel):
    codigo: str
    percentual_desconto: float
    validade: date

# ✅ CORREÇÃO: Usar os modelos corretos importados
TABELAS = {
    "carrinho": Carrinho,
    "pedidos": Pedido,
    "produtos": Produto,
    "ingredientes": Ingrediente,
}

@router.delete("/limpar/{tabela}")
def limpar_tabela(tabela: str, db: Session = Depends(get_db), usuario=Depends(role_required("admin"))):
    if tabela not in TABELAS:
        raise HTTPException(400, f"Tabela inválida. Opções: {list(TABELAS.keys())}")
    count = db.query(TABELAS[tabela]).delete()
    db.commit()
    return {"tabela": tabela, "registros_removidos": count}

@router.post("/produtos/criar")
def criar_produto(dados: ProdutoInput, usuario=Depends(role_required("admin")), db: Session = Depends(get_db)):
    produto = Produto(**dados.dict())
    db.add(produto)
    db.commit()
    return {"msg": "Produto criado", "id": produto.id}

@router.post("/ingredientes/criar")
def criar_ingrediente(dados: IngredienteInput, usuario=Depends(role_required("admin")), db: Session = Depends(get_db)):
    ingrediente = Ingrediente(**dados.dict())
    db.add(ingrediente)
    db.commit()
    return {"msg": "Ingrediente criado", "id": ingrediente.id}

@router.post("/cupons/criar")
def criar_cupom(dados: CupomInput, usuario=Depends(role_required("admin")), db: Session = Depends(get_db)):
    cupom = Cupom(**dados.dict())
    db.add(cupom)
    db.commit()
    return {"msg": "Cupom criado", "id": cupom.id}

@router.get("/metricas", response_model=MetricasOut)
def metricas(usuario=Depends(role_required("admin")), db: Session = Depends(get_db)):
    total_pedidos = db.query(Pedido).count()
    total_usuarios = db.query(Usuario).count()
    faturamento = db.query(Pagamento).with_entities(Pagamento.valor).all()
    total_faturado = sum(p.valor for p in faturamento)
    return {
        "total_pedidos": total_pedidos,
        "total_usuarios": total_usuarios,
        "faturamento_total": total_faturado
    }
