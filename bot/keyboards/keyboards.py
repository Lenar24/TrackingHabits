"""
Модуль отвечает за создание инлайн-клавиатур для MAX бота.
"""

from maxapi.enums import ButtonType
from maxapi.types import CallbackButton
from maxapi.types.attachments import AttachmentButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder


def create_main_keyboard() -> list[AttachmentButton]:
    """
    Создание главного меню бота с основными действиями.

    Returns:
        list[AttachmentButton]: Клавиатура для отправки
    """
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(type=ButtonType.CALLBACK, text="📋 Мои привычки", payload="my_habits"),
        CallbackButton(type=ButtonType.CALLBACK, text="➕ Добавить привычку", payload="add_habit"),
        CallbackButton(type=ButtonType.CALLBACK, text="✅ Отметить выполнение", payload="mark_complete"),
        CallbackButton(type=ButtonType.CALLBACK, text="🏁 Завершить привычку", payload="complete_early"),
        CallbackButton(type=ButtonType.CALLBACK, text="📊 Статистика", payload="stats"),
    )
    builder.adjust(1)
    return [builder.as_markup()]


def create_habit_keyboard(habit_id: int) -> list[AttachmentButton]:
    """
    Создание контекстной клавиатуры для управления конкретной привычкой.

    Args:
        habit_id: ID привычки

    Returns:
        list[AttachmentButton]: Клавиатура для отправки
    """
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(type=ButtonType.CALLBACK, text="✅ Выполнено", payload=f"complete_{habit_id}"),
        CallbackButton(type=ButtonType.CALLBACK, text="❌ Пропустить", payload=f"skip_{habit_id}"),
        CallbackButton(type=ButtonType.CALLBACK, text="🏁 Завершить досрочно", payload=f"finish_{habit_id}"),
    )
    builder.adjust(1)
    return [builder.as_markup()]


def create_stats_keyboard() -> list[AttachmentButton]:
    """Создание клавиатуры для статистики."""
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(type=ButtonType.CALLBACK, text="📈 Общая статистика", payload="stats_overall"),
        CallbackButton(type=ButtonType.CALLBACK, text="📊 По привычкам", payload="stats_by_habit"),
        CallbackButton(type=ButtonType.CALLBACK, text="◀️ Назад", payload="back_to_main"),
    )
    builder.adjust(1)
    return [builder.as_markup()]


def create_confirm_keyboard(action: str, habit_id: int) -> list[AttachmentButton]:
    """Создание клавиатуры подтверждения действия."""
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(type=ButtonType.CALLBACK, text="✅ Да", payload=f"confirm_{action}_{habit_id}"),
        CallbackButton(type=ButtonType.CALLBACK, text="❌ Нет", payload=f"cancel_{action}_{habit_id}"),
    )
    builder.adjust(2)
    return [builder.as_markup()]


def create_back_keyboard() -> list[AttachmentButton]:
    """Создание клавиатуры с кнопкой назад."""
    builder = InlineKeyboardBuilder()
    builder.add(
        CallbackButton(type=ButtonType.CALLBACK, text="◀️ Назад", payload="back_to_main"),
    )
    builder.adjust(1)
    return [builder.as_markup()]
