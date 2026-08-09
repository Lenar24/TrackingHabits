# pylint: disable=duplicate-code
"""
Модуль для создания клавиатур в бэкенде.
Используется для отправки напоминаний через прямой API-запрос.
"""


from maxapi.utils.inline_keyboard import InlineKeyboardBuilder


def create_main_keyboard_payload():
    """
    Создает главную клавиатуру в виде словаря для JSON.
    Используется для отправки напоминаний через прямой API-запрос.
    """
    # должен быть JSON
    builder = InlineKeyboardBuilder()
    builder.add(
        {"type": "callback", "text": "📋 Мои привычки", "payload": "my_habits"},
        {"type": "callback", "text": "➕ Добавить привычку", "payload": "add_habit"},
        {"type": "callback", "text": "✅ Отметить выполнение", "payload": "mark_complete"},
        {"type": "callback", "text": "🏁 Завершить привычку", "payload": "complete_early"},
        {"type": "callback", "text": "📊 Статистика", "payload": "stats"},
    )
    builder.adjust(1)
    return {"buttons": builder.payload}
