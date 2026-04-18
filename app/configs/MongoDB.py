from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.configs.Settings import get_settings


class MongoManager:
    def __init__(self):
        self.client = None

    async def connect(self) -> None:
        settings = get_settings()

        if not settings.ENABLE_MONGO_LOGS:
            return

        try:
            self.client = AsyncIOMotorClient(
                settings.MONGODB_URL, serverSelectionTimeoutMS=settings.MONGO_TIMEOUT_MS
            )

            await self.client.server_info()

            from app.models.LogDocument import LogDocument

            await init_beanie(
                database=self.client[settings.MONGO_DB_NAME],  # type: ignore[arg-type]
                document_models=[LogDocument],
            )
        except Exception:
            raise

    async def disconnect(self) -> None:
        if self.client:
            self.client.close()


mongo_db = MongoManager()
