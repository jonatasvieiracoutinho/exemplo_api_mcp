# Troubleshooting

Problemas comuns ao rodar o projeto em ambiente local.

## Portas ocupadas

- **8000 (API)**, **5173 (frontend)** ou **8765 (MCP)** ja em uso.
  - Feche o processo em conflito ou ajuste as portas (`run_api.py`, `frontend/.env`, `config_mcp.json`).

## Banco SQLite travado

- Erro `database is locked` ou `cannot open file`.
  - Feche instancias antigas do backend/MCP.
  - Garanta que a pasta `data/` existe e voce tem permissao de escrita.

## Dependencias Python

- Erros como `ModuleNotFoundError`.
  - Confirme que o ambiente (conda/venv/uv) esta ativo.
  - Rode `pip install -r requirements.txt` novamente.

## Dependencias Node

- Erro `npm ERR! missing script: dev` ou `Cannot find module`.
  - Execute `npm install` dentro de `frontend` antes de `npm run dev`.

## CORS ao acessar de outro host

- Se voce mudar `VITE_API_URL` para outro host/porta, atualize `backend/api/main.py` para permitir a origem correta (ou configure um proxy).

## MCP Server nao responde

- Verifique se o processo esta ativo (`python run_mcp_server.py`).
- Confira `backend/mcp/config_mcp.json` (host/port).  
- Certifique-se de que o cliente MCP suporta `streamable-http`.

## Problemas com variaveis de ambiente

- `.env` nao aplicado.
  - Tenha certeza de que o arquivo existe na raiz e que o processo esta sendo executado a partir dela.
  - Em producao, prefira usar variaveis de ambiente reais (nao .env).
