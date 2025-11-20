from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.core_models import (  # ✅ CORREÇÃO
    Cliente, PizzaPersonalizada, PizzaIngrediente, Ingrediente
)
from pizzaria_api_pkg.auth.rbac import role_required, get_usuario_autenticado
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/pizzas", tags=["Pizzas Personalizadas"])

class PizzaCreate(BaseModel):
    nome: str
    preco_base: float

class IngredienteInput(BaseModel):
    ingrediente_id: int
    quantidade: int = 1

class PizzaMontagem(BaseModel):
    nome: str
    preco_base: float
    ingredientes: List[IngredienteInput]

class PizzaOut(BaseModel):
    id: int
    nome: str
    preco_base: float
    class Config:
        from_attributes = True

@router.post("/", response_model=PizzaOut)
def criar_pizza(
    pizza: PizzaCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_autenticado)
):
    cliente = db.query(Cliente).filter(
        Cliente.usuario_id == usuario["usuario_id"]
    ).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    nova_pizza = PizzaPersonalizada(
        nome=pizza.nome,
        preco_base=pizza.preco_base,
        cliente_id=cliente.id
    )
    db.add(nova_pizza)
    db.commit()
    db.refresh(nova_pizza)
    return nova_pizza

@router.post("/montar", response_model=PizzaOut)
def montar_pizza(
    dados: PizzaMontagem,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_autenticado)
):
    cliente = db.query(Cliente).filter(
        Cliente.usuario_id == usuario["usuario_id"]
    ).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    nova_pizza = PizzaPersonalizada(
        nome=dados.nome,
        preco_base=dados.preco_base,
        cliente_id=cliente.id
    )
    db.add(nova_pizza)
    db.flush()

    for item in dados.ingredientes:
        ingrediente = db.query(Ingrediente).filter_by(id=item.ingrediente_id).first()  # ✅ CORRIGIDO
        if not ingrediente:
            raise HTTPException(404, f"Ingrediente {item.ingrediente_id} não encontrado")
        
        vinculo = PizzaIngrediente(
            pizza_personalizada_id=nova_pizza.id,
            ingrediente_id=item.ingrediente_id,
            quantidade=item.quantidade
        )
        db.add(vinculo)

    db.commit()
    db.refresh(nova_pizza)
    return nova_pizza

@router.get("/me", response_model=List[PizzaOut])
def listar_minhas_pizzas(
    usuario=Depends(role_required("cliente")),
    db: Session = Depends(get_db)
):
    cliente = db.query(Cliente).filter(
        Cliente.usuario_id == usuario["usuario_id"]
    ).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return db.query(PizzaPersonalizada).filter_by(cliente_id=cliente.id).all()

@router.get("/{pizza_id}/preco")
def calcular_preco(pizza_id: int, db: Session = Depends(get_db)):
    pizza = db.query(PizzaPersonalizada).filter_by(id=pizza_id).first()
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza não encontrada")
    
    total = pizza.preco_base
    for item in pizza.ingredientes:
        total += item.ingrediente.preco * item.quantidade
    
    return {"pizza_id": pizza.id, "preco_total": round(total, 2)}

@router.get("/")
def listar_pizzas_personalizadas():
    return [{"id": 1, "nome": "Pizza Teste"}]
