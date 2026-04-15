from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreateDto(BaseModel):
    name: Optional[str]
    email: EmailStr


class UserUpdateDto(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = None


class UserResponseDto(BaseModel):
    id: int
    active: bool
    name: Optional[str]
    email: EmailStr

    class Config:
        from_attributes = True
