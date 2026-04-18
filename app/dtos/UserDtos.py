from pydantic import BaseModel, EmailStr, field_validator, ConfigDict, Field
from typing import Annotated

from app.exceptions.UserExceptions import (
    UserNameInvalidException,
    PasswordTooLongException,
)


class UserCreateDto(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=30, examples=["John Doe"])]
    email: Annotated[EmailStr, Field(examples=["user@example.com"])]
    password: Annotated[
        str, Field(min_length=6, max_length=72, examples=["S3cur3P@ssw0rd"])
    ]

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
    name: Annotated[
        str | None,
        Field(min_length=2, max_length=30, examples=["John Doe"], default=None),
    ]
    email: Annotated[
        EmailStr | None, Field(examples=["user@example.com"], default=None)
    ]
    active: Annotated[bool | None, Field(examples=[True], default=None)]

    @field_validator("name")
    @classmethod
    def name_must_contain_space_if_provided(cls, v):
        if v is not None and " " not in v:
            raise UserNameInvalidException(v)
        return v.title() if v else v


class UserResponseDto(BaseModel):
    id: Annotated[int, Field(examples=[1])]
    active: Annotated[bool, Field(examples=[True])]
    name: Annotated[str | None, Field(examples=["John Doe"], default=None)]
    email: Annotated[EmailStr, Field(examples=["user@example.com"])]

    model_config = ConfigDict(from_attributes=True)
