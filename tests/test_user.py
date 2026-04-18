import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from fastapi import FastAPI, Request

from collections.abc import AsyncGenerator
from app.controllers.UserController import router
from app.configs.Database import Base, db_session_context

api_app = FastAPI()
api_app.include_router(router)

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession
)


@api_app.middleware("http")
async def db_session_test_middleware(request: Request, call_next):
    """Garante o isolamento do ContextVar injetando a session de teste por request."""
    async with TestingSessionLocal() as session:
        token = db_session_context.set(session)
        try:
            response = await call_next(request)
            await session.commit()
            return response
        except Exception:
            await session.rollback()
            raise
        finally:
            db_session_context.reset(token)


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Garante schema limpo antes e depois de CADA teste executado."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Fixture de cliente HTTP assíncrono para testes E2E/Integração."""
    async with AsyncClient(
        transport=ASGITransport(app=api_app), base_url="http://test-api.domain"
    ) as ac:
        yield ac


@pytest.fixture
def base_payload() -> dict:
    return {
        "name": "Jane Doe",
        "email": "jane.doe@company.com",
        "password": "SecurePassword123!",
    }


@pytest_asyncio.fixture
async def persistent_user(client: AsyncClient, base_payload: dict) -> dict:
    """Fixture que preenche o banco como setup e retorna a representação do usuário salvo."""
    response = await client.post("/users/", json=base_payload)
    return response.json()


@pytest.mark.asyncio
class TestUserIntegration:
    async def test_create_user_success(self, client: AsyncClient, base_payload: dict):
        response = await client.post("/users/", json=base_payload)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Jane Doe"
        assert data["email"] == base_payload["email"]
        assert data["active"] is True
        assert "password" not in data

    async def test_create_user_email_conflict(
        self, client: AsyncClient, base_payload: dict, persistent_user: dict
    ):
        response = await client.post("/users/", json=base_payload)

        assert response.status_code == 409

    async def test_create_user_invalid_business_rule_for_name(
        self, client: AsyncClient, base_payload: dict
    ):
        invalid_payload = {**base_payload, "name": "Jane"}
        response = await client.post("/users/", json=invalid_payload)

        assert response.status_code in [400, 422]
        assert "name" in response.text.lower()

    async def test_get_user_by_id_success(
        self, client: AsyncClient, persistent_user: dict
    ):
        user_id = persistent_user["id"]
        response = await client.get(f"/users/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == persistent_user["email"]

    async def test_get_user_not_found(self, client: AsyncClient):
        response = await client.get("/users/999999")
        assert response.status_code == 404

    async def test_list_all_users(self, client: AsyncClient, persistent_user: dict):
        response = await client.get("/users/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == persistent_user["id"]

    async def test_patch_user_partial_update(
        self, client: AsyncClient, persistent_user: dict
    ):
        user_id = persistent_user["id"]
        update_payload = {"name": "Jane Doe Updated", "active": False}

        response = await client.patch(f"/users/{user_id}", json=update_payload)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Doe Updated"
        assert data["active"] is False
        assert data["email"] == persistent_user["email"]
