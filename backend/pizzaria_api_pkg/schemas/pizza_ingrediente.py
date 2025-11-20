from pydantic import BaseModel

class PizzaIngrediente(BaseModel):
    id: int
    pizza_id: int
    ingrediente_id: int
    quantidade: int

class PizzaIngredienteCreate(BaseModel):
    pizza_id: int
    ingrediente_id: int
    quantidade: int

    model_config = {
        "from_attributes": True
    }
