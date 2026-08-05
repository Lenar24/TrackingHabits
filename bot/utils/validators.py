"""
Функция validate_habit_name() предоставляет простую
и надежную валидацию названий привычек.
Проверяет, что название не пустое, не состоит только из пробелов
и не превышает максимально допустимую длину.
"""


def validate_habit_name(name: str) -> bool:
    """Проверка корректности названия привычки перед созданием или обновлением."""
    if not name or not name.strip():
        return False
    if len(name) > 100:
        return False
    return True
