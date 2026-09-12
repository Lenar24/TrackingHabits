"""
Модель HabitLog представляет ежедневный лог выполнения привычки.
"""

from typing import TYPE_CHECKING
from datetime import date, datetime, timezone
from sqlalchemy import Integer, Boolean, Date, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import BaseModel

if TYPE_CHECKING:
    from .habit import Habit


class HabitLog(BaseModel):
    """
    Ежедневный лог выполнения привычки.
    """

    __tablename__ = "habit_logs"

    # Внешние ключи
    habit_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("habits.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Данные
    date: Mapped[date] = mapped_column(
        Date,
        default=lambda: datetime.now(timezone.utc).date(),  # ✅ Python время
        nullable=False,
        index=True
    )
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Связи
    habit: Mapped["Habit"] = relationship("Habit", back_populates="logs")

    # Уникальность: одна запись на привычку в день
    __table_args__ = (
        UniqueConstraint('habit_id', 'date', name='uq_habit_log_habit_date'),
        Index('ix_habit_logs_date_completed', 'date', 'completed'),
    )

    def __repr__(self) -> str:
        return f"<HabitLog id={self.id} habit_id={self.habit_id} date={self.date} completed={self.completed}>"
