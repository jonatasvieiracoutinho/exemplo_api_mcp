# MCP Server em detalhe

Esta e a parte mais importante do exemplo. Aqui voce ve como um servidor MCP pode nascer dentro do mesmo backend e reutilizar integralmente a camada de servicos.

## Conceitos rapidos

- **MCP Server**: processo que registra tools (operacoes) para serem consumidas por um cliente MCP (IDE, agente, automacao).
- **FastMCP**: biblioteca que facilita a criacao do servidor MCP com decorators semelhantes aos do FastAPI.
- **Tool**: funcao remota descrita por nome, parametros e texto de ajuda. O cliente MCP descobre tools e as chama dinamicamente.

Neste projeto, cada tool MCP faz exatamente o mesmo que as rotas HTTP `/api/books`. A diferenca esta apenas no protocolo.

## Arquivos principais

| Arquivo | Papel |
| ------- | ----- |
| `backend/mcp/config_mcp.json` | Define nome/versao/host/porta do servidor MCP e quais tools estao habilitadas. |
| `backend/mcp/server.py` | Carrega a configuracao, registra tools e inicia o FastMCP (`transport=streamable-http`). |
| `backend/mcp/mcp_tools.py` | Classe `MCPBookTools` com metodos que chamam `book_service` e devolvem dicionarios serializaveis. |

## `config_mcp.json`

Exemplo (resumido):

```json
{
  "server": {
    "name": "book-catalog-mcp",
    "version": "0.1.0",
    "host": "0.0.0.0",
    "port": 8765
  },
  "endpoints": [
    { "name": "books_add", "enabled": true, "description": "Cria um livro" },
    ...
  ]
}
```

- Alterar `enabled` para `false` remove a tool sem tocar em codigo.
- `description` e exibido para o cliente MCP como ajuda textual.

## `backend/mcp/server.py`

Fluxo principal:

1. Carrega `config_mcp.json`.
2. `init_db()` garante que o banco existe antes das tools rodarem.
3. Instancia `FastMCP` com `name/version`.
4. Cria `MCPBookTools` (adaptador do `book_service`).
5. Chama `register_tools(server, tools)`:
   - Para cada entrada habilitada no JSON, registra um decorator `@server.tool(...)`.
   - Cada tool MCP chama o metodo correspondente de `MCPBookTools`.
6. Inicia `server.run(transport="streamable-http", host=..., port=...)`.

### Como o decorator funciona

Exemplo abreviado:

```python
if is_tool_enabled("books_add"):
    @server.tool(name="books_add", description=get_tool_description("books_add"))
    def tool_books_add(title: str, author: str | None = None, ...):
        return tools.books_add(title, author, ...)
```

Quando o cliente MCP invoca `books_add`, o FastMCP executa `tool_books_add`, que delega para `MCPBookTools.books_add`.

## `backend/mcp/mcp_tools.py`

`MCPBookTools` encapsula as operacoes reais:

- Usa `get_db()` (context manager) para abrir uma sessao SQLAlchemy.
- Chama `book_service.*` para manter as mesmas regras de negocio da API HTTP.
- Converte o resultado para `dict` via `_to_dict`, para facilitar a serializacao em JSON.

### Metodos disponiveis

| Metodo | Tool MCP | Descricao |
| ------ | -------- | --------- |
| `books_add` | `books_add` | Cria livro (campos opcionais autor/editora/link). |
| `books_update` | `books_update` | Atualiza livro (total ou parcial). |
| `books_delete` | `books_delete` | Remove livro pelo ID. |
| `books_get` | `books_get` | Busca um unico livro. |
| `books_list` | `books_list` | Lista livros com `limit/offset`. |
| `books_search` | `books_search` | Busca por palavra-chave em titulo/autor/editora. |

### Exemplo de fluxo `books_search`

1. Cliente MCP envia:  
   ```
   {
     "tool": "books_search",
     "arguments": { "query": "tolkien", "limit": 5 }
   }
   ```
2. FastMCP executa `tool_books_search(...)` (gerado em `register_tools`).
3. Este chama `MCPBookTools.books_search`.
4. `books_search` valida `query`, abre DB (`with get_db() as db:`) e chama `book_service.search_books`.
5. CRUD executa `SELECT ... WHERE title ILIKE '%tolkien%'`.
6. Resultado vira `List[Dict[str, Any]]` e e enviado ao cliente MCP.

## Erros e propagacao

- `ValueError` (por exemplo, `query` vazia) gera uma falha de tool retornada ao cliente MCP.
- `book_service.BookNotFoundError` e propagado como erro da tool, permitindo que o cliente trate (por exemplo, exibindo mensagem).

## Consideracoes de seguranca

- O servidor MCP aqui roda em `http://0.0.0.0:8765` sem TLS, autenticao ou autorizacao. Isso e aceitavel apenas em laboratorio.
- Em ambiente real:
  - Use HTTPS (ou tunel seguro) e autentique o cliente (por exemplo, rodando localmente dentro da IDE ou atras de gateway).
  - Controle quem pode acessar cada tool (escopo/profiling no cliente ou no servidor).
  - Qualquer segredo (tokens de APIs externas, etc.) deve vir de Key Vault/secret manager, nao de `.env`.

## Checklist rapida antes de escrever novas tools

1. Adicione o metodo em `MCPBookTools` chamando `book_service`.
2. Atualize `config_mcp.json` com `name`, `enabled`, `description`.
3. Garanta que `register_tools` registre a nova tool (segue o mesmo padrao).
4. Opcional: exponha a mesma funcao via REST para manter paridade entre os canais.

## Exemplo de configuracao de cliente MCP (Cursor)

Cada cliente MCP tem seu proprio formato de configuracao. No Cursor, por exemplo,
voce adicionaria algo como o snippet abaixo ao arquivo `mcp.json`:

```json
"catalogo-pessoal-de-livros": {
  "url": "http://localhost:8765/mcp",
  "description": "Um servidor de MCP para o sistema de catalogo pessoal de livros, sendo usado para inserir, consultar e atualizar recomendacoes de livros.",
  "transport": "streamable-http"
}
```

- Ajuste `url` conforme host/porta configurados em `config_mcp.json`.
- Consulte a documentacao do cliente MCP que voce esta usando para entender
  como adicionar o servidor (no Cursor, fica em `~/.cursor/mcp.json`).
- Depois de configurar, reinicie/atualize o cliente para que as tools `books_*`
  aparecam na lista.
