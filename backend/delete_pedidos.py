#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

# Tentar pizzaria.db na raiz do backend
db_path = "pizzaria.db"
if not os.path.exists(db_path):
    db_path = "pizzaria_db/operacional.db"

print(f"Usando banco: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Listar tabelas para debugar
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"Tabelas disponíveis: {tables}")

# Deletar todos os registros da tabela pedidos
try:
    cursor.execute("DELETE FROM pedidos")
    conn.commit()
    
    # Verificar quantos pedidos ficaram
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    count = cursor.fetchone()[0]
    print("Pedidos deletados com sucesso!")
    print(f"Pedidos restantes: {count}")
except Exception as e:
    print(f"Erro: {e}")

conn.close()
