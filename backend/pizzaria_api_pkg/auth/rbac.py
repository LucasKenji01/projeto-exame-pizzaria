from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodificar_token
from typing import Optional
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login", auto_error=False)
http_bearer = HTTPBearer(auto_error=False)

def get_usuario_autenticado(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer)
):
    """
    Obtém o usuário autenticado a partir do token JWT.
    Aceita token via OAuth2PasswordBearer ou HTTPBearer.
    """
    print("="*80)
    print(f"[get_usuario_autenticado] ✓ INICIANDO VALIDAÇÃO DE TOKEN")
    print(f"[get_usuario_autenticado] URL: {request.url.path}")
    print(f"[get_usuario_autenticado] Método: {request.method}")
    print(f"[get_usuario_autenticado] Authorization header RAW: {request.headers.get('Authorization')}")
    print(f"[get_usuario_autenticado] Token via oauth2_scheme: {token[:30] + '...' if token else 'None'}")
    print(f"[get_usuario_autenticado] Credentials via HTTPBearer: {credentials}")
    
    # Tentar obter token do OAuth2PasswordBearer primeiro
    if not token and credentials:
        # Se não veio pelo OAuth2, tentar pelo HTTPBearer
        token = credentials.credentials
        print(f"[get_usuario_autenticado] ✓ Token obtido via HTTPBearer: {token[:30]}...")
    
    # Se ainda não tiver token, tentar obter do header Authorization diretamente
    if not token:
        auth_header = request.headers.get("Authorization")
        print(f"[get_usuario_autenticado] Tentando obter token do header Authorization: {auth_header}")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            print(f"[get_usuario_autenticado] ✓ Token extraído do header: {token[:30]}...")
        else:
            print(f"[get_usuario_autenticado] ❌ Header Authorization não encontrado ou não é Bearer")
    
    if not token:
        print(f"[get_usuario_autenticado] ❌ ERRO FATAL: Nenhum token foi fornecido!")
        logger.warning("Token não fornecido na requisição")
        print("="*80)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"[get_usuario_autenticado] ✓ Token RECEBIDO: {token[:50]}...")
    dados = decodificar_token(token)
    
    if not dados:
        print(f"[get_usuario_autenticado] ❌ ERRO: Token inválido ou expirado")
        logger.warning("Token inválido ou expirado")
        print("="*80)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"[get_usuario_autenticado] ✓✓✓ SUCESSO - Usuário autenticado:")
    print(f"    - usuario_id: {dados.get('usuario_id')}")
    print(f"    - tipo_usuario: {dados.get('tipo_usuario')}")
    print("="*80)
    logger.info(f"Usuário autenticado: {dados.get('usuario_id')}")
    return dados

def role_required(*roles):
    def wrapper(usuario=Depends(get_usuario_autenticado)):
        if usuario["tipo_usuario"] not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
        return usuario
    return wrapper
