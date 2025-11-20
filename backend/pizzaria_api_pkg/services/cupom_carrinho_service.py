from sqlalchemy.orm import Session
from pizzaria_api_pkg.core_models import Carrinho, Cupom, Produto, PizzaPersonalizada
from datetime import date
from fastapi import HTTPException

def aplicar_cupom_carrinho(db: Session, cliente_id: int, cupom_codigo: str):
    """✅ CORRIGIDO: Aplica cupom de desconto aos itens do carrinho"""
    
    # Normalizar código do cupom
    cupom_codigo = cupom_codigo.strip().upper()
    
    cupom = db.query(Cupom).filter(
        Cupom.codigo == cupom_codigo,
        Cupom.ativo == True
    ).first()
    
    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado ou inativo")
    
    if cupom.validade and cupom.validade < date.today():
        raise HTTPException(status_code=400, detail="Cupom expirado")
    
    itens = db.query(Carrinho).filter(Carrinho.cliente_id == cliente_id).all()
    
    if not itens:
        raise HTTPException(status_code=400, detail="Carrinho vazio")
    
    valor_original = 0.0
    for item in itens:
        try:
            if item.produto_id:
                produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
                if produto:
                    preco = produto.preco
                else:
                    continue  # Ignora item com produto inválido
            elif item.produto_personalizado_id:
                pizza = db.query(PizzaPersonalizada).filter(
                    PizzaPersonalizada.id == item.produto_personalizado_id
                ).first()
                if pizza:
                    preco = pizza.preco_base
                else:
                    continue  # Ignora item com pizza inválida
            else:
                continue  # Ignora item sem produto
            
            valor_original += preco * item.quantidade
        except Exception as e:
            print(f"Erro ao processar item do carrinho: {e}")
            continue
    
    if valor_original == 0:
        raise HTTPException(status_code=400, detail="Nenhum item válido no carrinho")
    
    desconto = valor_original * (cupom.percentual_desconto / 100)
    valor_final = valor_original - desconto
    
    return {
        "mensagem": f"Cupom {cupom_codigo} aplicado com sucesso!",
        "desconto_aplicado": round(desconto, 2),
        "valor_original": round(valor_original, 2),
        "valor_final": round(valor_final, 2),
        "percentual": cupom.percentual_desconto
    }
