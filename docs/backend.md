# Backend (FastAPI + Servicos + SQLAlchemy)

O backend ja segue uma arquitetura em camadas familiar para APIs REST. Esta pagina serve apenas como mapa para quem ja conhece FastAPI.

## Configuracao

- `backend/config.py`  
  Usa `pydantic-settings` para ler variaveis (ex.: `DATABASE_URL`) a partir de `.env`. Este arquivo existe apenas para facilitar o estudo. Em ambiente real, injete valores a partir de Key Vault/secret manager e nao versione `.env`.

- `backend/database/connection.py`  
  Monta o `engine`, cria `SessionLocal` e oferece `init_db`, `get_db`, `get_db_dependency`. Aqui tambem fica o caminho padrao do SQLite (`data/books.db`). Em producao, redirecione para o banco escolhido (Postgres, MySQL etc.), com credenciais vindas de fonte segura.

## API HTTP

- `backend/api/main.py`  
  Instancia o FastAPI, aplica `CORSMiddleware` (com `allow_origins=["*"]` apenas para ambiente local) e registra o router `/api/books`. Nao ha autenticacao nem autorizacao implementadas; adicione-as via dependencias ou proxies em um projeto real.

- `backend/api/endpoints.py`  
  Define as rotas `GET/POST/PUT/PATCH/DELETE`. Cada funcao:
  1. Valida parametros com Pydantic (`schemas.py`).
  2. Solicita uma sessao (`Depends(get_db_dependency)`).
  3. Chama o `book_service`.
  4. Traduz excecoes em respostas HTTP (404, 422 etc.).

- `backend/api/schemas.py`  
  Modelos Pydantic (v2) para entrada e saida (`BookCreate`, `BookUpdate`, `BookOut`). Validam o minimo necessario (ex.: titulo obrigatorio) antes de chegar na camada de servicos.

Documentacao detalhada de cada rota em [docs/api-http.md](api-http.md).

## Servicos (book_service)

Arquivo chave: `backend/services/book_service.py`.

- `create_book`, `list_books`, `get_book`, `update_book`, `delete_book`, `search_books`.
- Validacoes de negocio:
  - titulo nao pode ser vazio (com trim);
  - `limit` limitado a 500, `offset` >= 0;
  - busca exige pelo menos 1 caractere.
- Excecoes:
  - `BookNotFoundError` quando o ID nao existe;
  - `ValueError` para parametros invalidos.

Essa camada e chamada tanto pelos endpoints HTTP quanto pelas tools MCP.

## Persistencia

- `backend/database/models.py`  
  Modelo `Book` com indices em `title/author/publisher`, campo `created_at` e metodo `to_dict`.

- `backend/database/crud.py`  
  Operacoes de banco (selects com `limit/offset`, `ilike` para busca, `db.flush()` para obter IDs).

- `backend/database/connection.py`  
  Alem das funcoes mencionadas acima, garante `commit/rollback` automatico e cria a pasta `data/` se nao existir.

## Pontos de extensao

- Quer adicionar um novo campo? Atualize `Book` (ORM), schemas Pydantic, `book_service` e, automaticamente, API REST + MCP refletirao a mudanca.
- Precisa de validacao extra? Centralize em `book_service`.
- Vai endurecer seguranca? Adicione middlewares/dependencias em `backend/api/main.py` ou proteja via gateway externo.
