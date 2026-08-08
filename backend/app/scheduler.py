"""
Модуль отвечает за автоматическую отправку напоминаний
о привычках пользователям через платформу Max.
Использует APScheduler для планирования ежедневных рассылок
и проверки правила 21 дня.
"""

import asyncio
import json
import logging
import os

import httpx
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .services.habit_service import HabitService
from .utils.database import SessionLocal
from .utils.keyboards import create_main_keyboard_payload

logger = logging.getLogger(__name__)

API_URL = os.getenv("API_URL", "http://backend:8000")
BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")

logger.info("🔑 Токен загружен: %s", "ДА" if BOT_TOKEN else "НЕТ")
if BOT_TOKEN:
    logger.info("🔑 Длина токена: %s символов", len(BOT_TOKEN))

# Московский часовой пояс
moscow_tz = pytz.timezone("Europe/Moscow")


async def send_reminder_to_user(user_id: int, habits: list, chat_id: int):
    """Отправляет напоминание одному пользователю"""
    if not habits:
        return

    habits_text = "📋 **Ваши привычки на сегодня:**\n\n"
    for i, habit in enumerate(habits, 1):
        status = "✅" if habit.get("is_active", True) else "❌"
        progress = f"{habit.get('days_completed', 0)}/{habit.get('max_days', 21)} дн."
        habits_text += f"{i}. {habit['name']} {status} ({progress})\n"

    habits_text += "\n\n⚠️ Не забывайте отмечать выполнение привычек!"
    habits_text += "\n❤️ Для отметки выполнения нажмите кнопку ниже."

    # Используем общую функцию из utils.keyboards
    keyboard = create_main_keyboard_payload()

    url = f"https://platform-api2.max.ru/messages?chat_id={chat_id}"
    headers = {"Authorization": f"{BOT_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "text": habits_text,
        "attachments": [
            {
                "type": "inline_keyboard",
                "payload": keyboard
            }
        ]
    }

    try:
        logger.info("📤 Отправка пользователю %s (chat_id: %s)", user_id, chat_id)
        async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                logger.info("✅ Напоминание отправлено пользователю %s", user_id)
            else:
                logger.error("❌ Ошибка %s: %s - %s", user_id, response.status_code, response.text)
    except (httpx.HTTPError, asyncio.TimeoutError, json.JSONDecodeError) as e:
        logger.error("❌ Исключение для %s: %s", user_id, e)


async def get_users_with_habits():
    """Получает список пользователей с их активными привычками"""
    try:
        async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
            response = await client.get(f"{API_URL}/users/")
            if response.status_code != 200:
                logger.error("❌ Ошибка получения пользователей: %s", response.text)
                return []

            users = response.json()
            result = []
            for user in users:
                user_id = user.get("user_id")
                chat_id = user.get("chat_id")

                if not chat_id:
                    chat_id = user_id

                habits_response = await client.get(f"{API_URL}/habits/{user_id}")
                if habits_response.status_code == 200:
                    habits = habits_response.json()
                    active_habits = [h for h in habits if h.get("is_active", True)]
                    if active_habits:
                        result.append(
                            {
                                "user_id": user_id,
                                "chat_id": chat_id,
                                "habits": active_habits
                            }
                        )
            return result
    except (httpx.HTTPError, asyncio.TimeoutError, KeyError, ValueError) as e:
        logger.error("❌ Ошибка получения пользователей: %s", e)
        return []


async def send_daily_reminders():
    """
    Основная функция для отправки ежедневных напоминаний
    всем пользователям с активными привычками
    """
    logger.info("🔄 Запуск рассылки...")
    if not BOT_TOKEN:
        logger.error("❌ Токен не найден!")
        return

    users = await get_users_with_habits()
    if not users:
        logger.info("ℹ️ Нет пользователей с активными привычками")
        return

    logger.info("📨 Отправка %s пользователям", len(users))
    tasks = [send_reminder_to_user(u["user_id"], u["habits"], u["chat_id"]) for u in users]
    await asyncio.gather(*tasks)
    logger.info("✅ Рассылка завершена")


def check_21_days_job():
    """Обёртка для проверки правила 21 дня"""
    db = SessionLocal()
    try:
        result = HabitService.check_21_days(db)
        logger.info(
            "✅ Правило 21 дня: обновлено %s, завершено %s",
            result["updated"], result["completed"]
        )
    except (ValueError, KeyError) as e:
        logger.error("❌ Ошибка проверки правила 21 дня: %s", e)
    finally:
        db.close()


def job_function():
    """Обёртка для запуска асинхронной функции с правильным event loop"""
    logger.info("🔄 job_function вызвана!")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_daily_reminders())
    except (httpx.HTTPError, asyncio.TimeoutError, ValueError) as e:
        logger.error("❌ Ошибка в job_function: %s", e)
    finally:
        if loop and not loop.is_closed():
            loop.close()


def start_scheduler():
    """Старт планировщика"""
    scheduler = BackgroundScheduler()

    # Утренние напоминания (9:00 по Москве)
    scheduler.add_job(
        job_function,
        trigger=CronTrigger(hour=9, minute=0, timezone=moscow_tz),
        id="morning_reminder_09_00",
        replace_existing=True,
        name="Утренние напоминания в 9:00",
    )

    # Вечерние напоминания (21:00 по Москве)
    scheduler.add_job(
        job_function,
        trigger=CronTrigger(hour=21, minute=0, timezone=moscow_tz),
        id="evening_reminder_21_00",
        replace_existing=True,
        name="Вечерние напоминания в 21:00",
    )

    # Проверка правила 21 дня (каждый день в полночь по Москве)
    scheduler.add_job(
        check_21_days_job,
        trigger=CronTrigger(hour=0, minute=0, timezone=moscow_tz),
        id="check_21_days",
        replace_existing=True,
        name="Правило 21 дня",
    )

    # Для теста уведомления приходят через 1 минуту
    #scheduler.add_job(
    #    job_function,
    #    trigger=CronTrigger(minute='*', timezone=moscow_tz),
    #    id='test_every_minute',
    #    replace_existing=True,
    #    name='Тест каждую минуту'
    #)

    scheduler.start()
    logger.info("✅ Планировщик запущен (ежедневно в 9:00 и 21:00 по Москве)")
    return scheduler


async def test_reminder():
    """Тест напоминаний"""
    print("🧪 Тестирование отправки...")
    await send_daily_reminders()
