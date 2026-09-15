"""
Модель User представляет пользователя системы.
"""

from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .habit import Habit


class User(BaseModel):
    """
    Модель пользователя системы.
    """

    __tablename__ = "users"

    # Внешний ID из MAX
    max_user_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)

    # ID чата для отправки сообщений
    chat_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

    # Имя пользователя (опционально)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Администратор
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Активен ли пользователь
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Связи
    habits: Mapped[List["Habit"]] = relationship(
        "Habit", back_populates="user", cascade="all, delete-orphan", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} max_user_id={self.max_user_id} username={self.username}>"
