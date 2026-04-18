from fastapi_utils.cbv import cbv
from fastapi import APIRouter, HTTPException, status, Depends

from collections.abc import Sequence

from app.dtos.UserDtos import UserCreateDto, UserUpdateDto, UserResponseDto
from app.services.UserService import UserService
from app.models.User import User

router = APIRouter(prefix="/users", tags=["Users"])


@cbv(router)
class UserController:
    service: UserService = Depends()

    @router.get("/{user_id}", response_model=UserResponseDto)
    async def get_user(self, user_id: int) -> User:
        return await self.service.find_by_id(user_id)

    @router.get("/", response_model=list[UserResponseDto])
    async def list_users(self) -> Sequence[User]:
        return await self.service.list_users()

    @router.post(
        "/", response_model=UserResponseDto, status_code=status.HTTP_201_CREATED
    )
    async def create_user(self, dto: UserCreateDto) -> User:
        try:
            return await self.service.create_user(dto)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/{user_id}", response_model=UserResponseDto)
    async def update_user(self, user_id: int, dto: UserUpdateDto) -> User:
        try:
            return await self.service.update_user(user_id, dto)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
