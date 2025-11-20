from pydantic import BaseModel

class AplicarCupomRequest(BaseModel):
    cupom_codigo: str

class AplicarCupomResponse(BaseModel):
    mensagem: str
    desconto_aplicado: float
    valor_original: float
    valor_final: float
    
    model_config = {"from_attributes": True}
