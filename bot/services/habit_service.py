"""
Класс HabitService является клиентским сервисом для взаимодействия с бэкенд API из бота.
Обеспечивает все необходимые операции для управления привычками:
регистрация пользователей, получение привычек, создание, отметка выполнения,
пропуск и досрочное завершение.
"""

import logging

from .api_client import APIClient

logger = logging.getLogger(__name__)


class HabitService:
    """Инициализация сервиса с HTTP клиентом."""

    def __init__(self, client=None):
        self.client = client if client else APIClient()

    async def get_or_create_user(self, user_id: int, username: str = None, chat_id: int = None):
        """Получение или создание пользователя в системе."""
        response = await self.client.get(f"/users/{user_id}")
        if response.status_code == 200:
            user_data = response.json()
            if chat_id and user_data.get("chat_id") != chat_id:
                await self.client.put(f"/users/{user_id}/chat_id", json={"chat_id": chat_id})
            return user_data

        response = await self.client.post(
            "/users/", json={"user_id": user_id, "username": username, "chat_id": chat_id}
        )
        if response.status_code == 200:
            return response.json()
        return None

    async def get_habits(self, user_id: int, active_only: bool = True):
        """Получение привычек пользователя."""
        url = f"/habits/{user_id}"
        if not active_only:
            url = f"/habits/{user_id}/all"
        response = await self.client.get(url)
        if response.status_code == 200:
            return response.json()
        return []

    async def get_stats(self, user_id: int):
        """Получение статистики привычек пользователя."""
        response = await self.client.get(f"/habits/{user_id}/stats")
        if response.status_code == 200:
            return response.json()
        return []

    async def add_habit(self, user_id: int, name: str):
        """Создание новой привычки."""
        response = await self.client.post("/habits/", json={"user_id": user_id, "name": name})
        if response.status_code == 200:
            return response.json()
        return None

    async def get_habit_name(self, habit_id: int):
        """Получение названия привычки по ID."""
        response = await self.client.get(f"/habits/item/{habit_id}")
        if response.status_code == 200:
            habit = response.json()
            return habit.get("name", "Без названия")
        return None

    async def _check_habit_active(self, habit_id: int, habit_name: str):
        """Проверяет, активна ли привычка."""
        current_habit = await self.client.get(f"/habits/item/{habit_id}")
        if current_habit.status_code != 200:
            return None, {"text": f"❌ Не удалось найти привычку **{habit_name}**."}

        is_active = current_habit.json().get("is_active", True)
        if not is_active:
            return None, {
                "text": f"ℹ️ Привычка **{habit_name}** уже завершена. "
                        f"Это действие недоступно."
            }

        return current_habit.json(), None

    async def _handle_complete(self, habit_id: int, habit_name: str, current_habit: dict):
        """Обрабатывает отметку выполнения привычки."""
        old_days = current_habit.get("days_completed", 0)
        response = await self.client.post(f"/habits/{habit_id}/complete")
        if response.status_code != 200:
            return {"text": "❌ Не удалось выполнить действие."}

        habit = response.json()
        days = habit.get("days_completed", 0)
        max_days = habit.get("max_days", 21)
        is_completed = not habit.get("is_active", True)

        if days <= old_days:
            return {
                "text": f"ℹ️ **Привычка уже отмечена сегодня!**\n\n"
                f"📌 Привычка: **{habit_name}**\n"
                f"📊 Текущий прогресс: {days}/{max_days} дней\n"
                f"💡 Возвращайтесь завтра, чтобы продолжить!"
            }

        text = (
            f"✅ **Привычка выполнена!**\n\n"
            f"📌 " f"Привычка: **{habit_name}**\n"
            f"📊 Прогресс: {days}/{max_days} дней"
        )
        if is_completed:
            text += f"\n🎉 **Поздравляю! Привычка сформирована через {max_days} дней!** 🏁"
        else:
            text += f"\n💪 Осталось: {max_days - days} дней до цели"
        return {"text": text}

    async def _handle_skip(self, habit_id: int, habit_name: str):
        """Обрабатывает пропуск привычки."""
        response = await self.client.post(f"/habits/{habit_id}/skip")
        if response.status_code != 200:
            return {"text": "❌ Не удалось выполнить действие."}

        habit = response.json()
        days = habit.get("days_completed", 0)
        return {
            "text": f"❌ **Привычка пропущена**\n\n"
            f"📌 Привычка: **{habit_name}**\n"
            f"📊 Прогресс сброшен до {days} дней\n"
            f"💡 Счётчик дней обнулён. Вы можете начать заново в любой день!"
        }

    async def _handle_finish(self, habit_id: int, habit_name: str):
        """Обрабатывает досрочное завершение привычки."""
        response = await self.client.post(f"/habits/{habit_id}/complete-early")
        if response.status_code != 200:
            return {"text": "❌ Не удалось выполнить действие."}

        habit = response.json()
        days = habit.get("days_completed", 0)
        max_days = habit.get("max_days", 21)
        return {
            "text": f"🏁 **Привычка завершена досрочно!**\n\n"
            f"📌 Привычка: **{habit_name}**\n"
            f"📊 Прогресс: {days}/{max_days} дней\n"
            f"🎉 **Отличная работа!** "
            f"Вы решили, что привычка сформирована раньше срока!"
        }

    async def handle_habit_action(self, habit_id: int, action: str):
        """
        Обработка действий с привычкой (выполнить, пропустить, завершить).
        Возвращает текст для ответа
        """
        habit_name = await self.get_habit_name(habit_id)
        if not habit_name:
            return {"text": "❌ Не удалось найти привычку."}

        current_habit, error = await self._check_habit_active(habit_id, habit_name)
        if error:
            return error

        if action == "complete":
            return await self._handle_complete(habit_id, habit_name, current_habit)
        if action == "skip":
            return await self._handle_skip(habit_id, habit_name)
        if action == "finish":
            return await self._handle_finish(habit_id, habit_name)

        return {"text": "❌ Не удалось выполнить действие."}
