from collections.abc import Sequence

from app.repositories.UserRepository import UserRepository
from app.models.User import User
from app.dtos.UserDtos import UserCreateDto, UserUpdateDto
from app.utils.DtoUtil import patch
from app.exceptions.UserExceptions import (
    UserNotFoundException,
    UserEmailConflictException,
)


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    async def find_by_id(self, user_id: int) -> User:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return user

    async def list_users(self) -> Sequence[User]:
        return await self.repo.find_all()

    async def create_user(self, dto: UserCreateDto) -> User:
        existing_user = await self.repo.find_by_email(dto.email)
        if existing_user:
            raise UserEmailConflictException(dto.email)
        user = User(name=dto.name, email=dto.email)
        return await self.repo.save(user)

    async def update_user(self, user_id: int, dto: UserUpdateDto) -> User:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        user = patch(user, dto)
        return await self.repo.save(user)
