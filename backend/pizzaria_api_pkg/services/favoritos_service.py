from sqlalchemy.orm import Session
from pizzaria_api_pkg.models.favoritos import Favorito
from pizzaria_api_pkg.core_models import Cliente
from fastapi import HTTPException

def adicionar_favorito(db: Session, usuario_id: int, produto_id: int):
    """Adiciona produto aos favoritos do cliente"""
    
    # ✅ CORREÇÃO: Buscar o cliente pelo usuario_id
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Usar cliente.id (PK) ao invés de usuario_id
    favorito = Favorito(cliente_id=cliente.id, produto_id=produto_id)
    db.add(favorito)
    db.commit()
    db.refresh(favorito)
    return favorito

def listar_favoritos(db: Session, usuario_id: int):
    """Lista favoritos do cliente"""
    
    # ✅ CORREÇÃO: Buscar o cliente pelo usuario_id
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Usar cliente.id para buscar favoritos
    return db.query(Favorito).filter_by(cliente_id=cliente.id).all()
