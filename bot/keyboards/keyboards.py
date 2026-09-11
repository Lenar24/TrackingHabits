"""
Модуль отвечает за создание инлайн-клавиатур для MAX бота.
"""

from typing import List, Dict, Any

from maxapi.types import CallbackButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder


def create_main_keyboard() -> List[Dict[str, Any]]:
    """
    Создание главного меню бота с основными действиями.

    Returns:
        List[Dict[str, Any]]: Клавиатура для отправки
    """
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(type="callback", text="📋 Мои привычки", payload="my_habits"),
        CallbackButton(type="callback", text="➕ Добавить привычку", payload="add_habit"),
        CallbackButton(type="callback", text="✅ Отметить выполнение", payload="mark_complete"),
        CallbackButton(type="callback", text="🏁 Завершить привычку", payload="complete_early"),
        CallbackButton(type="callback", text="📊 Статистика", payload="stats"),
    )
    builder.adjust(1)
    return [builder.as_markup()]


def create_habit_keyboard(habit_id: int) -> List[Dict[str, Any]]:
    """
    Создание контекстной клавиатуры для управления конкретной привычкой.

    Args:
        habit_id: ID привычки

    Returns:
        List[Dict[str, Any]]: Клавиатура для отправки
    """
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(type="callback", text="✅ Выполнено", payload=f"complete_{habit_id}"),
        CallbackButton(type="callback", text="❌ Пропустить", payload=f"skip_{habit_id}"),
        CallbackButton(type="callback", text="🏁 Завершить досрочно", payload=f"finish_{habit_id}"),
    )
    builder.adjust(1)
    return [builder.as_markup()]


def create_stats_keyboard() -> List[Dict[str, Any]]:
    """Создание клавиатуры для статистики."""
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(type="callback", text="📈 Общая статистика", payload="stats_overall"),
        CallbackButton(type="callback", text="📊 По привычкам", payload="stats_by_habit"),
        CallbackButton(type="callback", text="◀️ Назад", payload="back_to_main"),
    )
    builder.adjust(1)
    return [builder.as_markup()]


def create_confirm_keyboard(action: str, habit_id: int) -> List[Dict[str, Any]]:
    """Создание клавиатуры подтверждения действия."""
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(type="callback", text="✅ Да", payload=f"confirm_{action}_{habit_id}"),
        CallbackButton(type="callback", text="❌ Нет", payload=f"cancel_{action}_{habit_id}"),
    )
    builder.adjust(2)
    return [builder.as_markup()]


def create_back_keyboard() -> List[Dict[str, Any]]:
    """Создание клавиатуры с кнопкой назад."""
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(type="callback", text="◀️ Назад", payload="back_to_main"),
    )
    builder.adjust(1)
    return [builder.as_markup()]
