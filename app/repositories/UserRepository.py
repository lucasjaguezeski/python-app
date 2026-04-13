from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from collections.abc import Sequence
from app.models.User import User
from app.core.Database import get_db_session


class UserRepository:
    @property
    def db(self) -> AsyncSession:
        return get_db_session()

    async def find_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def find_all(self) -> Sequence[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def save(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        """Função de exemplo, não usar em produção. Em produção, marcar como inativo é mais recomendado."""
        await self.db.delete(user)
        await self.db.commit()
