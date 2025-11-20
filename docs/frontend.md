# Frontend (React + Vite)

Para quem ja conhece React, esta pagina serve como mapa dos arquivos e do fluxo basico.

## Estrutura principal

- `frontend/src/main.tsx`  
  Ponto de entrada do Vite. Renderiza `<App />` em `#root`.

- `frontend/src/App.tsx`  
  Apenas exporta `<BooksPage />`.

- `frontend/src/pages/BooksPage.tsx`  
  Componente de pagina unico:
  - mantem estado de livros, loading, erro, termo de busca e livro ativo para edicao;
  - orquestra chamadas `listBooks`, `searchBooks`, `createBook`, `updateBook`, `deleteBook`;
  - renderiza `SearchBar`, `BookForm` e `BookTable`.

## Componentes

- `frontend/src/components/BookForm.tsx`  
  Formulario controlado usado para criar/editar. Recebe `onSubmit`, `activeBook` e `onCancel`. Normaliza valores com `trim`.

- `frontend/src/components/BookTable.tsx`  
  Componente de apresentacao que lista os livros e expoe botoes de editar/excluir via callbacks.

- `frontend/src/components/SearchBar.tsx`  
  Campo de texto + botao que invocam `onSearch` fornecido pela pagina.

## Camada de API

- `frontend/src/api/client.ts`  
  Instancia Axios com `baseURL = import.meta.env.VITE_API_URL` (padrao `http://localhost:8000/api`). Nao coloque segredos aqui; em apps reais a autenticacao ocorre no backend/gateway.

- `frontend/src/api/books.ts`  
  Funcoes tipadas (`listBooks`, `searchBooks`, `createBook` etc.) que mapeiam diretamente para as rotas FastAPI.

## Tipos

- `frontend/src/types/book.ts`  
  `Book` (equivalente ao `BookOut` do backend) e `BookPayload` (equivalente ao `BookCreate`). Mantem o frontend alinhado aos schemas da API.

## Fluxo resumido

1. `BooksPage` monta e chama `listBooks()` → Axios atinge `/api/books`.
2. A resposta atualiza o estado local → `BookTable` renderiza.
3. Formularios chamam `createBook/updateBook` → backend persiste → `fetchBooks` recarrega a lista.
4. MCP Server nao interfere no frontend; ambos consomem a mesma API interna de servicos.

## Consideracoes

- Nenhum fluxo de autenticacao foi implementado; a API esta aberta apenas para simplificar o estudo.
- Para levar este frontend a producao, inclua uma camada de autenticacao (login, tokens, interceptors), validacoes adicionais e UX mais robusta (paginacao visual, feedbacks).
