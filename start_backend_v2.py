#!/usr/bin/env python
import sys
import os

# Adicionar dirs ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.dirname(__file__))

# Forçar carregar .env ANTES de qualquer import
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), 'backend', 'pizzaria_api_pkg', '.env')
load_dotenv(env_path)

# AGORA importar o app
import uvicorn
from pizzaria_api_pkg.main import app

if __name__ == "__main__":
    print("Iniciando Uvicorn...")
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
    uvicorn.run(
        "pizzaria_api_pkg.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
