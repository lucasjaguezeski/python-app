from fastapi import FastAPI

from app.configs.Lifespan import lifespan
from app.configs.DBSessionMiddleware import DBSessionMiddleware
from app.controllers import api_router

app = FastAPI(lifespan=lifespan)

# Adiciona o Middleware Automático
app.add_middleware(DBSessionMiddleware)

# Registra as rotas da aplicação
app.include_router(api_router)
