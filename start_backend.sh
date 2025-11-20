#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "Iniciando Backend - API FastAPI"
echo "========================================"
echo

if command -v conda >/dev/null 2>&1; then
  eval "$(conda shell.bash hook)"
  if ! conda activate exemplo_api_mcp >/dev/null 2>&1; then
    echo "Nao foi possivel ativar o ambiente 'exemplo_api_mcp'."
    echo "Crie com: conda create -n exemplo_api_mcp python=3.11 -y"
    exit 1
  fi
else
  echo "Conda nao encontrado. Assumindo que o ambiente virtual ja esta ativo."
fi

echo "Executando API em http://localhost:8000 ..."
python run_api.py
