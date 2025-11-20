from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg import models, schemas
from pizzaria_api_pkg.auth.rbac import role_required
from pizzaria_api_pkg.schemas.categorias_produto import CategoriaProduto, CategoriaProdutoCreate

router = APIRouter(prefix="/categorias_produto", tags=["Categorias de Produto"])

@router.post("/criar", response_model=schemas.CategoriaProduto)
def criar_categoria(
    categoria: schemas.CategoriaProdutoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(role_required("admin"))
):
    categoria_existente = db.query(models.CategoriaProduto).filter(
        models.CategoriaProduto.nome.ilike(categoria.nome)
    ).first()
    if categoria_existente:
        raise HTTPException(status_code=400, detail="Categoria já cadastrada")

    nova_categoria = models.CategoriaProduto(nome=categoria.nome)
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria

@router.get("/", response_model=list[schemas.CategoriaProduto])
def listar_categorias(
    db: Session = Depends(get_db),
    usuario=Depends(role_required("admin"))
):
    return db.query(models.CategoriaProduto).all()
