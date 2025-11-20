#!/usr/bin/env python3
"""
Script para iniciar o servidor FastAPI da pizzaria.
Execute a partir da raiz do projeto: python start_backend.py
"""
import sys
import os

# Adicionar a raiz do projeto e o diretório backend ao path do Python
project_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_root, "backend")
sys.path.insert(0, backend_dir)
sys.path.insert(0, project_root)

if __name__ == "__main__":
    import uvicorn
    
    print("Iniciando servidor FastAPI...")
    print(f"Diretório de trabalho: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}")
    
    try:
        uvicorn.run(
            "pizzaria_api_pkg.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"Erro ao iniciar servidor: {e}", file=sys.stderr)
        sys.exit(1)
