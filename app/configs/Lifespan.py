from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.configs.Database import db
from app.configs.MongoDB import mongo_db
from app.configs.DDLManager import apply_ddl


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Conecta os bancos
    await db.connect()
    await mongo_db.connect()

    # Roda automação DDL após o db.engine estar pronto
    await apply_ddl(db.engine)

    yield

    # Shutdown: Encerra conexões
    await mongo_db.disconnect()
    await db.disconnect()
