"""Modelos ORM usados pelo SQLAlchemy."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Index, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Book(Base):
    """Tabela principal do catalogo."""

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=True, index=True)
    publisher = Column(String(255), nullable=True, index=True)
    purchase_link = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_books_title", "title"),
        Index("idx_books_author", "author"),
        Index("idx_books_publisher", "publisher"),
    )

    def to_dict(self) -> dict[str, str | int | None]:
        """Facilita transformar o modelo em JSON (usado pelo MCP)."""

        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "purchase_link": self.purchase_link,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
