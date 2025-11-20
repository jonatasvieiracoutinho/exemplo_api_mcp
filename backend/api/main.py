"""Inicializa o aplicativo FastAPI e registra as rotas REST.

Tudo aqui permanece propositalmente simples para favorecer o estudo. Quando
for expor publicamente, inclua middlewares de autenticacao, limite CORS e
coloque a API atras de um gateway com TLS.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.api_config import api_config
from backend.api.endpoints import router as books_router
from backend.database.connection import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Catalogo de Livros",
    description="API para catalogar livros",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # apenas para ambiente local/didatico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router, prefix="/api")


@app.on_event("startup")
async def startup_event() -> None:
    """Garante que o banco esteja pronto antes da primeira requisicao."""

    logger.info("Inicializando banco de dados...")
    init_db()
    logger.info("Banco pronto")


@app.get("/")
async def root() -> dict[str, str]:
    """Endpoint de saude simples apontando para o Swagger."""

    return {"message": "Catalogo de Livros", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.api.main:app", host=api_config.host, port=api_config.port, reload=True)
