# Instruções para Rodar Backend e Frontend

## Diagnóstico do erro 401

As seguintes correções foram implementadas:

### Frontend (Angular)
✅ **`auth.service.ts`**: Adicionados logs ao login() e getClienteInfo()
✅ **`jwt.interceptor.ts`**: Adicionados logs para diagnosticar envio de token

### Backend (FastAPI)
✅ **`jwt_handler.py`**: Adicionados logs ao criar_token() e decodificar_token()
✅ **`rbac.py`**: Adicionados logs ao get_usuario_autenticado()

## Passos para Rodar

### 1. Terminal 1 - Backend (FastAPI)

```bash
cd backend/pizzaria_api_pkg
.\.venv\Scripts\python.exe -m uvicorn pizzaria_api_pkg.main:app --host 0.0.0.0 --port 8000 --reload
```

Ou em PowerShell:
```powershell
cd 'D:\Lucas\FACULDADE EXAME\3º Semestre\Projeto Integrador\projeto\backend\pizzaria_api_pkg'
.\.venv\Scripts\python.exe -m uvicorn pizzaria_api_pkg.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Terminal 2 - Frontend (Angular)

```bash
cd frontend/projeto-pizzaria
ng serve
```

Ou:
```bash
npm start
```

## Testando a Aplicação

1. **Abrir no navegador**: http://localhost:4200
2. **Fazer cadastro/login** → Verifique os logs do console (F12 → Console)
3. **Clicar em Account** → Verifique se o token é enviado no header Authorization

## Verificando Logs

### No Chrome DevTools (Frontend)
- F12 → Console → Procure por:
  - "Login response:"
  - "JwtInterceptor: Adicionando token"
  - "getClienteInfo response:" (sucesso) ou erro

### No Terminal do Backend (Uvicorn)
- Procure por:
  - "Token criado para usuario_id="
  - "[get_usuario_autenticado] Token recebido:"
  - "[get_usuario_autenticado] Usuário autenticado:"

## Se Still der 401

1. **Verificar se o token é salvo no localStorage:**
   - F12 → Application → Local Storage → "access_token"

2. **Verificar se o token é enviado no header:**
   - F12 → Network → Clique na requisição /clientes/me
   - Headers → Authorization: Bearer [token]

3. **Verificar se o backend está recebendo o token:**
   - Procure por "[get_usuario_autenticado] Token recebido:" no terminal do backend

## Próximos Passos

Se o erro persistir, os logs fornecerão pistas sobre:
- Token não está sendo salvo no localStorage
- Token não está sendo enviado no header
- Token está sendo criado incorretamente (payload inválido)
- Token está expirado
