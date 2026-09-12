"""
Модуль предоставляет утилиты для форматирования данных в удобочитаемый вид
для отображения в MAX боте.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any


def format_date(date_str: Optional[str]) -> Optional[str]:
    """Преобразование даты в строковый формат ДД-ММ-ГГГГ."""
    if not date_str:
        return None
    try:
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        else:
            dt = date_str
        return dt.strftime("%d-%m-%Y")
    except (ValueError, TypeError):
        return str(date_str)


def format_habit_list(
    habits: List[Dict[str, Any]],
    username: Optional[str] = None
) -> str:
    """Форматирование списка привычек для отображения в боте."""
    if not habits:
        return "📋 У вас пока нет привычек."

    username_text = f"👤 {username}" if username else ""
    text = f"📋 **Ваши привычки** {username_text}\n\n"

    for i, habit in enumerate(habits, 1):
        name = habit.get("name", "Без названия")
        days = habit.get("days_completed", 0)
        max_days = habit.get("max_days", 21)
        is_active = habit.get("is_active", True)

        if is_active:
            status_emoji = "✅" if days > 0 else "⏳"
            status_text = "активна" if days > 0 else "ожидает начала"
        else:
            status_emoji = "🏁"
            status_text = "завершена"

        progress_percent = int((days / max_days) * 100) if max_days > 0 else 0
        progress = min(int((days / max_days) * 20), 20) if max_days > 0 else 0
        progress_bar = "█" * progress + "░" * (20 - progress)

        text += f"{i}. **{name}**\n"
        text += f"   Статус: {status_emoji} {status_text}\n"
        text += f"   Прогресс: {days}/{max_days} дней\n"
        text += f"   [{progress_bar}] {progress_percent}%\n\n"

    text += "\n💡 **Управление привычками:**\n"
    text += "• Нажмите «✅ Отметить выполнение» для отметки\n"
    text += "• Нажмите «🏁 Завершить привычку» для досрочного завершения"

    return text


def format_statistics(stats, username=None):
    """Форматирование общей статистики привычек."""
    if not stats:
        return "📊 У вас пока нет привычек для статистики."

    # ✅ Обрабатываем dict от /api/v1/stats/overall
    if isinstance(stats, dict):
        total_habits = stats.get("total_habits", 0)
        active_habits = stats.get("active_habits", 0)
        completed_habits = stats.get("completed_habits", 0)
        total_days = stats.get("total_days_completed", 0)
        best_streak = stats.get("best_overall_streak", 0)
        completion_rate = stats.get("completion_rate", 0.0)

        username_text = f"👤 {username}" if username else ""
        text = f"📊 **Ваша статистика** {username_text}\n\n"

        text += f"📌 **Всего привычек:** {total_habits}\n"
        text += f"✅ **Активных:** {active_habits}\n"
        text += f"🏁 **Завершено:** {completed_habits}\n"
        text += f"📅 **Всего выполнено дней:** {total_days}\n"
        text += f"🔥 **Лучшая серия:** {best_streak} дней\n"
        text += f"📈 **Эффективность:** {completion_rate:.1f}%\n"

        text += "\n💡 **Советы:**\n"
        if active_habits > 0:
            text += f"• У вас {active_habits} активных привычек. Продолжайте в том же духе! 💪\n"
        if completed_habits > 0:
            text += f"• Вы уже сформировали {completed_habits} привычек! 🎉\n"
        if not active_habits and completed_habits > 0:
            text += "• Добавьте новую привычку для продолжения пути! 🚀\n"

        return text

    # ✅ Если list — старая логика
    if isinstance(stats, list):
        username_text = f"👤 {username}" if username else ""
        text = f"📊 **Ваша статистика** {username_text}\n\n"

        total_habits = len(stats)
        completed_habits = sum(1 for h in stats if not h.get("is_active", True))
        active_habits = total_habits - completed_habits

        text += f"📌 **Всего привычек:** {total_habits}\n"
        text += f"✅ **Активных:** {active_habits}\n"
        text += f"🏁 **Завершено:** {completed_habits}\n\n"

        for habit in stats:
            name = habit.get("name", "Без названия")
            is_active = habit.get("is_active", True)
            days = habit.get("days_completed", 0)
            max_days = habit.get("max_days", 21)
            best_streak = habit.get("best_streak", 0)

            status = "✅ Активна" if is_active else "🏁 Завершена"

            text += f"📌 **{name}**\n"
            text += f"   Статус: {status}\n"
            text += f"   Прогресс: {days}/{max_days} дней\n"
            text += f"   🔥 Лучшая серия: {best_streak} дней\n\n"

        return text

    return "📊 Не удалось загрузить статистику."
