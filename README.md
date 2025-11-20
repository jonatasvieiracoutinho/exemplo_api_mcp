# Exemplo API MCP - Catalogo de Livros

Aplicacao didatica que mostra como evoluir uma stack comum (FastAPI + SQLAlchemy + React) para incluir um servidor MCP reutilizando a mesma camada de servicos. O repositorio existe para estudo guiado: voce sobe a API REST e o frontend tradicionais, e no mesmo backend habilita um MCP Server que expoe as mesmas operacoes de livros para agentes.

> **Importante**  
> Este projeto nao contem autenticacao, TLS, rate limiting ou qualquer outro controle de hardening. Rode apenas em ambiente local/de estudo. Para producao, siga as orientacoes em [docs/checklist-seguranca.md](docs/checklist-seguranca.md).

## Stack e foco didatico

- **Backend REST**: FastAPI, SQLAlchemy, SQLite.
- **MCP Server**: FastMCP expondo tools ligadas ao `book_service`.
- **Frontend**: React + Vite + Axios.
- **Regra de negocio unica**: `backend/services/book_service.py` concentra as validacoes e o fluxo CRUD consumido por REST e MCP.

## Arquitetura em alto nivel

```
Frontend (React)  -->  FastAPI /api/books  -->  book_service  -->  SQLAlchemy/SQLite
Cliente MCP       -->  FastMCP Server     -->  book_service  -->  SQLAlchemy/SQLite
```

Diagrama completo em [docs/arquitetura.md](docs/arquitetura.md) (usa `docs/architecture.svg`).

## Como estudar rapidamente

1. Leia [docs/visao-geral.md](docs/visao-geral.md) para entender o objetivo e as camadas.
2. Veja [docs/backend.md](docs/backend.md) para localizar rotas, schemas e servicos.
3. Estude [docs/mcp_server.md](docs/mcp_server.md): mostra como o MCP Server nasce e consome os mesmos servicos.
4. Rode o projeto seguindo [docs/configuracao-e-execucao.md](docs/configuracao-e-execucao.md).
5. Explore o frontend (arquivos descritos em [docs/frontend.md](docs/frontend.md)) e compare com o fluxo MCP.

## Como rodar (resumo)

1. Configure o ambiente Python (conda, venv ou uv) conforme [docs/configuracao-e-execucao.md](docs/configuracao-e-execucao.md#ambientes-python).
2. Ative o ambiente e instale `pip install -r requirements.txt`.
3. Suba o backend REST: `python run_api.py` (ou `start_backend.bat` / `./start_backend.sh`).
4. Suba o frontend:
   ```bash
   cd frontend
   npm install
   npm run dev  # ou start_frontend.bat / ./start_frontend.sh
   ```
5. Rode o MCP Server: `python run_mcp_server.py` (ou `start_mcp_server.bat` / `./start_mcp_server.sh`; porta 8765, transporte streamable-http).

## Referencias rapidas

| Area | Arquivos chave |
| ---- | --------------- |
| API REST | `backend/api/main.py`, `backend/api/endpoints.py`, `backend/api/schemas.py` |
| Servicos | `backend/services/book_service.py` |
| Persistencia | `backend/database/models.py`, `backend/database/crud.py`, `backend/database/connection.py` |
| MCP | `backend/mcp/server.py`, `backend/mcp/mcp_tools.py`, `backend/mcp/config_mcp.json` |
| Frontend | `frontend/src/pages/BooksPage.tsx`, `frontend/src/components/*`, `frontend/src/api/*` |

Detalhes em [docs/backend.md](docs/backend.md), [docs/mcp_server.md](docs/mcp_server.md) e [docs/frontend.md](docs/frontend.md).

## API HTTP em um minuto

Endpoints sob `http://localhost:8000/api`:

- `GET /books?limit=100&offset=0` — lista livros (ordenacao por criacao desc).
- `GET /books/search?query=texto` — busca em titulo/autor/editora.
- `GET /books/{id}` — detalhe.
- `POST /books` — cria (body `BookCreate`).
- `PUT /books/{id}` — atualiza completo.
- `PATCH /books/{id}` — atualiza parcial.
- `DELETE /books/{id}` — remove.

Documentacao completa + exemplos em [docs/api-http.md](docs/api-http.md).

## Segurança e producao

Este codigo fica propositalmente aberto para facilitar o estudo. Para levar qualquer parte ao mundo real, voce deve:

1. **Proteger com HTTPS** (API REST, frontend, MCP Server) via proxy/gateway com TLS.
2. **Adicionar autenticacao/autorizacao** conforme a politica da empresa (OAuth2/OIDC, API Gateway, etc).
3. **Aplicar rate limiting/WAF e CORS restritivo**.
4. **Mover segredos/chaves para Key Vaults** (Azure Key Vault, AWS Secrets Manager, HashiCorp Vault).
5. **Habilitar logs/auditoria e observabilidade**.
6. **Planejar backup/criptografia do banco**.

Detalhes e checklist: [docs/checklist-seguranca.md](docs/checklist-seguranca.md).

## Proximos passos sugeridos

- Adicionar autenticao/autorizacao nas rotas e no MCP Server.
- Criar testes automatizados (Pytest para backend, React Testing Library para frontend).
- Incluir paginação/UX mais rica no frontend.
- Evoluir o `book_service` para novos campos ou regras e observar como REST e MCP se beneficiam juntos.

## Navegue pelos docs

- [Visao geral](docs/visao-geral.md)
- [Arquitetura detalhada](docs/arquitetura.md)
- [Backend](docs/backend.md)
- [MCP server](docs/mcp_server.md)
- [Frontend](docs/frontend.md)
- [API HTTP](docs/api-http.md)
- [Configuracao e execucao (conda/venv/uv)](docs/configuracao-e-execucao.md)
- [Checklist de seguranca](docs/checklist-seguranca.md)
- [Troubleshooting](docs/troubleshooting.md)

Bom estudo! Qualquer duvida abra uma issue ou adapte o plano descrito aqui.
