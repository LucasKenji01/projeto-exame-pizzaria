#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import http.client

# Conectar ao servidor
conn = http.client.HTTPConnection("localhost", 8000)

# 1. Login para obter token
headers = {"Content-Type": "application/json"}
body = json.dumps({"username": "cliente@teste.com", "password": "senha123"})

conn.request("POST", "/usuarios/login", body, headers)
response = conn.getresponse()
data = response.read().decode()
print(f"Status Login: {response.status}")

if response.status == 200:
    login_resp = json.loads(data)
    token = login_resp.get("access_token")
    print(f"Token obtido: {token[:50]}...")
    
    # 2. Tentar DELETE de um item existente (ID 3)
    headers_with_auth = {"Authorization": f"Bearer {token}"}
    item_id = 3
    
    print(f"\nTentando DELETE /carrinho/{item_id}")
    conn.request("DELETE", f"/carrinho/{item_id}", "", headers_with_auth)
    del_response = conn.getresponse()
    del_data = del_response.read().decode()
    print(f"Status DELETE: {del_response.status}")
    print(f"Response: {del_data}")
else:
    print(f"Erro no login: {data}")

conn.close()
