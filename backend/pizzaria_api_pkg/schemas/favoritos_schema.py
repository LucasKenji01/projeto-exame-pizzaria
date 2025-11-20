from pydantic import BaseModel
from datetime import datetime

class FavoritoCreate(BaseModel):
    produto_id: int

class FavoritoOut(BaseModel):
    id: int
    produto_id: int
    cliente_id: int
    # ✅ Usar data_adicao conforme migration, mas aceitar criado_em também
    data_adicao: datetime
    
    class Config:
        from_attributes = True
        # Permite que o campo criado_em seja mapeado de data_adicao
        populate_by_name = True
        
    # Propriedade para compatibilidade
    @property
    def criado_em(self):
        return self.data_adicao
