# API HTTP (FastAPI)

Base URL padrao: `http://localhost:8000/api`

## Tabela de endpoints

| Metodo | Rota | Descricao | Parametros chave | Codigos | Implementacao | Observacoes de seguranca |
| ------ | ---- | --------- | ---------------- | ------- | ------------- | ------------------------- |
| GET | `/books` | Lista livros em ordem decrescente de criacao | Query `limit` (1-500), `offset` (>=0) | 200 | `endpoints.list_books` → `book_service.list_books` | Em producao, exigir auth e aplicar rate limiting |
| GET | `/books/search` | Busca por palavra-chave em titulo/autor/editora | Query `query` (>=1 caractere), `limit`, `offset` | 200, 422 | `endpoints.search_books` → `book_service.search_books` | Proteja contra abuso (rate limit + logs) |
| GET | `/books/{id}` | Retorna um livro especifico | Path `id` >= 1 | 200, 404 | `endpoints.get_book` → `book_service.get_book` | Requer autenticao em producao |
| POST | `/books` | Cria livro | Body `BookCreate` (`title` obrigatorio) | 201, 422 | `endpoints.create_book` → `book_service.create_book` | Validar payload e auditar criacoes |
| PUT | `/books/{id}` | Atualiza livro completo | Path `id`, body `BookCreate` | 200, 404, 422 | `endpoints.update_book` → `book_service.update_book` | Exigir permissao para editar |
| PATCH | `/books/{id}` | Atualiza campos parciais | Path `id`, body `BookUpdate` | 200, 404, 422 | `endpoints.patch_book` → `book_service.update_book` | Mesmo controle do PUT |
| DELETE | `/books/{id}` | Remove livro | Path `id` | 204, 404 | `endpoints.delete_book` → `book_service.delete_book` | Logar remocoes e exigir permissao |

## Schemas

| Nome | Arquivo | Campos |
| ---- | ------- | ------ |
| `BookCreate` | `backend/api/schemas.py` | `title` (obrigatorio), `author?`, `publisher?`, `purchase_link?` |
| `BookUpdate` | `backend/api/schemas.py` | Mesmos campos, todos opcionais. |
| `BookOut` | `backend/api/schemas.py` | `id`, `title`, `author?`, `publisher?`, `purchase_link?`, `created_at`. |

## Exemplos de uso

```bash
# Criar
curl -X POST http://localhost:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{"title":"O Senhor dos Aneis","author":"J. R. R. Tolkien"}'

# Buscar
curl "http://localhost:8000/api/books/search?query=tolkien&limit=5"

# Atualizar parcial
curl -X PATCH http://localhost:8000/api/books/1 \
  -H "Content-Type: application/json" \
  -d '{"publisher":"HarperCollins"}'

# Excluir
curl -X DELETE http://localhost:8000/api/books/1
```

## Swagger / OpenAPI

- Disponivel em `http://localhost:8000/docs` (Swagger UI).
- JSON em `http://localhost:8000/openapi.json`.

## Consideracoes

- A API nao realiza autenticao/autorizacao: adicione conforme seu contexto (API Gateway, OAuth2 etc.).
- Limite as origens CORS e use HTTPS quando exposta fora da maquina local.
