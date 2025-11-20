from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from backend.api import schemas
from backend.database.connection import get_db_dependency
from backend.services import book_service

router = APIRouter(prefix="/books", tags=["books"])


@router.get(
    "/",
    response_model=list[schemas.BookOut],
    summary="Listar livros",
    description=(
        "Retorna os livros cadastrados ordenados por data de criação (mais recentes primeiro). "
        "Use os parâmetros `limit` e `offset` para paginação simples."
    ),
    responses={
        200: {
            "description": "Lista paginada de livros",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "title": "O Senhor dos Anéis",
                            "author": "J. R. R. Tolkien",
                            "publisher": "Martins Fontes",
                            "purchase_link": None,
                            "created_at": "2024-11-18T10:00:00",
                        }
                    ]
                }
            },
        }
    },
)
def list_books(
    limit: int = Query(100, ge=1, le=500, description="Quantidade de registros a retornar."),
    offset: int = Query(0, ge=0, description="Deslocamento inicial para paginação."),
    db: Session = Depends(get_db_dependency),
):
    """Lista livros com paginação e ordenação por data de criação.

    Args:
        limit: Limite máximo de itens (1-500).
        offset: Deslocamento inicial para navegar entre páginas.
        db: Sessão de banco injetada pelo FastAPI.

    Returns:
        Lista de livros no formato `BookOut`.
    """
    return book_service.list_books(db, limit=limit, offset=offset)


@router.post(
    "/",
    response_model=schemas.BookOut,
    status_code=status.HTTP_201_CREATED,
    summary="Criar livro",
    description="Adiciona um novo livro ao catálogo. Apenas o título é obrigatório.",
    responses={
        201: {"description": "Livro criado com sucesso"},
        422: {"description": "Dados inválidos"},
    },
)
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db_dependency)):
    """Cria um novo livro.

    Args:
        payload: Dados validados pelo `BookCreate`.
        db: Sessão de banco.

    Returns:
        Livro persistido.
    """
    return book_service.create_book(db, title=payload.title, author=payload.author,
                                     publisher=payload.publisher, purchase_link=payload.purchase_link)


@router.get(
    "/search",
    response_model=list[schemas.BookOut],
    summary="Buscar livros por palavra-chave",
    description="Pesquisa case-insensitive em título, autor e editora.",
    responses={
        200: {"description": "Livros encontrados"},
        422: {"description": "Parâmetros inválidos"},
    },
)
def search_books(
    query: str = Query(..., min_length=1, description="Palavra-chave para busca."),
    limit: int = Query(100, ge=1, le=500, description="Quantidade máxima de itens."),
    offset: int = Query(0, ge=0, description="Deslocamento inicial para paginação."),
    db: Session = Depends(get_db_dependency),
):
    """Busca por palavra-chave em título, autor e editora."""
    return book_service.search_books(db, query=query, limit=limit, offset=offset)


@router.get(
    "/{book_id}",
    response_model=schemas.BookOut,
    summary="Obter detalhes de um livro",
    responses={
        200: {"description": "Livro encontrado"},
        404: {"description": "Livro não encontrado"},
    },
)
def get_book(
    book_id: int = Path(..., ge=1, description="ID do livro a ser consultado."),
    db: Session = Depends(get_db_dependency),
):
    """Obtém os detalhes de um livro específico."""
    try:
        return book_service.get_book(db, book_id)
    except book_service.BookNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put(
    "/{book_id}",
    response_model=schemas.BookOut,
    summary="Atualizar livro (replace)",
    description="Substitui todas as informações do livro pelo payload enviado.",
    responses={
        200: {"description": "Livro atualizado"},
        404: {"description": "Livro não encontrado"},
    },
)
def update_book(
    book_id: int = Path(..., ge=1, description="ID do livro a ser atualizado."),
    payload: schemas.BookCreate = ...,
    db: Session = Depends(get_db_dependency),
):
    """Atualiza todas as informações de um livro."""
    try:
        return book_service.update_book(db, book_id, title=payload.title, author=payload.author,
                                         publisher=payload.publisher, purchase_link=payload.purchase_link)
    except book_service.BookNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch(
    "/{book_id}",
    response_model=schemas.BookOut,
    summary="Atualizar parcialmente um livro",
    responses={
        200: {"description": "Livro atualizado"},
        404: {"description": "Livro não encontrado"},
    },
)
def patch_book(
    book_id: int = Path(..., ge=1, description="ID do livro a ser atualizado."),
    payload: schemas.BookUpdate = ...,
    db: Session = Depends(get_db_dependency),
):
    """Atualiza parcialmente campos de um livro."""
    try:
        return book_service.update_book(db, book_id, title=payload.title, author=payload.author,
                                         publisher=payload.publisher, purchase_link=payload.purchase_link)
    except book_service.BookNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir livro",
    description="Remove definitivamente um livro do catálogo.",
    responses={
        204: {"description": "Livro removido"},
        404: {"description": "Livro não encontrado"},
    },
)
def delete_book(
    book_id: int = Path(..., ge=1, description="ID do livro a ser removido."),
    db: Session = Depends(get_db_dependency),
):
    """Remove um livro definitivamente."""
    try:
        book_service.delete_book(db, book_id)
    except book_service.BookNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return None
