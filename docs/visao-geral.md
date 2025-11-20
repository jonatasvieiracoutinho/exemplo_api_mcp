# Visao geral

Este repositorio demonstra como acoplar um servidor MCP a uma aplicacao que ja possui backend REST e frontend. A ideia e mostrar, em um exemplo completo, que a camada de regras de negocio pode ser compartilhada entre:

- rotas HTTP tradicionais (FastAPI), consumidas por navegadores ou outras APIs; e
- tools MCP (FastMCP) consumidas por agentes/IDEs.

## Problema resolvido

Manter uma lista simples de livros com operacoes CRUD:

- listar, buscar, criar, atualizar e remover livros;
- campos basicos (titulo, autor, editora, link de compra);
- armazenamento em SQLite via SQLAlchemy.

## Escopo didatico

- Nao ha autenticacao, TLS, quotas ou rate limiting.
- O foco e **arquitetura + MCP**. Pressupoe que voce ja entende REST e frontend.
- Use apenas em ambiente local/de estudo. Para producao consulte [docs/checklist-seguranca.md](checklist-seguranca.md).

## Tecnologias

| Camada | Tecnologia principal | Observacoes |
| ------ | -------------------- | ----------- |
| API REST | FastAPI + Pydantic v2 | Rotas em `backend/api/endpoints.py`. Swagger em `/docs`. |
| Servico | Python puro + SQLAlchemy | `backend/services/book_service.py` orquestra CRUD e validacoes. |
| Banco | SQLite | Usado via SQLAlchemy; arquivo em `data/books.db`. |
| MCP Server | FastMCP | Configurado em `backend/mcp/server.py` com tools vindas de `MCPBookTools`. |
| Frontend | React + Vite + Axios | Tela unica em `frontend/src/pages/BooksPage.tsx`. |

## Fluxos principais

1. **Frontend → API REST**  
   React chama `/api/books` via Axios → FastAPI valida schema → `book_service` aplica regras → SQLAlchemy salva/busca → resposta em JSON.

2. **Cliente MCP → MCP Server**  
   IDE/Agente conecta no FastMCP (HTTP streamable) → descobre tools `books_*` → tool chama `MCPBookTools` → `book_service` → SQLAlchemy → resposta JSON-like para o agente.

No centro de tudo esta `backend/services/book_service.py`, garantindo consistencia entre os dois fluxos.
