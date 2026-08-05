# pylint: disable=duplicate-code
"""
Модуль для создания клавиатур в бэкенде.
Используется для отправки напоминаний через прямой API-запрос.
"""

from maxapi.types import CallbackButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder


def create_main_keyboard_payload():
    """
    Создает главную клавиатуру в виде словаря для JSON.
    Используется для отправки напоминаний через прямой API-запрос.
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
    return {"buttons": builder.payload}
