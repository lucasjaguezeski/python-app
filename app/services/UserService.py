from fastapi import HTTPException
from collections.abc import Sequence

from app.repositories.UserRepository import UserRepository
from app.models.User import User
from app.dtos.UserDtos import UserCreateUpdateDto
from app.utils.DtoUtil import patch


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    async def find_by_id(self, user_id: int) -> User | None:
        return await self.repo.find_by_id(user_id)

    async def list_users(self) -> Sequence[User]:
        return await self.repo.find_all()

    async def create_user(self, dto: UserCreateUpdateDto) -> User:
        user = User(name=dto.name, email=dto.email)
        return await self.repo.save(user)

    async def update_user(self, user_id: int, dto: UserCreateUpdateDto) -> User:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user = patch(user, dto)
        return await self.repo.save(user)
