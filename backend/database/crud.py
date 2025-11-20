"""Funcoes CRUD basicas usadas pelo book_service."""

from __future__ import annotations

from typing import Sequence

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from backend.database.models import Book


def create_book(
    db: Session,
    *,
    title: str,
    author: str | None = None,
    publisher: str | None = None,
    purchase_link: str | None = None,
) -> Book:
    """Insere um novo livro e devolve o modelo sincronizado."""

    book = Book(title=title.strip(), author=author, publisher=publisher, purchase_link=purchase_link)
    db.add(book)
    db.flush()
    db.refresh(book)
    return book


def list_books(db: Session, *, limit: int = 100, offset: int = 0) -> Sequence[Book]:
    """Retorna livros ordenados por created_at desc."""

    stmt = select(Book).order_by(Book.created_at.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()


def get_book(db: Session, book_id: int) -> Book | None:
    """Busca pelo ID ou retorna None."""

    return db.get(Book, book_id)


def update_book(
    db: Session,
    book: Book,
    *,
    title: str | None = None,
    author: str | None = None,
    publisher: str | None = None,
    purchase_link: str | None = None,
) -> Book:
    """Atualiza campos presentes e retorna o modelo sincronizado."""

    if title is not None:
        book.title = title.strip()
    if author is not None:
        book.author = author
    if publisher is not None:
        book.publisher = publisher
    if purchase_link is not None:
        book.purchase_link = purchase_link
    db.add(book)
    db.flush()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book) -> None:
    """Remove o registro associado."""

    db.delete(book)


def search_books(db: Session, *, query: str, limit: int = 100, offset: int = 0) -> Sequence[Book]:
    """Busca case-insensitive em titulo, autor e editora."""

    pattern = f"%{query.lower()}%"
    stmt = (
        select(Book)
        .where(
            or_(
                Book.title.ilike(pattern),
                Book.author.ilike(pattern),
                Book.publisher.ilike(pattern),
            )
        )
        .order_by(Book.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return db.execute(stmt).scalars().all()
