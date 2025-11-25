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


class PromoverUsuarioInput(BaseModel):
    usuario_id: int | None = None
    email: str | None = None

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


@router.post('/usuarios/promover')
def promover_usuario(dados: PromoverUsuarioInput, usuario=Depends(role_required("admin")), db: Session = Depends(get_db)):
    """Promove um usuário a admin. Requer que quem chama seja admin.

    Envia `usuario_id` ou `email` no corpo.
    """
    if not dados.usuario_id and not dados.email:
        raise HTTPException(status_code=400, detail="Forneça 'usuario_id' ou 'email' para promover.")

    query = db.query(Usuario)
    if dados.usuario_id:
        target = query.filter(Usuario.id == dados.usuario_id).first()
    else:
        target = query.filter(Usuario.email == dados.email).first()

    if not target:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    target.tipo_usuario = 'admin'
    db.add(target)
    db.commit()
    return {"msg": "Usuário promovido a admin", "usuario_id": target.id, "email": target.email}
