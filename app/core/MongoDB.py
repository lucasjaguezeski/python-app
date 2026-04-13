import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.Settings import get_settings

logger = logging.getLogger(__name__)


class MongoManager:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None

    async def connect(self) -> None:
        settings = get_settings()

        if not settings.ENABLE_MONGO_LOGS:
            logger.info("Logs no MongoDB desativados. Ignorando inicialização.")
            return

        try:
            self.client = AsyncIOMotorClient(
                settings.MONGODB_URL, serverSelectionTimeoutMS=settings.MONGO_TIMEOUT_MS
            )

            # Testa a conexão com o MongoDB (Motor é lazy, só conecta quando exigido)
            await self.client.server_info()

            # Importar os modelos de log localmente ou passá-los para evitar import circular complexo
            from app.models.LogDocument import LogDocument

            await init_beanie(
                database=self.client[settings.MONGO_DB_NAME],  # type: ignore[arg-type]
                document_models=[LogDocument],
            )
            logger.info("MongoDB conectado e Beanie inicializado.")
        except Exception as e:
            logger.error(f"Falha ao conectar no MongoDB: {e}")
            raise

    async def disconnect(self) -> None:
        if self.client:
            self.client.close()
            logger.info("Conexão MongoDB encerrada.")


mongo_db = MongoManager()
