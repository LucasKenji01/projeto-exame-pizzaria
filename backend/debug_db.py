#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import json

# Conectar ao banco de dados
db_path = "pizzaria.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Obter um cliente da base
cursor.execute("SELECT id, usuario_id FROM clientes LIMIT 1")
cliente = cursor.fetchone()

if cliente:
    print(f"Cliente encontrado: {cliente}")
    print(f"Cliente ID: {cliente[0]}, Usuario ID: {cliente[1]}")
else:
    print("Nenhum cliente encontrado")

# Listar 3 itens do carrinho
cursor.execute("SELECT id, cliente_id, produto_id, quantidade FROM carrinho LIMIT 3")
items = cursor.fetchall()
print(f"\nItens do carrinho: {items}")

conn.close()
