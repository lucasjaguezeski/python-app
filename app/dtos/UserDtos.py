from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

from app.exceptions.UserExceptions import (
    UserNameInvalidException,
    PasswordTooLongException,
)


class UserCreateDto(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise PasswordTooLongException()
        return v

    @field_validator("name")
    @classmethod
    def name_must_contain_space(cls, v):
        if " " not in v:
            raise UserNameInvalidException(v)
        return v.title()


class UserUpdateDto(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def name_must_contain_space_if_provided(cls, v):
        if v is not None and " " not in v:
            raise UserNameInvalidException(v)
        return v.title() if v else v


class UserResponseDto(BaseModel):
    id: int
    active: bool
    name: Optional[str]
    email: EmailStr

    class Config:
        from_attributes = True
