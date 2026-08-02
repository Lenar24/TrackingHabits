def validate_habit_name(name: str) -> bool:
    """Проверяет, что название привычки корректно"""
    if not name or len(name.strip()) == 0:
        return False
    if len(name) > 100:
        return False
    return True
