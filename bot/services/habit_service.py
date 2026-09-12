"""
Класс HabitService является клиентским сервисом для взаимодействия
с бэкенд API из бота.
"""

import logging
from typing import Optional, Dict, Any, List

from .api_client import APIClient
from .auth_service import AuthService

logger = logging.getLogger(__name__)


class HabitService:
    """Сервис для работы с привычками через бэкенд API."""

    def __init__(
        self,
        client: Optional[APIClient] = None,
        auth_service: Optional[AuthService] = None,
        token_db=None
    ):
        self.client = client if client else APIClient()
        self.auth = auth_service
        self.token_db = token_db

    def set_auth_service(self, auth_service: AuthService) -> None:
        """Установка сервиса аутентификации."""
        self.auth = auth_service

    def _get_token(self, user_id: int) -> Optional[str]:
        """Получение токена из AuthService."""
        if not self.auth:
            logger.error("❌ AuthService не установлен!")
            return None
        return self.auth.get_token(user_id)

    async def _ensure_token(
        self,
        user_id: int,
        chat_id: Optional[int] = None
    ) -> Optional[str]:
        """Проверяет валидность токена, при необходимости обновляет."""
        if not self.auth:
            logger.error("❌ AuthService не установлен!")
            return None

        token = self.auth.get_token(user_id)
        if token:
            return token

        logger.info(f"🔄 Получение токена для пользователя {user_id}")
        success = await self.auth.login(user_id, chat_id)
        if success:
            return self.auth.get_token(user_id)

        logger.error(f"❌ Не удалось получить токен для пользователя {user_id}")
        return None

    async def _request(
        self,
        method: str,
        endpoint: str,
        user_id: int,
        chat_id: Optional[int] = None,
        **kwargs
    ):
        """Выполняет HTTP запрос с JWT-токеном."""
        token = await self._ensure_token(user_id, chat_id)
        if not token:
            class ErrorResponse:
                status_code = 401
                def json(self):
                    return {"detail": "Authentication failed"}
                @property
                def text(self):
                    return '{"detail": "Authentication failed"}'
            return ErrorResponse()

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"

        response = await self.client.request(method, endpoint, headers=headers, **kwargs)

        if response.status_code == 401 and self.auth:
            logger.info(f"🔄 Токен истёк для пользователя {user_id}, обновляем...")
            self.auth.logout(user_id)

            if await self.auth.login(user_id, chat_id):
                token = self.auth.get_token(user_id)
                if token:
                    headers["Authorization"] = f"Bearer {token}"
                    response = await self.client.request(method, endpoint, headers=headers, **kwargs)

        return response

    async def get_or_create_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        chat_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Получение или создание пользователя."""
        if not await self._ensure_token(user_id, chat_id):
            response = await self._request(
                "POST", "/api/v1/users/", user_id, chat_id,
                json={"user_id": user_id, "username": username, "chat_id": chat_id}
            )
            if response.status_code in (200, 201):
                return response.json()
            return None

        response = await self._request("GET", "/api/v1/users/me", user_id, chat_id)
        if response.status_code in (200, 201):
            return response.json()
        return None

    async def get_habits(
        self,
        user_id: int,
        active_only: bool = True,
        chat_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Получение привычек пользователя."""
        url = f"/api/v1/habits?active_only={str(active_only).lower()}"
        response = await self._request("GET", url, user_id, chat_id)
        if response.status_code in (200, 201):
            return response.json()
        return []

    async def get_stats(
        self,
        user_id: int,
        chat_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Получение статистики привычек."""
        response = await self._request("GET", "/api/v1/stats/overall", user_id, chat_id)
        if response.status_code in (200, 201):
            return response.json()
        return []

    async def add_habit(
        self,
        user_id: int,
        name: str,
        chat_id: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Создание новой привычки."""
        response = await self._request(
            "POST", "/api/v1/habits/", user_id, chat_id,
            json={"user_id": user_id, "name": name}
        )
        if response.status_code in (200, 201):
            return response.json()
        return None

    async def get_habit_name(
        self,
        habit_id: int,
        user_id: int,
        chat_id: Optional[int] = None
    ) -> Optional[str]:
        """Получение названия привычки по ID."""
        response = await self._request("GET", f"/api/v1/habits/{habit_id}", user_id, chat_id)
        if response.status_code in (200, 201):
            return response.json().get("name", "Без названия")
        return None

    async def _check_habit_active(
        self,
        habit_id: int,
        habit_name: str,
        user_id: int,
        chat_id: Optional[int] = None
    ) -> tuple:
        """Проверяет, активна ли привычка."""
        response = await self._request("GET", f"/api/v1/habits/{habit_id}", user_id, chat_id)
        if response.status_code not in (200, 201):
            return None, {"text": f"❌ Не удалось найти привычку **{habit_name}**."}

        # ✅ ИСПРАВЛЕНО: извлекаем данные из вложенного habit
        result = response.json()
        habit = result.get("habit", result)

        if not habit.get("is_active", True):
            return None, {
                "text": f"ℹ️ Привычка **{habit_name}** уже завершена."
            }
        return habit, None

    async def _handle_complete(
        self, habit_id, habit_name, current_habit, user_id, chat_id=None
    ) -> Dict[str, str]:
        """Обрабатывает отметку выполнения привычки."""
        old_days = current_habit.get("days_completed", 0)
        response = await self._request("POST", f"/api/v1/habits/{habit_id}/complete", user_id, chat_id)

        if response.status_code not in (200, 201):
            return {"text": "❌ Не удалось выполнить действие."}

        # ✅ ИСПРАВЛЕНО: извлекаем данные из вложенного habit
        result = response.json()
        habit = result.get("habit", result)
        days = habit.get("days_completed", 0)
        max_days = habit.get("max_days", 21)
        is_completed = not habit.get("is_active", True)

        if days <= old_days:
            return {
                "text": (
                    f"ℹ️ **Привычка уже отмечена сегодня!**\n\n"
                    f"📌 Привычка: **{habit_name}**\n"
                    f"📊 Текущий прогресс: {days}/{max_days} дней"
                )
            }

        text = (
            f"✅ **Привычка выполнена!**\n\n"
            f"📌 Привычка: **{habit_name}**\n"
            f"📊 Прогресс: {days}/{max_days} дней"
        )
        if is_completed:
            text += f"\n🎉 **Поздравляю! Привычка сформирована через {max_days} дней!** 🏁"
        else:
            text += f"\n💪 Осталось: {max_days - days} дней до цели"
        return {"text": text}

    async def _handle_skip(self, habit_id, habit_name, user_id, chat_id=None) -> Dict[str, str]:
        """Обрабатывает пропуск привычки."""
        response = await self._request("POST", f"/api/v1/habits/{habit_id}/skip", user_id, chat_id)
        if response.status_code not in (200, 201):
            return {"text": "❌ Не удалось выполнить действие."}

        result = response.json()

        # ✅ ПРОВЕРКА: если backend вернул success = false
        if not result.get("success", True):
            return {
                "text": (
                    f"❌ **{result.get('message', 'Не удалось пропустить привычку')}**\n\n"
                    f"📌 Привычка: **{habit_name}**"
                )
            }

        habit = result.get("habit", result)
        days = habit.get("days_completed", 0)
        return {
            "text": (
                f"❌ **Привычка пропущена**\n\n"
                f"📌 Привычка: **{habit_name}**\n"
                f"📊 Прогресс сброшен до {days} дней"
            )
        }

    async def _handle_finish(self, habit_id, habit_name, user_id, chat_id=None) -> Dict[str, str]:
        """Обрабатывает досрочное завершение привычки."""
        response = await self._request("POST", f"/api/v1/habits/{habit_id}/complete-early", user_id, chat_id)
        if response.status_code not in (200, 201):
            return {"text": "❌ Не удалось выполнить действие."}

        result = response.json()

        # ✅ ПРОВЕРКА: если backend вернул success = false
        if not result.get("success", True):
            return {
                "text": (
                    f"❌ **{result.get('message', 'Не удалось завершить привычку')}**\n\n"
                    f"📌 Привычка: **{habit_name}**"
                )
            }

        habit = result.get("habit", result)
        days = habit.get("days_completed", 0)
        max_days = habit.get("max_days", 21)
        return {
            "text": (
                f"🏁 **Привычка завершена досрочно!**\n\n"
                f"📌 Привычка: **{habit_name}**\n"
                f"📊 Прогресс: {days}/{max_days} дней"
            )
        }

    async def handle_habit_action(
        self,
        user_id: int,
        habit_id: int,
        action: str,
        chat_id: Optional[int] = None
    ) -> Dict[str, str]:
        """Обработка действий с привычкой."""
        habit_name = await self.get_habit_name(habit_id, user_id, chat_id)
        if not habit_name:
            return {"text": "❌ Не удалось найти привычку."}

        current_habit, error = await self._check_habit_active(habit_id, habit_name, user_id, chat_id)
        if error:
            return error

        if action == "complete":
            return await self._handle_complete(habit_id, habit_name, current_habit, user_id, chat_id)
        if action == "skip":
            return await self._handle_skip(habit_id, habit_name, user_id, chat_id)
        if action == "finish":
            return await self._handle_finish(habit_id, habit_name, user_id, chat_id)

        return {"text": f"❌ Неизвестное действие: {action}"}

    async def refresh_token(self, user_id: int, chat_id: Optional[int] = None) -> bool:
        """Принудительное обновление токена."""
        if self.auth:
            self.auth.logout(user_id)
            return await self.auth.login(user_id, chat_id)
        return False

    def is_token_valid(self, user_id: int) -> bool:
        """Проверяет валидность токена."""
        return self.auth.is_token_valid(user_id) if self.auth else False

    def get_token_info(self, user_id: int) -> Optional[Dict]:
        """Возвращает информацию о токене."""
        return self.auth.get_token_info(user_id) if self.auth else None

    async def logout(self, user_id: int) -> None:
        """Выход пользователя."""
        if self.auth:
            self.auth.logout(user_id)
        logger.info(f"👋 Пользователь {user_id} вышел")
