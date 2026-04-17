from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )


class UserEmailConflictException(HTTPException):
    def __init__(self, email: str):
        self.email = email
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The email '{email}' is already in use by another user.",
        )


class UserNameInvalidException(HTTPException):
    def __init__(self, name: str):
        self.name = name
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The name '{name}' is invalid. It must contain at least a space.",
        )


class PasswordTooLongException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too long, try a shorter one.",
        )
