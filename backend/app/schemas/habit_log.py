"""
Модуль содержит Pydantic схемы для валидации, сериализации и десериализации
данных логов выполнения привычек.
Используется для работы с ежедневными записями о выполнении привычек.
"""

from datetime import date

from pydantic import BaseModel


class HabitLogBase(BaseModel):
    """Базовая схема, содержащая основные поля лога привычки."""

    habit_id: int
    date: date
    completed: bool


class HabitLog(HabitLogBase):
    """
    Полная схема лога для ответов API.
    Наследует базовые поля и добавляет уникальный идентификатор.
    """

    id: int

    class Config:  # pylint: disable=too-few-public-methods
        """Позволяет преобразовывать SQLAlchemy модели в Pydantic схемы автоматически."""

        from_attributes = True
