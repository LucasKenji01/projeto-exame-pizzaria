from pydantic import BaseModel, Field, field_validator, model_validator

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
    
    @model_validator(mode='after')
    def validate_produto_ou_personalizado(self):
        if self.produto_id is None and self.produto_personalizado_id is None:
            raise ValueError('Deve fornecer produto_id ou produto_personalizado_id')
        if self.produto_id is not None and self.produto_personalizado_id is not None:
            raise ValueError('Forneça apenas um: produto_id ou produto_personalizado_id')
        return self

class CarrinhoItemOut(BaseModel):
    id: int
    produto_id: int | None
    produto_personalizado_id: int | None
    quantidade: int
    cliente_id: int

    class Config:
        from_attributes = True
