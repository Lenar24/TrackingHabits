"""
Базовый класс для всех моделей с общими полями и методами.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """
    Абстрактный базовый класс для всех моделей.
    Содержит общие поля и методы.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def to_dict(self) -> dict:
        """Преобразование модели в словарь."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"
