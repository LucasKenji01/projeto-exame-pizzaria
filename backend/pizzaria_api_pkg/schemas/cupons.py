from datetime import date
from pydantic import BaseModel, Field


class CupomBase(BaseModel):
    codigo: str = Field(..., example="PROMO10")
    percentual_desconto: float = Field(..., gt=0, le=100, example=10.0)
    validade: date | None = Field(None, example="2025-12-31")
    ativo: bool = True


class CupomCreate(CupomBase):
    """Schema usado para criação de cupons."""
    pass


class CupomOut(CupomBase):
    """Schema usado para retorno de dados de cupons."""
    id: int

    class Config:
        # ✅ Corrigido para Pydantic v2
        from_attributes = True


# 🔁 Compatibilidade retroativa
# Alguns módulos antigos ainda importam "CupomResponse"
CupomResponse = CupomOut
