from sqlalchemy.orm import Session
from pizzaria_api_pkg.models.enderecos import Endereco
from pizzaria_api_pkg.core_models import Cliente
from fastapi import HTTPException

def adicionar_endereco(db: Session, usuario_id: int, dados):
    """Adiciona endereço mapeando campos antigos para novos"""
    
    # ✅ CORREÇÃO: Buscar o cliente pelo usuario_id
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Converte o schema para dict
    dados_dict = dados.model_dump()  # Pydantic v2
    
    # Mapeia campos antigos para novos
    if 'rua' in dados_dict:
        dados_dict['logradouro'] = dados_dict.pop('rua')
    
    if 'favorito' in dados_dict:
        dados_dict['padrao'] = dados_dict.pop('favorito')
    
    # Garante que apelido está presente
    if 'apelido' not in dados_dict or not dados_dict['apelido']:
        dados_dict['apelido'] = "Casa"
    
    # ✅ CORREÇÃO: Usar cliente.id (PK) ao invés de usuario_id
    endereco = Endereco(cliente_id=cliente.id, **dados_dict)
    db.add(endereco)
    db.commit()
    db.refresh(endereco)
    return endereco

def listar_enderecos(db: Session, usuario_id: int):
    """Lista endereços do cliente"""
    
    # ✅ CORREÇÃO: Buscar o cliente pelo usuario_id
    cliente = db.query(Cliente).filter(Cliente.usuario_id == usuario_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Usar cliente.id para buscar endereços
    return db.query(Endereco).filter_by(cliente_id=cliente.id).all()
