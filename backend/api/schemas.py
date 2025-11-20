from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class BookBase(BaseModel):
    title: str = Field(..., description="Título do livro.", example="O Senhor dos Anéis")
    author: Optional[str] = Field(default=None, description="Autor principal.", example="J. R. R. Tolkien")
    publisher: Optional[str] = Field(default=None, description="Editora responsável.", example="Martins Fontes")
    purchase_link: Optional[HttpUrl] = Field(
        default=None,
        description="URL para compra ou referência.",
        example="https://www.ecolivros.com/produto/o-senhor-dos-aneis",
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Title is required")
        return value.strip()


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, description="Novo título.", example="O Hobbit")
    author: Optional[str] = Field(default=None, description="Novo autor.", example="J. R. R. Tolkien")
    publisher: Optional[str] = Field(default=None, description="Nova editora.", example="HarperCollins")
    purchase_link: Optional[HttpUrl] = Field(
        default=None,
        description="Novo link de compra.",
        example="https://www.lojaexemplo.com/livros/o-hobbit",
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("Title must not be empty")
        return value.strip() if value else value


class BookOut(BookBase):
    id: int = Field(..., description="Identificador único do livro.", example=1)
    created_at: datetime = Field(..., description="Data/hora de criação.", example="2024-11-18T10:00:00")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "O Senhor dos Anéis",
                "author": "J. R. R. Tolkien",
                "publisher": "Martins Fontes",
                "purchase_link": None,
                "created_at": "2024-11-18T10:00:00",
            }
        },
    )
