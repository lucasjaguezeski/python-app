from fastapi import APIRouter, HTTPException, status
from typing import List, Sequence

from app.dtos.UserDtos import UserCreateUpdateDto, UserResponseDto
from app.services.UserService import UserService
from app.models.User import User

# Criação do roteador para este controller
router = APIRouter(prefix="/users", tags=["Users"])

# Service sendo instanciado globalmente
user_service = UserService()


@router.get("/{user_id}", response_model=UserResponseDto)
async def get_user(user_id: int) -> User:
    user = await user_service.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[UserResponseDto])
async def list_users() -> Sequence[User]:
    return await user_service.list_users()


@router.post("/", response_model=UserResponseDto, status_code=status.HTTP_201_CREATED)
async def create_user(dto: UserCreateUpdateDto) -> User:
    try:
        return await user_service.create_user(dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{user_id}", response_model=UserResponseDto)
async def update_user(user_id: int, dto: UserCreateUpdateDto) -> User:
    try:
        return await user_service.update_user(user_id, dto)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
