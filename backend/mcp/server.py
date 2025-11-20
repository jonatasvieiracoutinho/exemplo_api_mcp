"""Servidor MCP que espelha as operacoes do catalogo de livros.

O arquivo le `config_mcp.json`, registra as tools habilitadas e inicia o
FastMCP usando transporte streamable-http. Tudo e pensado para uso local,
por isso nao ha TLS nem autenticacao; ajuste antes de expor em ambiente real.
"""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

from fastmcp import FastMCP

from backend.database.connection import init_db
from backend.mcp.mcp_tools import MCPBookTools

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).with_name("config_mcp.json")
with CONFIG_PATH.open("r", encoding="utf-8") as fp:
    CONFIG = json.load(fp)


def is_tool_enabled(name: str) -> bool:
    """Verifica no JSON se a tool esta habilitada."""

    for endpoint in CONFIG.get("endpoints", []):
        if endpoint["name"] == name:
            return endpoint.get("enabled", False)
    return False


def get_tool_description(name: str) -> str:
    """Texto auxiliar exibido para o cliente MCP."""

    for endpoint in CONFIG.get("endpoints", []):
        if endpoint["name"] == name:
            return endpoint.get("description", "")
    return ""


def register_tools(server: FastMCP, tools: MCPBookTools) -> None:
    """Liga declaracoes do JSON aos metodos de MCPBookTools."""

    if is_tool_enabled("books_add"):
        @server.tool(name="books_add", description=get_tool_description("books_add"))
        def tool_books_add(
            title: str,
            author: str | None = None,
            publisher: str | None = None,
            purchase_link: str | None = None,
        ):
            return tools.books_add(title, author, publisher, purchase_link)

    if is_tool_enabled("books_update"):
        @server.tool(name="books_update", description=get_tool_description("books_update"))
        def tool_books_update(
            book_id: int,
            title: str | None = None,
            author: str | None = None,
            publisher: str | None = None,
            purchase_link: str | None = None,
        ):
            return tools.books_update(book_id, title, author, publisher, purchase_link)

    if is_tool_enabled("books_delete"):
        @server.tool(name="books_delete", description=get_tool_description("books_delete"))
        def tool_books_delete(book_id: int):
            return tools.books_delete(book_id)

    if is_tool_enabled("books_get"):
        @server.tool(name="books_get", description=get_tool_description("books_get"))
        def tool_books_get(book_id: int):
            return tools.books_get(book_id)

    if is_tool_enabled("books_list"):
        @server.tool(name="books_list", description=get_tool_description("books_list"))
        def tool_books_list(limit: int = 100, offset: int = 0):
            return tools.books_list(limit, offset)

    if is_tool_enabled("books_search"):
        @server.tool(name="books_search", description=get_tool_description("books_search"))
        def tool_books_search(query: str, limit: int = 100, offset: int = 0):
            return tools.books_search(query, limit, offset)


def main() -> None:
    """Entry point chamado por `python run_mcp_server.py`."""

    server_info = CONFIG["server"]
    logger.info("Iniciando MCP Server %s v%s", server_info["name"], server_info["version"])
    init_db()
    logger.info("Banco inicializado")

    server = FastMCP(server_info["name"], version=server_info["version"])
    tools = MCPBookTools()
    register_tools(server, tools)

    enabled = [endpoint["name"] for endpoint in CONFIG["endpoints"] if endpoint.get("enabled", False)]
    logger.info("Tools habilitadas: %s", ", ".join(enabled) or "nenhuma")

    try:
        server.run(transport="streamable-http", host=server_info["host"], port=server_info["port"])
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("MCP Server interrompido pelo usuario. Encerrando com seguranca.")


if __name__ == "__main__":
    main()
