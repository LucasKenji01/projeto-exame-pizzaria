from pydantic import BaseModel, Field, field_validator

class CarrinhoItemCreate(BaseModel):
    produto_id: int | None = None
    produto_personalizado_id: int | None = None
    quantidade: int = Field(gt=0, description="Quantidade deve ser maior que zero")
    
    @field_validator('quantidade')
    @classmethod
    def validate_quantidade(cls, v):
        if v <= 0:
            raise ValueError('Quantidade deve ser maior que zero')
        return v

class CarrinhoItemOut(BaseModel):
    id: int
    produto_id: int | None
    produto_personalizado_id: int | None
    quantidade: int
    cliente_id: int

    class Config:
        from_attributes = True
