from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, date
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    chat_id = Column(Integer, index=True)
    username = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    habits = relationship("Habit", back_populates="user")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    days_completed = Column(Integer, default=0)
    max_days = Column(Integer, default=21)
    last_updated = Column(Date, default=lambda: date.today())
    last_completed = Column(Date, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    completed_early = Column(Boolean, default=False)

    user = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit")


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date, default=lambda: date.today())
    completed = Column(Boolean, default=False)

    habit = relationship("Habit", back_populates="logs")
