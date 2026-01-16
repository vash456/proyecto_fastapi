from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum


class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role: str = Field(default=RoleEnum.USER)
    is_active: bool = Field(default=True)
