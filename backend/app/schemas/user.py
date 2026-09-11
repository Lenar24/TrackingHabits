"""
Pydantic схемы для пользователей.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_validator

from .habit import HabitResponse


class UserBase(BaseModel):
    """Базовая схема пользователя."""
    max_user_id: int = Field(..., description="ID пользователя из MAX")
    username: Optional[str] = Field(None, max_length=100)
    chat_id: int = Field(..., description="ID чата для отправки сообщений")


class UserCreate(UserBase):
    """Схема для создания пользователя."""
    pass


class UserUpdate(BaseModel):
    """Схема для обновления пользователя."""
    username: Optional[str] = Field(None, max_length=100)
    chat_id: Optional[int] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None

    @field_validator('username')
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Имя пользователя не может быть пустым')
            return v.strip()
        return v


class UserResponse(BaseModel):
    """Базовая информация о пользователе (без привычек)."""
    id: int
    max_user_id: int
    username: Optional[str]
    chat_id: int
    is_admin: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserWithHabits(UserResponse):
    """Пользователь с привычками."""
    habits: List[HabitResponse] = []

    model_config = ConfigDict(from_attributes=True)
