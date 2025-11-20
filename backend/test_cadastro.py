#!/usr/bin/env python
import sys
sys.path.insert(0, 'pizzaria_api_pkg')
sys.path.insert(0, '.')

from fastapi import FastAPI
from pizzaria_api_pkg.routers.usuarios import cadastro_completo, ClienteCreate
from pizzaria_api_pkg.database import SessionLocal
from pizzaria_api_pkg.dependencies import get_db

# Simular a chamada com dependência
app = FastAPI()

@app.post("/test")
def test(dados: ClienteCreate, db = ...):
    try:
        return cadastro_completo(dados, db)
    except Exception as e:
        import traceback
        print("ERRO COMPLETO:")
        traceback.print_exc()
        return {"error": str(e), "type": type(e).__name__}

# Testar chamada direta
if __name__ == "__main__":
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    response = client.post(
        "/test",
        json={
            "nome": "Test",
            "email": "test999@test.com",
            "senha": "123456",
            "telefone": "11999999999",
            "endereco": "Rua"
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
