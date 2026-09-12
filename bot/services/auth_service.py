"""
Модуль предоставляет сервис аутентификации для бота.
"""

import logging
from typing import Optional

from ..database import TokenDB
from .api_client import APIClient

logger = logging.getLogger(__name__)


class AuthService:
    """Сервис для управления JWT-аутентификацией."""

    def __init__(self, client: APIClient, db: TokenDB):
        self.client = client
        self.db = db

    async def login(
        self,
        user_id: int,
        chat_id: int,
        username: Optional[str] = None
    ) -> bool:
        """Логин пользователя и получение JWT-токена."""
        try:
            response = await self.client.post(
                "/api/v1/auth/login",
                json={
                    "user_id": user_id,
                    "chat_id": chat_id,
                    "username": username,
                }
            )

            if response.status_code == 200:
                data = response.json()
                access_token = data["access_token"]
                expires_in = data["expires_in"]

                self.db.save_token(
                    user_id=user_id,
                    access_token=access_token,
                    expires_in=expires_in,
                )
                self.client.set_token(access_token)

                logger.info(f"✅ Токен получен для пользователя {user_id}")
                return True
            else:
                logger.error(f"❌ Ошибка логина: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"❌ Ошибка логина: {e}")
            return False

    async def refresh_token(
        self,
        user_id: int,
        chat_id: Optional[int] = None
    ) -> bool:
        """Обновление токена."""
        self.client.clear_token()
        self.db.delete_token(user_id)
        return await self.login(user_id, chat_id)

    def get_token(self, user_id: int) -> Optional[str]:
        """Получение токена из БД."""
        token = self.db.get_token(user_id)
        if token:
            self.client.set_token(token)
            logger.debug(f"🔑 Токен найден для пользователя {user_id}")
        else:
            logger.warning(f"⚠️ Токен не найден для пользователя {user_id}")
        return token

    def is_token_valid(self, user_id: int) -> bool:
        """Проверка валидности токена."""
        return self.db.get_token(user_id) is not None

    def get_token_info(self, user_id: int) -> Optional[dict]:
        """Информация о токене."""
        return self.db.get_token_info(user_id)

    def logout(self, user_id: int) -> None:
        """Удаление токена (выход)."""
        self.db.delete_token(user_id)
        self.client.clear_token()
        logger.info(f"👋 Пользователь {user_id} вышел")
