from maxapi.utils.inline_keyboard import InlineKeyboardBuilder


def create_main_keyboard():
    """Создает главную клавиатуру (меню)"""
    builder = InlineKeyboardBuilder()
    builder.add(
        {"type": "callback", "text": "📋 Мои привычки", "payload": "my_habits"},
        {"type": "callback", "text": "➕ Добавить привычку", "payload": "add_habit"},
        {"type": "callback", "text": "✅ Отметить выполнение", "payload": "mark_complete"},
        {"type": "callback", "text": "🏁 Завершить привычку", "payload": "complete_early"},
        {"type": "callback", "text": "📊 Статистика", "payload": "stats"},
    )
    builder.adjust(1)
    return [builder.as_markup()]


def create_habit_keyboard(habit_id: int):
    """Создает клавиатуру для управления привычкой"""
    builder = InlineKeyboardBuilder()
    builder.add(
        {"type": "callback", "text": "✅ Выполнено", "payload": f"complete_{habit_id}"},
        {"type": "callback", "text": "❌ Пропустить", "payload": f"skip_{habit_id}"},
        {"type": "callback", "text": "🏁 Завершить досрочно", "payload": f"finish_{habit_id}"},
    )
    builder.adjust(1)
    return [builder.as_markup()]
