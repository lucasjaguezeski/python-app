from contextvars import ContextVar
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from app.configs.Settings import get_settings


# Contexto para armazenar a sessão do banco de dados, permitindo acesso em diferentes partes da aplicação
db_session_context: ContextVar[AsyncSession] = ContextVar("db_session")


class Base(MappedAsDataclass, DeclarativeBase):
    pass


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

        except Exception as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    async def disconnect(self) -> None:
        if self.engine:
            await self.engine.dispose()

    def session_factory(self) -> AsyncSession:
        if self._session_factory is None:
            raise Exception("O banco de dados não foi inicializado.")
        return self._session_factory()


# Instância global do gerenciador de banco de dados
db = DatabaseManager()


# Função para obter a sessão atual do banco de dados, injetada pelo middleware
def get_db_session() -> AsyncSession:
    """Busca a sessão injetada pelo middleware no contexto atual."""
    try:
        return db_session_context.get()
    except LookupError:
        raise Exception(
            "Não há uma sessão conectada para a operação (O contexto perdeu a session)."
        )
