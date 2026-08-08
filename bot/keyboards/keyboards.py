"""
Модуль отвечает за создание инлайн-клавиатур для MAX бота.
Предоставляет функции для генерации главного меню и контекстных клавиатур
для управления привычками. Использует библиотеку maxapi
для формирования JSON-структуры кнопок.
"""

from maxapi.types import CallbackButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder


def create_main_keyboard():
    """Создание главного меню бота с основными действиями."""
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(
            type="callback", # type: ignore
            text="📋 Мои привычки",
            payload="my_habits"
        ),
        CallbackButton(
            type="callback", # type: ignore
            text="➕ Добавить привычку",
            payload="add_habit"),
        CallbackButton(
            type="callback",# type: ignore
            text="✅ Отметить выполнение",
            payload="mark_complete"),
        CallbackButton(
            type="callback", # type: ignore
            text="🏁 Завершить привычку",
            payload="complete_early"),
        CallbackButton(
            type="callback", # type: ignore
            text="📊 Статистика",
            payload="stats"),
    )
    builder.adjust(1)
    return [builder.as_markup()]


def create_habit_keyboard(habit_id: int):
    """Создание контекстной клавиатуры для управления конкретной привычкой."""
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(
            type="callback", # type: ignore
            text="✅ Выполнено",
            payload=f"complete_{habit_id}"
        ),
        CallbackButton(
            type="callback", # type: ignore
            text="❌ Пропустить",
            payload=f"skip_{habit_id}"
        ),
        CallbackButton(
            type="callback", # type: ignore
            text="🏁 Завершить досрочно",
            payload=f"finish_{habit_id}"
        ),
    )
    builder.adjust(1)
    return [builder.as_markup()]
