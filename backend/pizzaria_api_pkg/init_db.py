#!/usr/bin/env python3
"""
Script para inicializar o banco de dados criando as tabelas.
Execute a partir da raiz do projeto backend.
"""
import sys
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente ANTES de importar o resto
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Adicionar paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

if __name__ == "__main__":
    from pizzaria_api_pkg.database import Base, engine
    from pizzaria_api_pkg.core_models import Usuario, Cliente
    
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

