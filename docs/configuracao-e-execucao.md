# Configuracao e execucao

## Ambientes Python

### 1. Miniconda (recomendado)

1. Instale [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
2. Crie o ambiente:
   ```bash
   conda create -n exemplo_api_mcp python=3.11
   ```
3. Ative:
   ```bash
   conda activate exemplo_api_mcp
   ```
4. Instale dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. (Opcional) copie variaveis:
   ```bash
   cp env.example .env
   ```

### 2. venv (python padrão)

1. Criar:
   ```bash
   python -m venv .venv
   ```
2. Ativar:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`
3. Instalar deps: `pip install -r requirements.txt`

### 3. uv

1. Instale `uv` (https://github.com/astral-sh/uv).
2. Crie o ambiente:
   ```bash
   uv venv
   ```
3. Ative (igual ao venv).
4. Instale deps:
   ```bash
   uv pip install -r requirements.txt
   ```

> **Obs.:** qualquer que seja o metodo, nao versione `.venv`, `.conda` ou pastas semelhantes.

## Backend REST

Com o ambiente Python ativo:

```bash
pip install -r requirements.txt  # caso ainda nao tenha feito
python run_api.py
```

- Porta padrao: `8000`
- Swagger: `http://localhost:8000/docs`
- Base URL: `http://localhost:8000/api`

## Frontend

```bash
cd frontend
npm install
npm run dev
```

- Porta padrao: `5173`
- Ajuste `VITE_API_URL` em `frontend/.env` se mudar o backend.

## MCP Server

Com o mesmo ambiente Python do backend:

```bash
python run_mcp_server.py
```

- Porta padrao: `8765`
- Configuracao em `backend/mcp/config_mcp.json`
- Transporte: `streamable-http`

Para testar, use um cliente MCP compatível (ex.: IDE com suporte ou CLI do FastMCP) apontando para `http://localhost:8765`.

## Scripts rapidos (.bat /.sh)

Para facilitar workshops ou demos rapidas, use os scripts na raiz:

| Script Windows | Script Linux/Mac | O que faz |
| -------------- | ---------------- | --------- |
| `start_backend.bat` | `./start_backend.sh` | Ativa o ambiente `exemplo_api_mcp` (se houver conda) e roda `python run_api.py`. |
| `start_mcp_server.bat` | `./start_mcp_server.sh` | Mesma ideia, mas executa `python run_mcp_server.py`. |
| `start_frontend.bat` | `./start_frontend.sh` | Entra em `frontend/`, roda `npm install` (se `node_modules` nao existir) e executa `npm run dev`. |

> **Dica:** Nos scripts `.sh`, se o `conda` nao estiver disponivel, eles assumem que voce ja ativou o ambiente adequado antes de rodar.

## Sequencia sugerida

1. Ative o ambiente Python.
2. Rode `python run_api.py`.
3. Em outro terminal, rode o MCP Server (`python run_mcp_server.py`).
4. Em outro terminal, suba o frontend (`npm run dev`).
5. Navegue em `http://localhost:5173` e, em paralelo, use um cliente MCP para chamar as tools `books_*`.

## Consideracoes para producao

- Coloque API, frontend e MCP atras de HTTPS/TLS (proxy ou gateway).
- Injete variaveis sensiveis via Key Vault/secret manager; nao use `.env` versionado.
- Adicione autenticacao/autorizacao (gateway, middleware, OAuth2/OIDC, etc.).
- Aplique observabilidade (logs, metrics, tracing) e politicas de backup para o banco.
