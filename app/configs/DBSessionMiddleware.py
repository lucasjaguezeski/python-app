from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.configs.Database import db, db_session_context


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
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
