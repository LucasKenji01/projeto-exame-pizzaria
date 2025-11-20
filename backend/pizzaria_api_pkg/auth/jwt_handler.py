from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from os import getenv
from pizzaria_api_pkg.config import SECRET_KEY as CONFIG_SECRET_KEY, TOKEN_EXPIRATION_MINUTES as CONFIG_EXPIRATION

# Usar SECRET_KEY do .env se existir, senão usar o valor padrão do config.py
SECRET_KEY = getenv("SECRET_KEY") or CONFIG_SECRET_KEY
ALGORITHM = getenv("ALGORITHM", "HS256")
EXPIRATION_MINUTES = int(getenv("TOKEN_EXPIRATION_MINUTES", str(CONFIG_EXPIRATION)))

# Usar argon2 em vez de bcrypt (evita limites de 72 bytes)
try:
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
except Exception:
    # Fallback para bcrypt se argon2 não estiver disponível
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=4)

def criar_token(usuario_id: int, tipo_usuario: str) -> str:
    payload = {"sub": str(usuario_id), "role": tipo_usuario, "exp": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Token criado para usuario_id={usuario_id}, tipo_usuario={tipo_usuario}")
    print(f"Payload: {payload}")
    print(f"Token: {token[:50]}...")
    return token

def decodificar_token(token: str):
    """
    Decodifica e valida um token JWT.
    Retorna None se o token for inválido ou expirado.
    """
    try:
        print(f"Decodificando token: {token[:50]}...")
        print(f"SECRET_KEY: {SECRET_KEY[:20]}...")
        print(f"ALGORITHM: {ALGORITHM}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Payload decodificado: {payload}")
        usuario_id = payload.get("sub")
        tipo_usuario = payload.get("role")
        
        if not usuario_id or not tipo_usuario:
            print(f"Token inválido: faltando campos obrigatórios (sub: {usuario_id}, role: {tipo_usuario})")
            return None
        
        print(f"Token válido para usuario_id={usuario_id}, tipo_usuario={tipo_usuario}")
        return {"usuario_id": int(usuario_id), "tipo_usuario": tipo_usuario}
    except jwt.ExpiredSignatureError:
        print("Token expirado")
        return None
    except jwt.JWTError as e:
        print(f"Erro ao decodificar token: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado ao decodificar token: {e}")
        return None

def gerar_hash_senha(senha: str) -> str:
    # Limitar a 72 bytes para compatibilidade com bcrypt se necessário
    if len(senha) > 72:
        senha = senha[:72]
    try:
        return pwd_context.hash(senha)
    except Exception as e:
        # Fallback: usar uma senha simples se bcrypt falhar
        import hashlib
        print(f"Aviso: bcrypt falhou ({e}), usando sha256 como fallback")
        return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha: str, senha_hash: str) -> bool:
    if len(senha) > 72:
        senha = senha[:72]
    try:
        return pwd_context.verify(senha, senha_hash)
    except Exception:
        # Fallback: comparar hashes sha256
        import hashlib
        return hashlib.sha256(senha.encode()).hexdigest() == senha_hash

