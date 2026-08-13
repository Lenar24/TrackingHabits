"""
Модель User представляет пользователя системы.
Хранит информацию о пользователе из MAX, включая идентификаторы для связи с ботом
и отправки сообщений. Связана с привычками пользователя через отношение один-ко-многим.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..utils.database import Base


class User(Base):  # pylint: disable=too-few-public-methods
    """
    Модель Пользователя.
    Определяет структуру таблицы users в базе данных для хранения информации о пользователях.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    chat_id = Column(Integer, index=True)
    username = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Связь с моделью Habit (один пользователь → много привычек).
    habits = relationship("Habit", back_populates="user")
