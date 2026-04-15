from fastapi import APIRouter
from app.controllers.UserController import router as user_router

api_router = APIRouter()

# Aqui registramos os novo routers, conforme formos criando novos controllers
api_router.include_router(user_router)
