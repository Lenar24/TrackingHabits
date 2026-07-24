import asyncio
import httpx
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logger = logging.getLogger(__name__)

API_URL = os.getenv("API_URL", "http://backend:8000")
BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")

logger.info(f"🔑 Токен загружен: {'ДА' if BOT_TOKEN else 'НЕТ'}")
if BOT_TOKEN:
    logger.info(f"🔑 Длина токена: {len(BOT_TOKEN)} символов")

client = httpx.AsyncClient(timeout=30.0, verify=False)


async def send_reminder_to_user(user_id: int, habits: list, chat_id: int):
    """Отправляет напоминание одному пользователю"""
    logger.info(f"📤 send_reminder_to_user вызвана для user_id={user_id}, chat_id={chat_id}")

    if not habits:
        logger.info(f"ℹ️ У пользователя {user_id} нет привычек")
        return

    # Формируем сообщение
    habits_text = "📋 **Ваши привычки на сегодня:**\n\n"
    for i, habit in enumerate(habits, 1):
        status = "✅" if habit.get("is_active", True) else "❌"
        habits_text += f"{i}. {habit['name']} {status} ({habit.get('days_completed', 0)} дн.)\n"
    habits_text += "\n\n🌟 Не забывайте отмечать выполнение привычек!"

    if not habits_text or habits_text.strip() == "":
        logger.error(f"❌ Текст сообщения пустой для пользователя {user_id}")
        return

    logger.info(f"📝 Текст для {user_id}: {habits_text[:100]}...")

    url = f"https://platform-api2.max.ru/messages?chat_id={chat_id}"
    headers = {
        "Authorization": f"{BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"text": habits_text}

    try:
        logger.info(f"📤 Отправка пользователю {user_id} (chat_id: {chat_id})")
        response = await client.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            logger.info(f"✅ Напоминание отправлено пользователю {user_id}")
        else:
            logger.error(f"❌ Ошибка {user_id}: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"❌ Исключение для {user_id}: {e}")


async def get_users_with_habits():
    """Получает список пользователей с их привычками"""
    try:
        logger.info("🔄 Получение пользователей с привычками...")
        response = await client.get(f"{API_URL}/users/")
        logger.info(f"📊 Статус ответа /users/: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"❌ Ошибка получения пользователей: {response.text}")
            return []

        users = response.json()
        logger.info(f"📊 Получено пользователей: {len(users)}")

        if not users:
            logger.info("ℹ️ Нет пользователей в БД")
            return []

        result = []
        for user in users:
            user_id = user.get('user_id')
            chat_id = user.get('chat_id')
            logger.info(f"📊 Обработка пользователя: {user_id}, chat_id: {chat_id}")

            if not chat_id:
                logger.warning(f"⚠️ У пользователя {user_id} нет chat_id, используем user_id")
                chat_id = user_id

            habits_response = await client.get(f"{API_URL}/habits/{user_id}")
            logger.info(f"📊 Статус ответа /habits/{user_id}: {habits_response.status_code}")

            if habits_response.status_code == 200:
                habits = habits_response.json()
                logger.info(f"📊 Получено привычек для {user_id}: {len(habits)}")

                if habits:
                    active_habits = [h for h in habits if h.get("is_active", True)]
                    if active_habits:
                        result.append({
                            "user_id": user_id,
                            "chat_id": chat_id,
                            "habits": active_habits
                        })
                        logger.info(f"✅ Добавлен пользователь {user_id} с {len(active_habits)} привычками, chat_id: {chat_id}")
                    else:
                        logger.info(f"ℹ️ У пользователя {user_id} нет активных привычек")
                else:
                    logger.info(f"ℹ️ У пользователя {user_id} нет привычек")
            else:
                logger.error(f"❌ Ошибка получения привычек для {user_id}: {habits_response.text}")

        logger.info(f"📊 Итоговый результат: {len(result)} пользователей с активными привычками")
        return result
    except Exception as e:
        logger.error(f"❌ Ошибка получения пользователей: {e}")
        return []


async def send_daily_reminders():
    """Основная функция для отправки ежедневных напоминаний"""
    logger.info("🔄 Запуск рассылки...")
    if not BOT_TOKEN:
        logger.error("❌ Токен не найден!")
        return

    users = await get_users_with_habits()
    if not users:
        logger.info("ℹ️ Нет пользователей с активными привычками")
        return

    logger.info(f"📨 Отправка {len(users)} пользователям")
    tasks = [send_reminder_to_user(u["user_id"], u["habits"], u["chat_id"]) for u in users]
    await asyncio.gather(*tasks)
    logger.info("✅ Рассылка завершена")


def job_function():
    import asyncio
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_daily_reminders())
    except Exception as e:
        logger.error(f"❌ Ошибка в job_function: {e}")
    finally:
        loop.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        job_function,
        trigger=CronTrigger(minute='*'),
        id='test_reminder',
        replace_existing=True,
        name='Тестовые напоминания'
    )
    scheduler.start()
    logger.info("✅ Планировщик запущен (каждую минуту)")
    return scheduler


async def test_reminder():
    print("🧪 Тестирование отправки...")
    await send_daily_reminders()
    await client.aclose()