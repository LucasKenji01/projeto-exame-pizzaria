#!/bin/bash
cd "$(dirname "$0")" || exit 1
VENV_PY="backend/pizzaria_api_pkg/.venv/Scripts/python.exe"
echo "Iniciando backend com: $VENV_PY"
echo "Comando: pizzaria_api_pkg.main:app (a partir da raiz)"
"$VENV_PY" -m uvicorn pizzaria_api_pkg.main:app --reload --host 0.0.0.0 --port 8000
