from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.relatorios.relatorio_vendas import vendas_por_periodo

router = APIRouter()

@router.get("/relatorios/pizzas-mais-vendidas/{periodo}")
def relatorio_vendas(periodo: str, db: Session = Depends(get_db)):
    """✅ CORRIGIDO: Trata retorno corretamente"""
    resultados = vendas_por_periodo(db, periodo)
    
    # ✅ Resultados já vêm como lista de dicts
    if not resultados:
        return []
    
    # ✅ Verificar se é dict ou objeto
    if isinstance(resultados, list) and len(resultados) > 0:
        if isinstance(resultados[0], dict):
            # Já está no formato correto
            return resultados
        else:
            # Converter objeto para dict
            return [
                {
                    "pizza": r.pizza,
                    "periodo": r.periodo.strftime("%Y-%m-%d") if hasattr(r.periodo, 'strftime') else str(r.periodo),
                    "quantidade": int(r.quantidade)
                } for r in resultados
            ]
    
    return []
