from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..utils.database import Base


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
