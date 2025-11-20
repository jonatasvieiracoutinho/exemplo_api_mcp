#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

echo "========================================"
echo "Iniciando Frontend - React"
echo "========================================"
echo

cd "$FRONTEND_DIR"

if [ ! -d "node_modules" ]; then
  echo "Dependencias nao encontradas. Instalando npm install..."
  npm install
fi

echo "Executando npm run dev (porta padrao 5173). Pressione Ctrl+C para encerrar."
npm run dev
