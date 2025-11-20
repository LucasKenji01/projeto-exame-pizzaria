from fastapi import Depends
from pizzaria_api_pkg.auth.rbac import get_usuario_autenticado

def get_usuario_logado(usuario=Depends(get_usuario_autenticado)):
    return usuario
