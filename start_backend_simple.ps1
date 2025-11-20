# Script para iniciar o backend
$ErrorActionPreference = "Stop"

# Obter o diretório do script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Adicionar backend ao PYTHONPATH
$backendDir = Join-Path $scriptDir "backend"
$env:PYTHONPATH = "$backendDir;$scriptDir"

Write-Host "Iniciando backend FastAPI..."
Write-Host "Diretório: $scriptDir"
Write-Host "PYTHONPATH: $env:PYTHONPATH"

# Iniciar uvicorn
python -m uvicorn pizzaria_api_pkg.main:app --host 0.0.0.0 --port 8000 --reload

