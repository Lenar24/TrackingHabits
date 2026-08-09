"""
Модуль отвечает за обработку callback-запросов от инлайн-кнопок в MAX боте.
Обрабатывает действия пользователя: просмотр привычек, отметка выполнения,
пропуск, досрочное завершение и просмотр статистики.
"""

import logging

import httpx

from ..keyboards import create_habit_keyboard, create_main_keyboard
from ..services import HabitService
from ..utils import format_habit_list, format_statistics

logger = logging.getLogger(__name__)


async def handle_message_callback(update_data: dict, bot, client):
    """Основной обработчик callback-запросов от инлайн-кнопок."""
    try:
        callback = update_data.get("callback")
        if not callback:
            return

        payload = callback.get("payload")
        user_id = callback.get("user", {}).get("user_id")
        message = update_data.get("message", {})
        chat_id = message.get("recipient", {}).get("chat_id")
        username = callback.get("user", {}).get("first_name")

        logger.info("🔘 Получен callback: %s", payload)

        if not chat_id or not user_id:
            return

        service = HabitService(client)
        await service.get_or_create_user(user_id, None, chat_id)  # type: ignore

        if payload == "my_habits":
            await handle_my_habits(chat_id, user_id, username, bot, service)

        elif payload == "add_habit":
            await bot.send_message(
                chat_id=chat_id,
                text="✏️ **Введите название новой привычки:**\n\n"
                "Например: «Читать 30 минут» или «Заниматься спортом»\n\n"
                "💡 Цель будет автоматически установлена на 21 день.",
                attachments=create_main_keyboard(),
            )

        elif payload == "mark_complete":
            await handle_mark_complete(chat_id, user_id, bot, service)

        elif payload == "complete_early":
            await handle_complete_early(chat_id, user_id, bot, service)

        elif payload == "stats":
            await handle_stats(chat_id, user_id, username, bot, service)

        elif payload.startswith("complete_") or payload.startswith("skip_") or payload.startswith("finish_"):
            await handle_habit_action(chat_id, user_id, payload, bot, service)

        else:
            logger.warning("⚠️ Неизвестный callback: %s", payload)

    except (httpx.HTTPError, ValueError, KeyError) as e:
        logger.error("❌ Ошибка в message_callback: %s", e)


async def handle_my_habits(chat_id, user_id, username, bot, service):
    """Отображение списка всех привычек пользователя."""
    habits = await service.get_habits(user_id)
    text = format_habit_list(habits, username)
    await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())


async def handle_mark_complete(chat_id, user_id, bot, service):
    """Показ списка активных привычек для отметки выполнения или пропуска."""
    habits = await service.get_habits(user_id)
    active_habits = [h for h in habits if h.get("is_active", True)]

    if not active_habits:
        await bot.send_message(
            chat_id=chat_id,
            text="📋 У вас нет активных привычек для управления.\n\n"
            "Добавьте новую привычку через «➕ Добавить привычку»",
            attachments=create_main_keyboard(),
        )
        return

    text = "✅ **Отметить выполнение привычки**\n\nВыберите привычку, которую хотите отметить:\n\n"
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
            text=f"📌 **{name}**\n"
            f"📊 Прогресс: {days}/{max_days} дней\n\n"
            f"✅ Отметить как выполненную?\n"
            f"❌ Или пропустить сегодняшний день?",
            attachments=create_habit_keyboard(habit_id),
        )


async def handle_complete_early(chat_id, user_id, bot, service):
    """Показ списка привычек для досрочного завершения."""
    habits = await service.get_habits(user_id)
    active_habits = [h for h in habits if h.get("is_active", True)]

    if not active_habits:
        await bot.send_message(
            chat_id=chat_id, text="📋 Все привычки уже завершены или ещё не созданы", attachments=create_main_keyboard()
        )
        return

    text = (
        "🏁 **Завершить привычку досрочно**\n\n"
        "Выберите привычку, которую хотите завершить "
        "(даже если 21 день не прошёл):\n\n"
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
            text=(f"📌 **{name}**\n" f"📊 Прогресс: {days}/{max_days} дней\n\n" f"🏁 Завершить привычку досрочно?"),
            attachments=create_habit_keyboard(habit_id),
        )


async def handle_stats(chat_id, user_id, username, bot, service):
    """Отображение статистики привычек пользователя."""
    stats = await service.get_stats(user_id)
    text = format_statistics(stats, username)
    await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())


async def handle_habit_action(chat_id, user_id, payload, bot, service):
    """Обработка действий с конкретной привычкой."""
    action, habit_id = payload.split("_")
    habit_id = int(habit_id)

    result = await service.handle_habit_action(user_id, habit_id, action)
    if result:
        await bot.send_message(chat_id=chat_id, text=result["text"], attachments=create_main_keyboard())
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="❌ Не удалось выполнить действие. Попробуйте позже.",
            attachments=create_main_keyboard(),
        )
