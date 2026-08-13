"""
Модель HabitLog представляет ежедневную запись о выполнении привычки.
Хранит историю выполнения, позволяя отслеживать прогресс,
строить графики и анализировать паттерны поведения пользователя.
"""

from datetime import date

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..utils.database import Base


class HabitLog(Base):  # pylint: disable=too-few-public-methods
    """
    Определяет структуру таблицы habit_logs в базе данных
    для хранения ежедневных записей о выполнении привычек.
    """

    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date, default=date.today())
    completed = Column(Boolean, default=False)

    # Связь с моделью Habit (одна привычка → много логов).
    habit = relationship("Habit", back_populates="logs")
