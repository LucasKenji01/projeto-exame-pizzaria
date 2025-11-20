from sqlalchemy.orm import Session
from pizzaria_api_pkg.core_models import Cliente
from fastapi import HTTPException

def atualizar_dados_cliente(db: Session, usuario_id: int, telefone: str = None, endereco: str = None):
    """Atualiza dados do cliente"""
    
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    if telefone is not None:
        cliente.telefone = telefone
    
    if endereco is not None:
        cliente.endereco = endereco
    
    db.commit()
    db.refresh(cliente)
    
    return cliente
