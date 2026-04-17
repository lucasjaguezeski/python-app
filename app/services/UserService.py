from collections.abc import Sequence
import bcrypt

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

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

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

        hashed_password = self.get_password_hash(dto.password)
        user = User(name=dto.name, email=dto.email, password=hashed_password)

        return await self.repo.save(user)

    async def update_user(self, user_id: int, dto: UserUpdateDto) -> User:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        user = patch(user, dto)
        return await self.repo.save(user)
