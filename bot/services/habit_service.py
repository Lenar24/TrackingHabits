import logging

from ..utils import format_date
from .api_client import APIClient

logger = logging.getLogger(__name__)


class HabitService:
    def __init__(self, client=None):
        self.client = client if client else APIClient()

    async def get_or_create_user(self, user_id: int, username: str = None, chat_id: int = None):
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
        url = f"/habits/{user_id}"
        if not active_only:
            url = f"/habits/{user_id}/all"
        response = await self.client.get(url)
        if response.status_code == 200:
            return response.json()
        return []

    async def get_stats(self, user_id: int):
        response = await self.client.get(f"/habits/{user_id}/stats")
        if response.status_code == 200:
            return response.json()
        return []

    async def add_habit(self, user_id: int, name: str):
        response = await self.client.post("/habits/", json={"user_id": user_id, "name": name})
        if response.status_code == 200:
            return response.json()
        return None

    async def get_habit_name(self, habit_id: int):
        response = await self.client.get(f"/habits/item/{habit_id}")
        if response.status_code == 200:
            habit = response.json()
            return habit.get("name", "Без названия")
        return None

    async def handle_habit_action(self, user_id: int, habit_id: int, action: str):
        """Обрабатывает действия с привычкой и возвращает текст для ответа"""
        habit_name = await self.get_habit_name(habit_id)
        if not habit_name:
            return {"text": "❌ Не удалось найти привычку."}

        # Проверяем, активна ли привычка
        current_habit = await self.client.get(f"/habits/item/{habit_id}")
        if current_habit.status_code != 200:
            return {"text": f"❌ Не удалось найти привычку **{habit_name}**."}

        is_active = current_habit.json().get("is_active", True)
        if not is_active:
            return {"text": f"ℹ️ Привычка **{habit_name}** уже завершена. Это действие недоступно."}

        if action == "complete":
            old_days = current_habit.json().get("days_completed", 0)
            response = await self.client.post(f"/habits/{habit_id}/complete")
            if response.status_code == 200:
                habit = response.json()
                days = habit.get("days_completed", 0)
                max_days = habit.get("max_days", 21)
                is_completed = not habit.get("is_active", True)

                if days > old_days:
                    text = (
                        f"✅ **Привычка выполнена!**\n\n📌 Привычка: **{habit_name}**\n📊 Прогресс: {days}/{max_days} дней"
                    )
                    if is_completed:
                        text += f"\n🎉 **Поздравляю! Привычка сформирована через {max_days} дней!** 🏁"
                    else:
                        text += f"\n💪 Осталось: {max_days - days} дней до цели"
                    return {"text": text}
                else:
                    return {
                        "text": f"ℹ️ **Привычка уже отмечена сегодня!**\n\n📌 Привычка: **{habit_name}**\n📊 Текущий прогресс: {days}/{max_days} дней\n💡 Возвращайтесь завтра, чтобы продолжить!"
                    }

        elif action == "skip":
            response = await self.client.post(f"/habits/{habit_id}/skip")
            if response.status_code == 200:
                habit = response.json()
                days = habit.get("days_completed", 0)
                return {
                    "text": f"❌ **Привычка пропущена**\n\n📌 Привычка: **{habit_name}**\n📊 Прогресс сброшен до {days} дней\n💡 Счётчик дней обнулён. Вы можете начать заново в любой день!"
                }

        elif action == "finish":
            response = await self.client.post(f"/habits/{habit_id}/complete-early")
            if response.status_code == 200:
                habit = response.json()
                days = habit.get("days_completed", 0)
                max_days = habit.get("max_days", 21)
                return {
                    "text": f"🏁 **Привычка завершена досрочно!**\n\n📌 Привычка: **{habit_name}**\n📊 Прогресс: {days}/{max_days} дней\n🎉 **Отличная работа!** Вы решили, что привычка сформирована раньше срока!"
                }

        return {"text": f"❌ Не удалось выполнить действие."}
