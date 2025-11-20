from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Criar app ANTES de importar routers
app = FastAPI(
    title="Pizzaria API",
    version="2.0",
    description="API para gerenciamento de pedidos, clientes e produtos da pizzaria."
)

# ✅ CORS - REGISTRAR ANTES DOS ROUTERS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importações dos routers DEPOIS de criar o app
from pizzaria_api_pkg.routers import (
    usuarios,
    clientes,
    pedidos,
    produtos,
    carrinho,
    entregas,
    cupons,
    ingredientes,
    pizza_personalizada,
    pagamentos,
    favoritos,
    enderecos,
    rastreamento,
    relatorios,
    routes_relatorios,
    admin,
    nuvem_sabores,
    nuvem_avaliadores,
    avaliacoes_detalhes,
    avaliacoes_relatorios
)

# ✅ IMPORTANTE: Registrar routers da API
app.include_router(usuarios.router, tags=["Usuários"])
app.include_router(clientes.router, tags=["Clientes"])
app.include_router(pedidos.router, tags=["Pedidos"])
app.include_router(produtos.router, tags=["Produtos"])
app.include_router(carrinho.router, tags=["Carrinho"])
app.include_router(entregas.router, tags=["Entregas"])
app.include_router(cupons.router, tags=["Cupons"])
app.include_router(ingredientes.router, tags=["Ingredientes"])
app.include_router(pizza_personalizada.router, tags=["Pizza Personalizada"])
app.include_router(pagamentos.router, tags=["Pagamentos"])
app.include_router(favoritos.router, tags=["Favoritos"])
app.include_router(enderecos.router, tags=["Endereços"])
app.include_router(rastreamento.router, tags=["Rastreamento"])
app.include_router(relatorios.router, tags=["Relatórios"])
app.include_router(routes_relatorios.router, tags=["Relatórios Vendas"])
app.include_router(nuvem_sabores.router, tags=["Nuvem Sabores"])
app.include_router(admin.router, tags=["Admin"])
app.include_router(nuvem_avaliadores.router, tags=["Nuvem Avaliadores"])
app.include_router(avaliacoes_detalhes.router, tags=["Avaliações Detalhes"])
app.include_router(avaliacoes_relatorios.router, tags=["Avaliações Relatórios"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.0"}

@app.get("/test-cors")
def test_cors():
    """Endpoint simples para testar CORS - sem dependências de BD"""
    return {"message": "CORS funcionando!", "timestamp": "2025-11-18"}


# ✅ Montar frontend DEPOIS de registrar as rotas da API
# app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("pizzaria_api_pkg.main:app", host="127.0.0.1", port=8000, reload=True)