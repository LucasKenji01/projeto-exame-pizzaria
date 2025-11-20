# Script para executar o backend
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "========================================="
Write-Host "  Iniciando Backend da Pizzaria"
Write-Host "========================================="
Write-Host "Diretorio: $scriptPath"
Write-Host ""

# Verificar se o arquivo existe
if (Test-Path "start_backend.py") {
    Write-Host "Executando start_backend.py..."
    python start_backend.py
} else {
    Write-Host "Arquivo start_backend.py nao encontrado!"
    Write-Host "Tentando executar diretamente..."
    Set-Location "backend"
    python -m uvicorn pizzaria_api_pkg.main:app --host 0.0.0.0 --port 8000 --reload
}


