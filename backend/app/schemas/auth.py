"""
Pydantic схемы для аутентификации.
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class LoginRequest(BaseModel):
    """
    Запрос на логин.

    Поддерживает как `user_id`, так и `max_user_id`.
    """
    user_id: int = Field(
        ...,
        description="ID пользователя из MAX",
        validation_alias="max_user_id",
        serialization_alias="user_id",
    )
    chat_id: int = Field(..., description="ID чата для отправки сообщений")
    username: Optional[str] = Field(None, max_length=100, description="Имя пользователя")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )


class TokenResponse(BaseModel):
    """Ответ с JWT токеном."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """Запрос на обновление токена."""
    refresh_token: str


class TokenData(BaseModel):
    """Данные из JWT токена."""
    sub: str
    user_id: int
    chat_id: int
    exp: int
    type: Optional[str] = "access"
