from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.Database import db, db_session_context
from app.core.MongoDB import mongo_db
from app.controllers.UserController import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Conecta ambos os bancos de forma segura
    await db.connect()
    await mongo_db.connect()
    yield
    # Shutdown: Encerra os pools de conexão
    await mongo_db.disconnect()
    await db.disconnect()

app = FastAPI(lifespan=lifespan)

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Abre uma nova "conexão" para esta Request inteira
        session = db.session_factory()
        # 2. Guarda ela no "Thread Local" do ContextVar
        token = db_session_context.set(session)
        try:
            # 3. A Request roda por completo. Todos os services/repos acessam a mesma `session` aqui!
            response = await call_next(request)
            return response
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            # 4. De maneira garantida, fechamos a sessão da Request para voltar ao pool
            await session.close()
            db_session_context.reset(token)

# Adiciona o Middleware Automático
app.add_middleware(DBSessionMiddleware)

# Registra nossas rotas Controladas
app.include_router(user_router)