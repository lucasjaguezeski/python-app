import uvicorn
from fastapi import FastAPI

from app.configs.Lifespan import lifespan
from app.configs.DBSessionMiddleware import DBSessionMiddleware
from app.configs.Settings import get_settings
from app.controllers import api_router

app = FastAPI(lifespan=lifespan)

# Adiciona o Middleware Automático
app.add_middleware(DBSessionMiddleware)

# Registra as rotas da aplicação
app.include_router(api_router)


def run() -> None:
    settings = get_settings()
    uvicorn.run(
        "app:app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        log_level=settings.LOG_LEVEL.lower(),
        reload=settings.APP_ENV == "development",
    )


if __name__ == "__main__":
    run()
