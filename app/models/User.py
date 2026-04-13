from sqlalchemy import Column, Integer, String, Boolean
from app.core.Database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default=True, nullable=False)
    name = Column(String(50), nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=False)