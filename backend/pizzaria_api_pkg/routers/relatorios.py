from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.services.relatorios_service import (
    relatorio_vendas,
    nomes_pizzas_mais_vendidas
)

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/vendas")
def vendas(db: Session = Depends(get_db)):
    return relatorio_vendas(db)

# ✅ Mantido para compatibilidade com frontend
@router.get("/nuvem-sabores-lista-json")
def nuvem_sabores(db: Session = Depends(get_db)):
    return nomes_pizzas_mais_vendidas(db)
