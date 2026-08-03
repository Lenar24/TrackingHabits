"""
Модуль содержит Pydantic схемы для валидации, сериализации и десериализации
данных пользователей. Используется для регистрации пользователей,
получения информации о них и управления их данными.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .habit import Habit


class UserBase(BaseModel):
    """Базовая схема, содержащая основные поля пользователя из MAX."""

    user_id: int
    username: Optional[str] = None


class UserCreate(UserBase):
    """Схема для создания нового пользователя. Наследует поля от UserBase и добавляет chat_id."""

    chat_id: Optional[int] = None


class User(UserBase):
    """
    Полная схема пользователя для ответов API.
    Наследует базовые поля и добавляет все системные поля и связи.
    """

    id: int
    created_at: datetime
    chat_id: Optional[int] = None
    habits: List[Habit] = []

    class Config:  # pylint: disable=too-few-public-methods
        """
        Позволяет преобразовывать SQLAlchemy модели в Pydantic
        схемы автоматически, включая вложенные отношения.
        """

        from_attributes = True
