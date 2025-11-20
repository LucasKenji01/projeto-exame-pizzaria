from sqlalchemy.orm import Session
from pizzaria_api_pkg.core_models import PizzaPersonalizada, Ingrediente

def calcular_preco_pizza(db: Session, pizza_id: int):
    pizza = db.query(PizzaPersonalizada).filter_by(id=pizza_id).first()
    if not pizza:
        raise ValueError("Pizza não encontrada")

    preco_total = pizza.preco_base
    for item in pizza.ingredientes:
        ingrediente = db.query(Ingrediente).filter_by(id=item.ingrediente_id, disponivel=True).first()
        if ingrediente:
            preco_total += ingrediente.preco * item.quantidade

    pizza.preco_base = preco_total
    db.commit()
    return preco_total
