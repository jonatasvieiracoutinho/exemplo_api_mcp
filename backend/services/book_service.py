"""Camada de regras de negocio compartilhada por REST e MCP.

Todas as validacoes e limites de negocio vivem aqui para evitar duplicacao
entre FastAPI e o MCP Server. Sempre que a API ganhar um novo comportamento,
o ideal e implementa-lo neste modulo.
"""

from __future__ import annotations

from typing import Sequence

from sqlalchemy.orm import Session

from backend.database import crud
from backend.database.models import Book


class BookNotFoundError(Exception):
    """Indica que um ID solicitado nao existe no banco."""


def _validate_title(title: str | None) -> str | None:
    """Garante que o titulo nao esteja vazio depois do strip."""

    if title is None:
        return None
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("Title must not be empty")
    return cleaned


def create_book(
    db: Session,
    *,
    title: str,
    author: str | None = None,
    publisher: str | None = None,
    purchase_link: str | None = None,
) -> Book:
    """Cria um livro aplicando as validacoes de titulo."""

    cleaned_title = _validate_title(title)
    return crud.create_book(
        db,
        title=cleaned_title,
        author=author,
        publisher=publisher,
        purchase_link=purchase_link,
    )


def list_books(db: Session, *, limit: int = 100, offset: int = 0) -> Sequence[Book]:
    """Retorna livros ordenados por data de criacao."""

    safe_limit = min(max(limit, 1), 500)
    safe_offset = max(offset, 0)
    return crud.list_books(db, limit=safe_limit, offset=safe_offset)


def get_book(db: Session, book_id: int) -> Book:
    """Busca um livro ou dispara BookNotFoundError."""

    book = crud.get_book(db, book_id)
    if not book:
        raise BookNotFoundError(f"Book {book_id} not found")
    return book


def update_book(
    db: Session,
    book_id: int,
    *,
    title: str | None = None,
    author: str | None = None,
    publisher: str | None = None,
    purchase_link: str | None = None,
) -> Book:
    """Atualiza total ou parcialmente um livro."""

    book = get_book(db, book_id)
    cleaned_title = _validate_title(title) if title is not None else None
    return crud.update_book(
        db,
        book,
        title=cleaned_title,
        author=author,
        publisher=publisher,
        purchase_link=purchase_link,
    )


def delete_book(db: Session, book_id: int) -> None:
    """Remove um livro definitivamente."""

    book = get_book(db, book_id)
    crud.delete_book(db, book)


def search_books(db: Session, *, query: str, limit: int = 100, offset: int = 0) -> Sequence[Book]:
    """Executa busca case-insensitive em titulo, autor e editora."""

    if len(query.strip()) < 1:
        raise ValueError("Query must contain at least one character")
    safe_limit = min(max(limit, 1), 500)
    safe_offset = max(offset, 0)
    return crud.search_books(db, query=query.strip(), limit=safe_limit, offset=safe_offset)
