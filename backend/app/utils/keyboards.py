"""
Модуль для создания клавиатур в бэкенде.
Используется для отправки напоминаний через API.
"""

import json
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class KeyboardButton:
    """Класс для представления кнопки клавиатуры."""

    def __init__(self, text: str, payload: str, button_type: str = "callback"):
        self.text = text
        self.payload = payload
        self.type = button_type

    def to_dict(self) -> Dict[str, str]:
        """Преобразование кнопки в словарь."""
        return {
            "type": self.type,
            "text": self.text,
            "payload": self.payload,
        }


class InlineKeyboardBuilder:
    """Построитель инлайн-клавиатуры."""

    def __init__(self):
        self.buttons: List[KeyboardButton] = []
        self.row_width = 1

    def add(self, text: str, payload: str, button_type: str = "callback") -> 'InlineKeyboardBuilder':
        """
        Добавление кнопки.

        Args:
            text: Текст кнопки
            payload: Payload кнопки
            button_type: Тип кнопки (callback, url, etc.)

        Returns:
            InlineKeyboardBuilder: Для цепочки вызовов
        """
        self.buttons.append(KeyboardButton(text, payload, button_type))
        return self

    def adjust(self, row_width: int) -> 'InlineKeyboardBuilder':
        """
        Установка ширины ряда.

        Args:
            row_width: Количество кнопок в ряду

        Returns:
            InlineKeyboardBuilder: Для цепочки вызовов
        """
        self.row_width = row_width
        return self

    def build(self) -> Dict[str, Any]:
        """
        Построение клавиатуры.

        Returns:
            Dict: Клавиатура в формате для API
        """
        if not self.buttons:
            return {}

        # Разбиваем кнопки по рядам
        keyboard = []
        for i in range(0, len(self.buttons), self.row_width):
            row = self.buttons[i:i + self.row_width]
            keyboard.append([button.to_dict() for button in row])

        return {"buttons": keyboard}

    @property
    def payload(self) -> List[List[Dict[str, str]]]:
        """Payload для отправки в API."""
        if not self.buttons:
            return []

        keyboard = []
        for i in range(0, len(self.buttons), self.row_width):
            row = self.buttons[i:i + self.row_width]
            keyboard.append([button.to_dict() for button in row])

        return keyboard


def create_main_keyboard_payload() -> Dict[str, Any]:
    """
    Создает главную клавиатуру в виде словаря для JSON.

    Returns:
        Dict: Клавиатура для отправки
    """
    try:
        builder = InlineKeyboardBuilder()
        builder.add("📋 Мои привычки", "my_habits")
        builder.add("➕ Добавить привычку", "add_habit")
        builder.add("✅ Отметить выполнение", "mark_complete")
        builder.add("🏁 Завершить привычку", "complete_early")
        builder.add("📊 Статистика", "stats")
        builder.adjust(1)

        result = builder.build()
        logger.debug("Created main keyboard payload")
        return result

    except Exception as e:
        logger.error(f"Failed to create keyboard: {e}")
        return {}


def create_habit_keyboard(habit_id: int, habit_name: str) -> Dict[str, Any]:
    """
    Создает клавиатуру для конкретной привычки.

    Args:
        habit_id: ID привычки
        habit_name: Название привычки

    Returns:
        Dict: Клавиатура для привычки
    """
    builder = InlineKeyboardBuilder()
    builder.add(
        f"✅ Выполнить: {habit_name}",
        f"complete_habit_{habit_id}"
    )
    builder.add(
        f"⏭️ Пропустить: {habit_name}",
        f"skip_habit_{habit_id}"
    )
    builder.add("◀️ Назад", "back_to_habits")
    builder.adjust(1)

    return builder.build()


def create_stats_keyboard() -> Dict[str, Any]:
    """
    Создает клавиатуру для статистики.
    """
    builder = InlineKeyboardBuilder()
    builder.add("📈 Общая статистика", "stats_overall")
    builder.add("📊 По привычкам", "stats_by_habit")
    builder.add("◀️ Назад", "back_to_main")
    builder.adjust(1)

    return builder.build()
