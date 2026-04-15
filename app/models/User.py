from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.configs.Database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(50), default=None, nullable=True)
