from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.core_models import Produto as ProdutoModel, CategoriaProduto
from pizzaria_api_pkg.schemas.pizza_personalizada import TamanhoPizza
from pizzaria_api_pkg.schemas.produtos import Produto, ProdutoCreate
from pizzaria_api_pkg.auth.rbac import role_required

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/", response_model=list[Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoModel).all()

@router.post("/", response_model=Produto)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("admin", "funcionario"))
):
    novo_produto = ProdutoModel(**produto.dict(exclude={"tamanhos"}))
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

@router.post("/pizza_com_tamanhos", response_model=Produto)
def cadastrar_pizza_com_tamanhos(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("admin"))
):
    if produto.tipo.lower() != "pizza":
        raise HTTPException(status_code=400, detail="Tipo de produto deve ser 'pizza'")

    categoria = db.query(CategoriaProduto).filter(CategoriaProduto.id == produto.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    nova_pizza = ProdutoModel(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        tipo=produto.tipo,
        categoria_id=produto.categoria_id
    )
    db.add(nova_pizza)
    db.flush()

    if produto.tamanhos:
        for tamanho in produto.tamanhos:
            novo_tamanho = TamanhoPizza(
                nome=tamanho.nome,
                descricao=tamanho.descricao,
                preco=tamanho.preco,
                produto_id=nova_pizza.id
            )
            db.add(novo_tamanho)

    db.commit()
    db.refresh(nova_pizza)
    return nova_pizza

@router.delete("/excluir/{produto_id}", response_model=dict)
def excluir_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("admin"))
):
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return {"mensagem": "Produto excluído com sucesso"}

@router.get("/categoria/{categoria_id}", response_model=list[Produto])
def listar_produtos_por_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("admin"))
):
    produtos = db.query(ProdutoModel).filter(ProdutoModel.categoria_id == categoria_id).all()
    if not produtos:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado para esta categoria")
    return produtos

@router.get("/{produto_id}", response_model=Produto)
def buscar_produto_por_id(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto
