from sqlalchemy import text
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    # Время устанавливается на стороне БД
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))

    habits = relationship("Habit", back_populates="user")


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    # Время устанавливается на стороне БД
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    is_active = Column(Boolean, default=True)
    days_completed = Column(Integer, default=0)

    user = relationship("User", back_populates="habits")
