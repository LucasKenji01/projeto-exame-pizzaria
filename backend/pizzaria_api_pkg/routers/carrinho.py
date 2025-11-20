from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from pizzaria_api_pkg.core_models import (  # ✅ CORREÇÃO: import correto
    Carrinho, Cliente, Produto, PizzaPersonalizada,
    Pedido, ItemPedido, Pagamento, Entrega
)
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.schemas.carrinho import CarrinhoItemCreate, CarrinhoItemOut
from pizzaria_api_pkg.schemas.pedidos import PedidoOut
from pizzaria_api_pkg.dependencies import get_usuario_logado
from pizzaria_api_pkg.auth.rbac import role_required
from pizzaria_api_pkg.services.cupom_carrinho_service import aplicar_cupom_carrinho
from pizzaria_api_pkg.schemas.cupom_aplicacao import AplicarCupomRequest, AplicarCupomResponse

router = APIRouter(prefix="/carrinho", tags=["Carrinho"])

@router.post("/adicionar", response_model=CarrinhoItemOut)
def adicionar_item(
    item: CarrinhoItemCreate,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("cliente"))
):
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario["usuario_id"]).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # ✅ NOVO: Verificar se o produto já existe no carrinho
    item_existente = None
    if item.produto_id:
        item_existente = db.query(Carrinho).filter(
            Carrinho.cliente_id == cliente.id,
            Carrinho.produto_id == item.produto_id,
            Carrinho.produto_personalizado_id == None
        ).first()
    elif item.produto_personalizado_id:
        item_existente = db.query(Carrinho).filter(
            Carrinho.cliente_id == cliente.id,
            Carrinho.produto_personalizado_id == item.produto_personalizado_id,
            Carrinho.produto_id == None
        ).first()

    if item_existente:
        # ✅ NOVO: Incrementar quantidade do item existente
        print(f"✅ Item já existe no carrinho (ID: {item_existente.id}). Incrementando quantidade de {item_existente.quantidade} para {item_existente.quantidade + item.quantidade}")
        item_existente.quantidade += item.quantidade
        db.commit()
        db.refresh(item_existente)
        return item_existente
    else:
        # ✅ NOVO: Criar novo item
        novo_item = Carrinho(
            cliente_id=cliente.id,
            produto_id=item.produto_id,
            produto_personalizado_id=item.produto_personalizado_id,
            quantidade=item.quantidade
        )

        db.add(novo_item)
        db.commit()
        db.refresh(novo_item)
        return novo_item

@router.get("/", response_model=list[CarrinhoItemOut])
def listar_carrinho(
    db: Session = Depends(get_db),
    usuario=Depends(role_required("cliente"))
):
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario["usuario_id"]).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return db.query(Carrinho).filter(Carrinho.cliente_id == cliente.id).all()


@router.get("/detalhado")
def listar_carrinho_detalhado(
    db: Session = Depends(get_db),
    usuario=Depends(role_required("cliente"))
):
    """✅ NOVO: Retorna carrinho com detalhes completos dos produtos"""
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario["usuario_id"]).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    itens = db.query(Carrinho).filter(Carrinho.cliente_id == cliente.id).all()
    
    carrinho_detalhado = []
    total_geral = 0.0
    
    for item in itens:
        item_info = {
            "id": item.id,
            "quantidade": item.quantidade
        }
        
        if item.produto_id and item.produto:
            item_info["tipo"] = "produto"
            item_info["produto_id"] = item.produto_id
            item_info["nome"] = item.produto.nome
            item_info["preco_unitario"] = item.produto.preco
            item_info["preco_total"] = item.produto.preco * item.quantidade
        elif item.produto_personalizado_id and item.produto_personalizado:
            pizza = item.produto_personalizado
            item_info["tipo"] = "pizza_personalizada"
            item_info["pizza_id"] = pizza.id
            item_info["nome"] = pizza.nome
            item_info["preco_unitario"] = pizza.preco_base
            item_info["preco_total"] = pizza.preco_base * item.quantidade
            item_info["ingredientes"] = [
                {
                    "id": ing.ingrediente.id,
                    "nome": ing.ingrediente.nome,
                    "quantidade": ing.quantidade
                }
                for ing in pizza.ingredientes
            ] if pizza.ingredientes else []
        else:
            continue
        
        total_geral += item_info.get("preco_total", 0)
        carrinho_detalhado.append(item_info)
    
    return {
        "itens": carrinho_detalhado,
        "quantidade_itens": len(carrinho_detalhado),
        "total": round(total_geral, 2)
    }

@router.delete("/limpar")
def limpar_carrinho(
    db: Session = Depends(get_db),
    usuario=Depends(role_required("cliente"))
):
    """Limpar todo o carrinho do cliente"""
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario["usuario_id"]).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.query(Carrinho).filter(Carrinho.cliente_id == cliente.id).delete()
    db.commit()
    return {"mensagem": "Carrinho limpo com sucesso"}

@router.delete("/{item_id}")
def remover_item_carrinho(
    item_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("cliente"))
):
    """Remove um item específico do carrinho do cliente"""
    print(f"🔍 DEBUG DELETE: item_id={item_id}, tipo={type(item_id)}")
    print(f"🔍 DEBUG DELETE: usuario={usuario}")
    
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario["usuario_id"]).first()
    print(f"🔍 DEBUG DELETE: cliente_id={cliente.id if cliente else 'None'}")
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    item = db.query(Carrinho).filter(
        Carrinho.id == item_id,
        Carrinho.cliente_id == cliente.id
    ).first()
    print(f"🔍 DEBUG DELETE: item encontrado={item is not None}, item={item}")
    
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado no carrinho")

    db.delete(item)
    db.commit()
    return {"mensagem": "Item removido com sucesso"}

@router.post("/finalizar", response_model=PedidoOut)
def finalizar_carrinho(
    db: Session = Depends(get_db),
    usuario=Depends(role_required("cliente"))
):
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario["usuario_id"]).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    carrinho = db.query(Carrinho).filter(Carrinho.cliente_id == cliente.id).all()
    if not carrinho:
        raise HTTPException(status_code=400, detail="Carrinho vazio")

    valor_total = 0.0
    itens_pedido = []

    for item in carrinho:
        if item.produto_id and item.produto:
            preco_unitario = item.produto.preco
        elif item.produto_personalizado_id and item.produto_personalizado:
            preco_unitario = item.produto_personalizado.preco_base
        else:
            raise HTTPException(status_code=400, detail="Item inválido no carrinho")

        preco_total = preco_unitario * item.quantidade
        valor_total += preco_total

        itens_pedido.append(ItemPedido(  # ✅ CORRIGIDO
            quantidade=item.quantidade,
            preco_unitario=preco_unitario,
            preco_total=preco_total,
            produto_id=item.produto_id,
            produto_personalizado_id=item.produto_personalizado_id,
            pedido_id=None
        ))

    pedido = Pedido(
        descricao="Pedido via carrinho",
        quantidade=sum(i.quantidade for i in itens_pedido),
        valor_total=valor_total,
        email=cliente.usuario.email,
        cliente_id=cliente.id
    )

    db.add(pedido)
    db.flush()

    for item in itens_pedido:
        item.pedido_id = pedido.id
        db.add(item)

    pagamento = Pagamento(
        pedido_id=pedido.id,
        forma_pagamento="pix",
        valor=valor_total,
        data_pagamento=None
    )
    db.add(pagamento)

    entrega = Entrega(
        pedido_id=pedido.id,
        endereco_entrega=cliente.endereco or "Endereço não cadastrado",
        data_prevista=date.today() + timedelta(days=2),
        status="pendente"
    )
    db.add(entrega)

    db.query(Carrinho).filter(Carrinho.cliente_id == cliente.id).delete()
    db.commit()
    db.refresh(pedido)

    return pedido


@router.post("/adicionar-pizza-personalizada", response_model=CarrinhoItemOut)
def adicionar_pizza_personalizada(
    pizza_id: int,
    quantidade: int = 1,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("cliente"))
):
    """✅ CORRIGIDO: Adicionar pizza personalizada ao carrinho"""
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario["usuario_id"]).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verificar se a pizza existe
    pizza = db.query(PizzaPersonalizada).filter(PizzaPersonalizada.id == pizza_id).first()
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza personalizada não encontrada")
    
    # Verificar se a pizza pertence ao cliente
    if pizza.cliente_id != cliente.id:
        raise HTTPException(status_code=403, detail="Esta pizza não pertence a você")

    novo_item = Carrinho(
        cliente_id=cliente.id,
        produto_id=None,
        produto_personalizado_id=pizza_id,
        quantidade=quantidade
    )

    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    return novo_item

@router.post("/aplicar-cupom", response_model=AplicarCupomResponse)
def aplicar_cupom(
    request: AplicarCupomRequest,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("cliente"))
):
    cliente = db.query(Cliente).filter(
        Cliente.usuario_id == usuario["usuario_id"]
    ).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    resultado = aplicar_cupom_carrinho(db, cliente.id, request.cupom_codigo)
    return resultado
