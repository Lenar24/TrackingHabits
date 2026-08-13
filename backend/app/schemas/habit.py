"""
Модуль содержит Pydantic схемы для валидации, сериализации и десериализации
данных привычек. Используется для проверки входных данных API-запросов и форматирования ответов.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class HabitBase(BaseModel):
    """Базовая схема, содержащая общие поля для всех операций с привычками."""

    name: str
    description: Optional[str] = None


class HabitCreate(HabitBase):
    """Схема для создания новой привычки. Наследует все поля от HabitBase и добавляет user_id."""

    user_id: int


class HabitUpdate(BaseModel):
    """
    Схема для частичного обновления привычки.
    Все поля опциональны, что позволяет обновлять только необходимые поля.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class Habit(HabitBase):
    """
    Полная схема привычки для ответов API.
    Наследует базовые поля и добавляет все системные поля.
    """

    id: int
    user_id: int
    created_at: datetime
    is_active: bool
    days_completed: int
    max_days: int
    last_updated: date
    last_completed: Optional[date] = None
    completed_at: Optional[datetime] = None
    completed_early: bool = False

    class Config:  # pylint: disable=too-few-public-methods
        """Позволяет преобразовывать SQLAlchemy модели в Pydantic схемы автоматически."""

        from_attributes = True
