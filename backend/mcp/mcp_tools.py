"""Metodos que implementam as tools MCP do catalogo de livros."""

from __future__ import annotations

from typing import Any, Dict, List

from backend.database.connection import get_db
from backend.services import book_service


class MCPBookTools:
    """Adaptador entre FastMCP e o book_service.

    Cada metodo trabalha apenas com tipos primitivos (str, int, dict) para
    facilitar a serializacao e o consumo pelos agentes MCP.
    """

    def _to_dict(self, obj: Any) -> Dict[str, Any]:
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        data = obj.__dict__.copy()
        data.pop("_sa_instance_state", None)
        return data

    def books_add(
        self,
        title: str,
        author: str | None = None,
        publisher: str | None = None,
        purchase_link: str | None = None,
    ) -> Dict[str, Any]:
        """Cria um novo livro usando o service compartilhado."""

        if not title or not title.strip():
            raise ValueError("Title is required")
        with get_db() as db:
            book = book_service.create_book(
                db,
                title=title,
                author=author,
                publisher=publisher,
                purchase_link=purchase_link,
            )
            return self._to_dict(book)

    def books_update(
        self,
        book_id: int,
        title: str | None = None,
        author: str | None = None,
        publisher: str | None = None,
        purchase_link: str | None = None,
    ) -> Dict[str, Any]:
        """Atualiza campos de um livro existente."""

        with get_db() as db:
            book = book_service.update_book(
                db,
                book_id,
                title=title,
                author=author,
                publisher=publisher,
                purchase_link=purchase_link,
            )
            return self._to_dict(book)

    def books_delete(self, book_id: int) -> Dict[str, Any]:
        """Remove um livro e confirma o ID deletado."""

        with get_db() as db:
            book_service.delete_book(db, book_id)
        return {"deleted": True, "id": book_id}

    def books_get(self, book_id: int) -> Dict[str, Any]:
        """Retorna um livro unico."""

        with get_db() as db:
            book = book_service.get_book(db, book_id)
            return self._to_dict(book)

    def books_list(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista livros paginados (mais recentes primeiro)."""

        with get_db() as db:
            books = book_service.list_books(db, limit=limit, offset=offset)
            return [self._to_dict(book) for book in books]

    def books_search(self, query: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Busca livros por palavra-chave."""

        if not query or not query.strip():
            raise ValueError("Query must contain at least one character")
        with get_db() as db:
            books = book_service.search_books(db, query=query, limit=limit, offset=offset)
            return [self._to_dict(book) for book in books]
