import logging
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.Settings import get_settings

logger = logging.getLogger(__name__)
Base = declarative_base()

db_session_context: ContextVar[AsyncSession] = ContextVar("db_session")


def get_db_session() -> AsyncSession:
    """Busca a sessão injetada pelo middleware no contexto atual."""
    try:
        return db_session_context.get()
    except LookupError:
        raise Exception(
            "Não há uma sessão conectada para a operação (O contexto perdeu a session)."
        )


class DatabaseManager:
    def __init__(self):
        self.engine = None
        self._session_factory = None

    async def connect(self) -> None:
        settings = get_settings()

        try:
            self.engine = create_async_engine(
                settings.DB_URL,
                pool_pre_ping=settings.DB_POOL_PRE_PING,
                pool_size=settings.DB_POOL_SIZE,
                max_overflow=settings.DB_MAX_OVERFLOW,
                echo=settings.DB_ECHO,
            )
            # Fator de sessões assíncronas
            self._session_factory = async_sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )

            # Recurso de DDL Auto
            if settings.DDL_AUTO_CREATE:
                async with self.engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)

        except Exception as e:
            logger.error(f"Falha ao conectar no banco de dados: {e}")
            raise

    async def disconnect(self) -> None:
        if self.engine:
            await self.engine.dispose()
            logger.info("Conexões do banco de dados encerradas.")

    def session_factory(self) -> AsyncSession:
        if self._session_factory is None:
            raise Exception("O banco de dados não foi inicializado.")
        return self._session_factory()


db = DatabaseManager()
