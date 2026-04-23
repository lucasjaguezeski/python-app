from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from enum import Enum


class DDLAutoOption(str, Enum):
    UPDATE = "update"
    CREATE = "create"
    NONE = "none"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Configurações gerais da aplicação
    APP_ENV: str = "development"
    APP_VERSION: str = "1.0.0"
    LOG_LEVEL: str = "INFO"
    UVICORN_HOST: str = "0.0.0.0"
    UVICORN_PORT: int = 8000

    # Configurações do banco de dados PostgreSQL
    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False
    DB_POOL_PRE_PING: bool = True
    ALEMBIC_DDL_AUTO: DDLAutoOption = DDLAutoOption.NONE

    # Configurações do MongoDB
    MONGODB_URL: str
    MONGO_DB_NAME: str
    MONGO_TIMEOUT_MS: int = 5000
    ENABLE_MONGO_LOGS: bool = False


@lru_cache
def get_settings():
    return Settings()  # type: ignore[call-arg]
