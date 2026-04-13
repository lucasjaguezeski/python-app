from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_ENV: str = "development"
    
    DB_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False
    DB_POOL_PRE_PING: bool = True
    DDL_AUTO_CREATE: bool = False
    
    MONGODB_URL: str
    MONGO_DB_NAME: str
    MONGO_TIMEOUT_MS: int = 5000
    ENABLE_MONGO_LOGS: bool = True

@lru_cache
def get_settings():
    return Settings()