from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from pizzaria_api_pkg import models
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.schemas.pedidos import PedidoCreate, PedidoOut
from pizzaria_api_pkg.auth.rbac import role_required, get_usuario_autenticado
from pizzaria_api_pkg.services.pedidos_service import atualizar_status_pedido, gerar_pedido_do_carrinho

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/finalizar", response_model=PedidoOut)
def finalizar_pedido(
    pedido_data: PedidoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_autenticado)
):
    print(f"\n\n{'='*60}")
    print(f"🔍 [POST /finalizar] Iniciando finalização de pedido")
    print(f"🔍 usuario_id from token = {usuario['usuario_id']}")
    print(f"{'='*60}\n")
    
    cliente = db.query(models.Cliente).filter(
        models.Cliente.usuario_id == usuario["usuario_id"]
    ).first()
    print(f"🔍 Cliente encontrado? {cliente is not None}")
    if cliente:
        print(f"🔍 Cliente ID = {cliente.id}, Usuario ID = {cliente.usuario_id}")
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Debug: lista todos os carrinhos no banco
    todos_carrinhos = db.query(models.Carrinho).all()
    print(f"🔍 Total de carrinhos no banco = {len(todos_carrinhos)}")
    for c in todos_carrinhos:
        print(f"  - Carrinho ID: {c.id}, Cliente ID: {c.cliente_id}, Produto ID: {c.produto_id}, Qty: {c.quantidade}")

    print(f"\n🔍 Buscando carrinho para cliente_id = {cliente.id}")
    carrinho = db.query(models.Carrinho).filter(
        models.Carrinho.cliente_id == cliente.id
    ).all()
    print(f"🔍 Carrinho items encontrados para cliente {cliente.id} = {len(carrinho)}")
    for item in carrinho:
        print(f"  - Item ID: {item.id}, Produto ID: {item.produto_id}, Qty: {item.quantidade}")
    
    if not carrinho:
        print(f"\n❌ [ERROR] Carrinho vazio para cliente {cliente.id}\n")
        raise HTTPException(status_code=400, detail="Carrinho vazio")

    valor_total = 0.0
    quantidade_total = 0

    for item in carrinho:
        if item.produto_id and item.produto:
            unit = item.produto.preco or 0.0
        elif item.produto_personalizado_id and item.produto_personalizado:
            unit = item.produto_personalizado.preco_base or 0.0
        else:
            raise HTTPException(status_code=400, detail="Item inválido no carrinho")

        valor_total += unit * item.quantidade
        quantidade_total += item.quantidade

    novo_pedido = models.Pedido(
        descricao=pedido_data.descricao or "Pedido via carrinho",
        quantidade=quantidade_total,
        valor_total=valor_total,
        email=pedido_data.email or cliente.usuario.email,
        cliente_id=cliente.id,
        data_pedido=datetime.utcnow(),
        status="Finalizado"
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    for item in carrinho:
        preco_unit = item.produto.preco if item.produto_id else item.produto_personalizado.preco_base
        item_pedido = models.ItemPedido(
            pedido_id=novo_pedido.id,
            quantidade=item.quantidade,
            preco_unitario=preco_unit,
            preco_total=preco_unit * item.quantidade,
            produto_id=item.produto_id,
            produto_personalizado_id=item.produto_personalizado_id
        )
        db.add(item_pedido)
        db.delete(item)

    db.commit()
    novo_pedido.itens = db.query(models.ItemPedido).filter(
        models.ItemPedido.pedido_id == novo_pedido.id
    ).all()
    
    # ✅ Enriquecer com nomes dos produtos antes de retornar
    pedido_enriquecido = {
        "id": novo_pedido.id,
        "descricao": novo_pedido.descricao,
        "quantidade": novo_pedido.quantidade,
        "valor_total": novo_pedido.valor_total,
        "email": novo_pedido.email,
        "data_pedido": novo_pedido.data_pedido,
        "status": novo_pedido.status,
        "cliente_id": novo_pedido.cliente_id,
        "itens": []
    }
    
    for item in novo_pedido.itens:
        item_dict = {
            "id": item.id,
            "produto_id": item.produto_id,
            "produto_personalizado_id": item.produto_personalizado_id,
            "quantidade": item.quantidade,
            "preco_unitario": item.preco_unitario,
            "preco_total": item.preco_total
        }
        
        if item.produto_id and item.produto:
            item_dict["nome_produto"] = item.produto.nome
            item_dict["tipo"] = "produto"
        elif item.produto_personalizado_id and item.produto_personalizado:
            item_dict["nome_produto"] = item.produto_personalizado.nome
            item_dict["tipo"] = "pizza_personalizada"
        else:
            item_dict["nome_produto"] = "Produto Removido"
            item_dict["tipo"] = "desconhecido"
        
        pedido_enriquecido["itens"].append(item_dict)
    
    return pedido_enriquecido

@router.post("/gerar-do-carrinho", response_model=PedidoOut, dependencies=[Depends(role_required("cliente"))])
def gerar_pedido_automatico(
    usuario=Depends(role_required("cliente")),
    db: Session = Depends(get_db)
):
    try:
        pedido = gerar_pedido_do_carrinho(db, cliente_id=usuario["usuario_id"], email="cliente@teste.com")
        return pedido
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/me", response_model=List[PedidoOut])
def listar_meus_pedidos(
    usuario=Depends(role_required("cliente")),
    db: Session = Depends(get_db)
):
    """✅ CORRIGIDO: Retorna pedidos com nomes dos produtos"""
    pedidos = db.query(models.Pedido).filter_by(cliente_id=usuario["usuario_id"]).all()
    
    # Enriquecer cada pedido com nomes dos produtos
    pedidos_enriquecidos = []
    for pedido in pedidos:
        pedido_dict = {
            "id": pedido.id,
            "descricao": pedido.descricao,
            "quantidade": pedido.quantidade,
            "valor_total": pedido.valor_total,
            "email": pedido.email,
            "data_pedido": pedido.data_pedido,
            "status": pedido.status,
            "cliente_id": pedido.cliente_id,
            "itens": []
        }
        
        for item in pedido.itens:
            item_dict = {
                "id": item.id,
                "produto_id": item.produto_id,
                "produto_personalizado_id": item.produto_personalizado_id,
                "quantidade": item.quantidade,
                "preco_unitario": item.preco_unitario,
                "preco_total": item.preco_total
            }
            
            # ✅ ADICIONAR NOME DO PRODUTO
            if item.produto_id and item.produto:
                item_dict["nome_produto"] = item.produto.nome
                item_dict["tipo"] = "produto"
            elif item.produto_personalizado_id and item.produto_personalizado:
                item_dict["nome_produto"] = item.produto_personalizado.nome
                item_dict["tipo"] = "pizza_personalizada"
            else:
                item_dict["nome_produto"] = "Produto Removido"
                item_dict["tipo"] = "desconhecido"
            
            pedido_dict["itens"].append(item_dict)
        
        pedidos_enriquecidos.append(pedido_dict)
    
    return pedidos_enriquecidos

@router.delete("/{pedido_id}")
def cancelar_pedido(
    pedido_id: int,
    usuario=Depends(role_required("cliente")),
    db: Session = Depends(get_db)
):
    pedido = db.query(models.Pedido).filter_by(
        id=pedido_id,
        cliente_id=usuario["usuario_id"]
    ).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if pedido.status != "pendente":
        raise HTTPException(status_code=400, detail="Apenas pedidos pendentes podem ser cancelados")

    db.delete(pedido)
    db.commit()
    return {"msg": "Pedido cancelado"}


@router.delete("")
def deletar_todos_pedidos(
    usuario=Depends(role_required("admin")),
    db: Session = Depends(get_db)
):
    """🗑️ Deletar todos os pedidos do banco (apenas admin)"""
    db.query(models.Pedido).delete()
    db.commit()
    return {"mensagem": "Todos os pedidos foram deletados com sucesso"}


@router.get("/{pedido_id}/detalhes")
def detalhes_pedido(
    pedido_id: int,
    usuario=Depends(role_required("cliente", "admin", "funcionario")),
    db: Session = Depends(get_db)
):
    """✅ CORRIGIDO: Retorna detalhes completos do pedido com nomes corretos"""
    pedido = db.query(models.Pedido).filter_by(id=pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    # Verificar permissão de acesso
    if usuario["tipo_usuario"] == "cliente" and pedido.cliente_id != usuario["usuario_id"]:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    itens_detalhados = []
    for item in pedido.itens:
        item_info = {
            "id": item.id,
            "quantidade": item.quantidade,
            "preco_unitario": item.preco_unitario,
            "preco_total": item.preco_total
        }
        
        if item.produto_id:
            item_info["tipo"] = "produto"
            item_info["nome"] = item.produto.nome if item.produto else "Produto Removido"
        elif item.produto_personalizado_id:
            item_info["tipo"] = "pizza_personalizada"
            pizza = item.produto_personalizado
            if pizza:
                item_info["nome"] = pizza.nome
                item_info["ingredientes"] = [
                    ing.ingrediente.nome for ing in pizza.ingredientes
                ] if pizza.ingredientes else []
            else:
                item_info["nome"] = "Pizza Personalizada Removida"
        
        itens_detalhados.append(item_info)
    
    return {
        "id": pedido.id,
        "descricao": pedido.descricao,
        "status": pedido.status,
        "valor_total": pedido.valor_total,
        "data_pedido": pedido.data_pedido,
        "itens": itens_detalhados
    }

@router.put("/{pedido_id}/status")
def atualizar_status(
    pedido_id: int,
    novo_status: str,
    usuario=Depends(role_required("admin", "funcionario")),
    db: Session = Depends(get_db)
):
    pedido = db.query(models.Pedido).filter_by(id=pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    pedido.status = novo_status
    db.commit()
    return {"msg": "Status atualizado", "status": novo_status}
