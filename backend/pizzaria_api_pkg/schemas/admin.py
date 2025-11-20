from pydantic import BaseModel

class MetricasOut(BaseModel):
    total_pedidos: int
    total_usuarios: int
    faturamento_total: float

class TabelaLimpaOut(BaseModel):
    tabela: str
    registros_removidos: int
    mensagem: str
