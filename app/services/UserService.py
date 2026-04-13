from fastapi import HTTPException
from warnings import _deprecated

from app.repositories.UserRepository import UserRepository
from app.models.User import User
from app.dtos.UserDtos import UserCreateUpdateDto

class UserService:

    def __init__(self):
        self.repo = UserRepository()

    async def find_by_id(self, user_id: int):
        return await self.repo.find_by_id(user_id)

    async def list_users(self):
        return await self.repo.find_all()

    async def create_user(self, dto: UserCreateUpdateDto):
        user = User(name=dto.name, email=dto.email)
        return await self.repo.save(user)

    async def update_user(self, user_id: int, dto: UserCreateUpdateDto):
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.name = dto.name if dto.name else user.name
        user.email = dto.email if dto.email else user.email
        user.active = dto.active if dto.active is not None else user.active
        return await self.repo.save(user)
        