from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    usuario_id: int
    tipo_usuario: str

    model_config = {
        "from_attributes": True
    }
