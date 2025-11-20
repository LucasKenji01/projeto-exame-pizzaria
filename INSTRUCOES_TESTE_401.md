# Instruções para Testar a Correção do Erro 401

## Passo 1: Recarregar o Frontend
- Pressione **Ctrl+Shift+R** (hard refresh) no navegador para limpar cache e recarregar
- Feche DevTools se estiver aberto
- Aguarde a página recarregar completamente

## Passo 2: Limpar localStorage (IMPORTANTE!)
Abra DevTools (F12) → Console → Cole este comando:
```javascript
localStorage.clear(); console.log('localStorage limpo!');
```

## Passo 3: Fazer Login Novamente
1. Vá para a página de Login (http://localhost:4200/login)
2. Use email e senha do cadastro (exemplo: teste@email.com / senha123)
3. Clique no botão "Login"
4. **MONITORE O CONSOLE:**
   - Procure por mensagens começando com `✓` verde
   - Deve ver: `✓ Login response:` com os dados do usuário
   - Deve ver: `Token salvo: eyJhbGci...`

## Passo 4: Ir para Página Account
1. Clique no link "Account" ou navegue para http://localhost:4200/account
2. **MONITORE O CONSOLE - esperamos ver:**
   ```
   AccountComponent: Token encontrado? true
   AccountComponent: Token value eyJhbGci...
   AccountComponent: Fazendo requisição para /clientes/me
   ✓ getClienteInfo: Token encontrado? true
   ✓ getClienteInfo: Headers que serão enviados? YES (com Authorization)
   ✓ getClienteInfo: Fazendo requisição para GET /clientes/me
   JwtInterceptor: Adicionando token ao header da requisição para: http://localhost:8000/clientes/me
   JwtInterceptor: Token: eyJhbGci...
   ✓ getClienteInfo: SUCCESS - Resposta recebida: {id: ..., nome: ..., email: ...}
   AccountComponent: Sucesso ao carregar dados do cliente: {id: ..., nome: ..., email: ...}
   ```

## Passo 5: Verificar Backend Console
**Ao mesmo tempo no terminal do backend, procure por:**
```
================================================================================
[get_usuario_autenticado] ✓ INICIANDO VALIDAÇÃO DE TOKEN
[get_usuario_autenticado] URL: /clientes/me
[get_usuario_autenticado] Método: GET
[get_usuario_autenticado] Authorization header RAW: Bearer eyJhbGci...
[get_usuario_autenticado] Token via oauth2_scheme: eyJhbGci...
[get_usuario_autenticado] ✓ Token RECEBIDO: eyJhbGc...
[get_usuario_autenticado] ✓✓✓ SUCESSO - Usuário autenticado:
    - usuario_id: 1
    - tipo_usuario: cliente
================================================================================
```

## Passo 6: Resultado Esperado
✅ **SUCESSO:** Página mostra dados do usuário (nome, email, telefone, endereço)

❌ **AINDA FALHANDO:** Se ainda receber 401, verifique:

### Se vir no Console Frontend:
- `JwtInterceptor: Nenhum token disponível` → Token não está em localStorage
  - Solução: Fazer login novamente e verificar se salva mesmo

- `AccountComponent: Token encontrado? false` → localStorage vazio
  - Solução: Limpar e fazer login de novo

### Se vir no Console Backend:
- `❌ ERRO FATAL: Nenhum token foi fornecido!` → Frontend não está enviando Authorization header
  - Verifique Network tab (F12 → Network) → clique em `/clientes/me` → veja Headers
  - Procure por linha `Authorization: Bearer eyJh...`
  - Se não existir, o JwtInterceptor não está funcionando

## Passo 7: Debug Avançado (se ainda falhar)
Abra DevTools → Network Tab:
1. Clique na requisição `GET /clientes/me` 
2. Vá até aba "Request Headers"
3. Procure pela linha `authorization` (ou `Authorization`)
4. Se existir, deve ser: `Bearer eyJhbGciOiJIUzI1NiIs...`
5. Se não existir, o problema está no interceptor

## Resumo das Mudanças Feitas
1. ✅ Adicionado `HttpHeaders` ao AuthService
2. ✅ Modificado `getClienteInfo()` para enviar Authorization header manualmente
3. ✅ Verificado `JwtInterceptor` está registrado em `app.config.ts`
4. ✅ Adicionados logs detalhados em AccountComponent, AuthService, JwtInterceptor
5. ✅ Adicionados logs detalhados em `rbac.py` no backend

---

**Próxima ação:** Execute os passos acima e compartilhe:
1. Screenshot do console do frontend (mostrando os logs)
2. Screenshot do console do backend (mostrando os logs)
3. Me diga se os dados carregaram ou se ainda recebe 401
