"""Leitura centralizada de configuracoes para o modo de estudo.

Os valores sao carregados via variaveis de ambiente ou arquivo .env para
facilitar o desenvolvimento local. Em producao, injete-os a partir de um
Key Vault/secret manager e nunca versione segredos.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Define campos usados em todo o backend."""

    database_url: str = Field(
        default="sqlite:///./data/books.db",
        description="URL de conexao usada pelo SQLAlchemy.",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Retorna uma instancia cacheada de Settings."""

    return Settings()


config = get_settings()
