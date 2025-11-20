#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

# Conectar ao banco de dados
db_path = "pizzaria.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verificar estrutura da tabela carrinho
cursor.execute("PRAGMA table_info(carrinho)")
columns = cursor.fetchall()
print("Colunas da tabela carrinho:")
for col in columns:
    print(f"  - {col[1]}: {col[2]}")

# Verificar alguns itens do carrinho
cursor.execute("""
SELECT c.id, c.cliente_id, c.produto_id, c.quantidade, 
       p.nome, p.preco
FROM carrinho c
LEFT JOIN produtos p ON c.produto_id = p.id
LIMIT 5
""")
items = cursor.fetchall()
print(f"\nItens do carrinho (primeiros 5):")
for item in items:
    print(f"  ID: {item[0]}, Cliente: {item[1]}, Produto: {item[4]}, Qty: {item[3]}, Preco: {item[5]}")

conn.close()
