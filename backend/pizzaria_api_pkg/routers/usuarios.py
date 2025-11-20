from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from pizzaria_api_pkg.database import get_db
from pizzaria_api_pkg.core_models import Usuario, Cliente
from pizzaria_api_pkg.auth.jwt_handler import gerar_hash_senha, verificar_senha, criar_token
from pizzaria_api_pkg.auth.rbac import get_usuario_autenticado
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

class ClienteCreate(BaseModel):
    nome: str
    email: str
    senha: str
    telefone: Optional[str]
    endereco: Optional[str]

class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: Optional[str]
    endereco: Optional[str]
    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    usuario_id: int
    tipo_usuario: str

class AlterarSenhaRequest(BaseModel):
    nova_senha: str
    confirmacao_senha: str

class AlterarSenhaResponse(BaseModel):
    mensagem: str
    success: bool

@router.post("/cadastro_completo", response_model=ClienteResponse)
def cadastro_completo(dados: ClienteCreate, db: Session = Depends(get_db)):
    """Cadastro completo de cliente com usuário"""
    if db.query(Usuario).filter(Usuario.email == dados.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo_usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        tipo_usuario="cliente"
    )
    db.add(novo_usuario)
    db.flush()

    novo_cliente = Cliente(
        usuario_id=novo_usuario.id,
        telefone=dados.telefone,
        endereco=dados.endereco
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return ClienteResponse(
        id=novo_cliente.id,
        nome=novo_usuario.nome,
        email=novo_usuario.email,
        telefone=novo_cliente.telefone,
        endereco=novo_cliente.endereco
    )

@router.post("/login", response_model=TokenResponse)
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Login de usuário"""
    usuario = db.query(Usuario).filter(Usuario.email == username).first()
    
    if not usuario or not verificar_senha(password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    token = criar_token(usuario.id, usuario.tipo_usuario)
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        usuario_id=usuario.id,
        tipo_usuario=usuario.tipo_usuario
    )

@router.get("/me")
def get_usuario_atual(
    usuario=Depends(get_usuario_autenticado),
    db: Session = Depends(get_db)
):
    """Retorna dados do usuário atual"""
    user = db.query(Usuario).filter(Usuario.id == usuario["usuario_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "tipo_usuario": user.tipo_usuario
    }

@router.post("/alterar-senha", response_model=AlterarSenhaResponse)
def alterar_senha(
    dados: AlterarSenhaRequest,
    usuario=Depends(get_usuario_autenticado),
    db: Session = Depends(get_db)
):
    """Altera a senha do usuário autenticado"""
    print(f"[alterar_senha] Usuario {usuario['usuario_id']} tentando alterar senha")
    
    # Validações básicas
    if not dados.nova_senha or not dados.confirmacao_senha:
        raise HTTPException(status_code=400, detail="Senha e confirmação são obrigatórias")
    
    if len(dados.nova_senha) < 6:
        raise HTTPException(status_code=400, detail="Senha deve ter no mínimo 6 caracteres")
    
    if dados.nova_senha != dados.confirmacao_senha:
        raise HTTPException(status_code=400, detail="As senhas não conferem")
    
    # Buscar usuário
    user = db.query(Usuario).filter(Usuario.id == usuario["usuario_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Atualizar senha
    try:
        user.senha_hash = gerar_hash_senha(dados.nova_senha)
        db.commit()
        print(f"[alterar_senha] ✓ Senha alterada com sucesso para usuario {usuario['usuario_id']}")
        return AlterarSenhaResponse(
            mensagem="Senha alterada com sucesso!",
            success=True
        )
    except Exception as e:
        db.rollback()
        print(f"[alterar_senha] ✗ Erro ao alterar senha: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao alterar senha")
