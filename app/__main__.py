import uvicorn
from app.configs.Settings import AppEnvironment, get_settings


def run() -> None:
    """Entrypoint da aplicação.

    Inicia o servidor uvicorn.
    """
    settings = get_settings()
    uvicorn.run(
        "app:app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        log_level=settings.LOG_LEVEL.lower(),
        reload=settings.APP_ENV == AppEnvironment.LOCAL,
        workers=settings.UVICORN_WORKERS,
        proxy_headers=settings.PROXY_HEADERS,
        timeout_keep_alive=settings.UVICORN_TIMEOUT_KEEP_ALIVE,
    )


if __name__ == "__main__":
    run()
