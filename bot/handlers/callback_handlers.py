"""
Модуль отвечает за обработку callback-запросов от инлайн-кнопок в MAX боте.

Обрабатывает действия пользователя: просмотр привычек, отметка выполнения,
пропуск, досрочное завершение и просмотр статистики.
"""

import logging

import httpx

from ..keyboards import create_habit_keyboard, create_main_keyboard
from ..services import HabitService
from ..services.auth_service import AuthService
from ..database import TokenDB
from ..utils import format_habit_list, format_statistics

logger = logging.getLogger(__name__)


async def handle_message_callback(
    update_data: dict,
    bot,
    client,
    auth_service: AuthService,
    token_db: TokenDB,
) -> None:
    """
    Основной обработчик callback-запросов от инлайн-кнопок.

    Args:
        update_data: Данные обновления от MAX API
        bot: Экземпляр бота
        client: HTTP клиент
        auth_service: Сервис аутентификации
        token_db: База токенов
    """
    try:
        callback = update_data.get("callback")
        if not callback:
            return

        payload = callback.get("payload")
        user_id = callback.get("user", {}).get("user_id")
        message = update_data.get("message", {})
        chat_id = message.get("recipient", {}).get("chat_id")
        username = callback.get("user", {}).get("first_name")

        logger.info(f"🔘 Получен callback: {payload}")

        if not chat_id or not user_id:
            logger.warning("⚠️ Отсутствует chat_id или user_id")
            return

        # Используем JWT
        service = HabitService(client, auth_service, token_db)
        await service.get_or_create_user(user_id, None, chat_id)

        # Маршрутизация
        if payload == "my_habits":
            await handle_my_habits(chat_id, user_id, username, bot, service)

        elif payload == "add_habit":
            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "✏️ **Введите название новой привычки:**\n\n"
                    "Например: «Читать 30 минут» или «Заниматься спортом»\n\n"
                    "💡 Цель будет автоматически установлена на 21 день."
                ),
                attachments=create_main_keyboard(),
            )

        elif payload == "mark_complete":
            await handle_mark_complete(chat_id, user_id, bot, service)

        elif payload == "complete_early":
            await handle_complete_early(chat_id, user_id, bot, service)

        elif payload == "stats":
            await handle_stats(chat_id, user_id, username, bot, service)

        elif any(payload.startswith(prefix) for prefix in ["complete_", "skip_", "finish_"]):
            await handle_habit_action(chat_id, user_id, payload, bot, service)

        else:
            logger.warning(f"⚠️ Неизвестный callback: {payload}")

    except (httpx.HTTPError, ValueError, KeyError) as e:
        logger.error(f"❌ Ошибка в message_callback: {e}")


async def handle_my_habits(chat_id, user_id, username, bot, service) -> None:
    """Отображение списка всех привычек пользователя."""
    habits = await service.get_habits(user_id, chat_id=chat_id)
    text = format_habit_list(habits, username)
    await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())


async def handle_mark_complete(chat_id, user_id, bot, service) -> None:
    """Показ списка активных привычек для отметки выполнения."""
    habits = await service.get_habits(user_id, chat_id=chat_id)
    active_habits = [h for h in habits if h.get("is_active", True)]

    if not active_habits:
        await bot.send_message(
            chat_id=chat_id,
            text=(
                "📋 У вас нет активных привычек для управления.\n\n"
                "Добавьте новую привычку через «➕ Добавить привычку»"
            ),
            attachments=create_main_keyboard(),
        )
        return

    text = "✅ **Отметить выполнение привычки**\n\nВыберите привычку:\n\n"
    for habit in active_habits:
        name = habit.get("name", "Без названия")
        days = habit.get("days_completed", 0)
        max_days = habit.get("max_days", 21)
        text += f"📌 **{name}** — {days}/{max_days} дн.\n"

    await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())

    for habit in active_habits:
        habit_id = habit.get("id")
        name = habit.get("name", "Без названия")
        days = habit.get("days_completed", 0)
        max_days = habit.get("max_days", 21)

        await bot.send_message(
            chat_id=chat_id,
            text=(
                f"📌 **{name}**\n"
                f"📊 Прогресс: {days}/{max_days} дней\n\n"
                f"✅ Отметить как выполненную?\n"
                f"❌ Или пропустить сегодняшний день?"
            ),
            attachments=create_habit_keyboard(habit_id),
        )


async def handle_complete_early(chat_id, user_id, bot, service) -> None:
    """Показ списка привычек для досрочного завершения."""
    habits = await service.get_habits(user_id, chat_id=chat_id)
    active_habits = [h for h in habits if h.get("is_active", True)]

    if not active_habits:
        await bot.send_message(
            chat_id=chat_id,
            text="📋 Все привычки уже завершены или ещё не созданы",
            attachments=create_main_keyboard(),
        )
        return

    text = (
        "🏁 **Завершить привычку досрочно**\n\n"
        "Выберите привычку:\n\n"
    )
    for habit in active_habits:
        name = habit.get("name", "Без названия")
        days = habit.get("days_completed", 0)
        max_days = habit.get("max_days", 21)
        text += f"📌 **{name}** — {days}/{max_days} дн.\n"

    await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())

    for habit in active_habits:
        habit_id = habit.get("id")
        name = habit.get("name", "Без названия")
        days = habit.get("days_completed", 0)
        max_days = habit.get("max_days", 21)

        await bot.send_message(
            chat_id=chat_id,
            text=(
                f"📌 **{name}**\n"
                f"📊 Прогресс: {days}/{max_days} дней\n\n"
                f"🏁 Завершить привычку досрочно?"
            ),
            attachments=create_habit_keyboard(habit_id),
        )


async def handle_stats(chat_id, user_id, username, bot, service) -> None:
    """Отображение статистики привычек пользователя."""
    stats = await service.get_stats(user_id, chat_id=chat_id)
    text = format_statistics(stats, username)
    await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())


async def handle_habit_action(chat_id, user_id, payload, bot, service) -> None:
    """Обработка действий с конкретной привычкой."""
    # Правильный парсинг
    if payload.startswith("complete_"):
        action = "complete"
        habit_id = int(payload.replace("complete_", ""))
    elif payload.startswith("skip_"):
        action = "skip"
        habit_id = int(payload.replace("skip_", ""))
    elif payload.startswith("finish_"):
        action = "finish"
        habit_id = int(payload.replace("finish_", ""))
    else:
        logger.error(f"❌ Неизвестное действие: {payload}")
        return

    result = await service.handle_habit_action(user_id, habit_id, action, chat_id=chat_id)

    if result:
        await bot.send_message(
            chat_id=chat_id,
            text=result["text"],
            attachments=create_main_keyboard(),
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="❌ Не удалось выполнить действие. Попробуйте позже.",
            attachments=create_main_keyboard(),
        )
