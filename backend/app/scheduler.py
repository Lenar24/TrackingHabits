"""
Модуль отвечает за автоматическую отправку напоминаний
о привычках пользователям через платформу Max.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from asyncio import Semaphore
from datetime import datetime, timedelta

import httpx
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from tenacity import retry, stop_after_attempt, wait_exponential
from jose import jwt

from .core.config import settings
from .services.habit_service import HabitService
from .utils.database import SessionLocal
from .utils.keyboards import create_main_keyboard_payload
from .utils.auth import create_access_token

logger = logging.getLogger(__name__)

# Константы
MOSCOW_TZ = pytz.timezone("Europe/Moscow")
MAX_CONCURRENT_REQUESTS = 10
REMINDER_TIMEOUT = 30.0
MAX_RETRIES = 3

# Ограничитель для параллельных запросов
semaphore = Semaphore(MAX_CONCURRENT_REQUESTS)


def create_system_token(data: dict) -> str:
    """
    Создание системного токена (без истечения).
    Используется для внутренних вызовов планировщика.
    """
    to_encode = data.copy()
    to_encode.update({"type": "system"})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def get_http_client() -> httpx.AsyncClient:
    """
    Создание HTTP клиента с правильной конфигурацией.
    """
    verify_ssl = settings.ENVIRONMENT != "development"

    return httpx.AsyncClient(
        timeout=httpx.Timeout(REMINDER_TIMEOUT),
        verify=verify_ssl,
        limits=httpx.Limits(max_keepalive_connections=20, max_connections=50)
    )


def get_internal_token() -> str:
    """
    Получение токена для внутренних API вызовов.
    Создает системный токен с расширенными правами.
    """
    if settings.INTERNAL_API_TOKEN:
        return settings.INTERNAL_API_TOKEN

    # Создаем системный токен для сервисов
    token_data = {
        "sub": "system",
        "user_id": 0,
        "chat_id": 0,
        "system": True
    }
    return create_system_token(token_data)


@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
async def send_reminder_to_user(
    user_id: int,
    habits: List[Dict[str, Any]],
    chat_id: int
) -> bool:
    """
    Отправляет напоминание одному пользователю с повторными попытками.

    Args:
        user_id: ID пользователя
        habits: Список привычек
        chat_id: ID чата

    Returns:
        bool: True если успешно отправлено
    """
    if not habits or not chat_id:
        return False

    # Ограничиваем количество одновременных запросов
    async with semaphore:
        try:
            # Формируем сообщение
            habits_text = _format_habits_message(habits)
            keyboard = create_main_keyboard_payload()

            # Отправляем запрос
            url = f"https://platform-api2.max.ru/messages?chat_id={chat_id}"
            headers = {
                "Authorization": f"{settings.MAX_BOT_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "text": habits_text,
                "attachments": [{"type": "inline_keyboard", "payload": keyboard}]
            }

            logger.info(f"📤 Отправка напоминания пользователю {user_id} (chat_id: {chat_id})")

            async with get_http_client() as client:
                response = await client.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    logger.info(f"✅ Напоминание отправлено пользователю {user_id}")
                    return True
                else:
                    logger.error(
                        f"❌ Не удалось отправить напоминание пользователю {user_id}: "
                        f"status={response.status_code}, response={response.text}"
                    )
                    return False

        except httpx.TimeoutException:
            logger.error(f"⏱️ Истекло время ожидания отправки напоминания пользователю {user_id}")
            raise
        except httpx.HTTPError as e:
            logger.error(f"❌ HTTP ошибка для пользователя {user_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Непредвиденная ошибка для пользователя {user_id}: {e}")
            raise


def _format_habits_message(habits: List[Dict[str, Any]]) -> str:
    """
    Форматирование списка привычек в текстовое сообщение.
    """
    if not habits:
        return "📋 У вас нет активных привычек на сегодня."

    lines = ["📋 **Ваши привычки на сегодня:**", ""]

    for i, habit in enumerate(habits, 1):
        name = habit.get('name', 'Без названия')
        is_active = habit.get('is_active', True)
        days = habit.get('days_completed', 0)
        max_days = habit.get('max_days', 21)
        status = "✅" if is_active else "❌"

        lines.append(f"{i}. {name} {status} ({days}/{max_days} дн.)")

    lines.extend([
        "",
        "⚠️ Не забывайте отмечать выполнение привычек!",
        "❤️ Для отметки выполнения нажмите кнопку ниже."
    ])

    return "\n".join(lines)


async def get_users_with_habits() -> List[Dict[str, Any]]:
    """
    Получает список пользователей с их активными привычками.
    Использует внутренний API с системным токеном.
    """
    try:
        token = get_internal_token()
        headers = {"Authorization": f"Bearer {token}"}

        async with get_http_client() as client:
            # Получаем всех пользователей
            users_response = await client.get(
                f"{settings.API_URL}/api/v1/users",
                headers=headers
            )

            if users_response.status_code != 200:
                logger.error(f"❌ Не удалось получить пользователей: {users_response.text}")
                return []

            users = users_response.json()
            result = []

            for user in users:
                user_id = user.get("id")
                max_user_id = user.get("max_user_id")
                chat_id = user.get("chat_id")
                username = user.get("username", f"User_{user_id}")

                if not chat_id:
                    logger.warning(f"⚠️ Пользователь {username} отсутствует chat_id, пропускаем")
                    continue

                if not user.get("is_active", True):
                    logger.debug(f"⏭️ Пользователь {username} неактивен, пропускаем")
                    continue

                # Получаем привычки пользователя
                habits_response = await client.get(
                    f"{settings.API_URL}/api/v1/habits",
                    params={"user_id": user_id, "active_only": True},
                    headers=headers
                )

                if habits_response.status_code == 200:
                    habits = habits_response.json()
                    if habits:
                        result.append({
                            "user_id": user_id,
                            "max_user_id": max_user_id,
                            "chat_id": chat_id,
                            "username": username,
                            "habits": habits,
                            "habit_count": len(habits)
                        })

            logger.info(f"📊 Найдены {len(result)} пользователей с активными привычками")
            return result

    except httpx.TimeoutException:
        logger.error("⏱️ Timeout при получении пользователей с привычками")
        return []
    except httpx.HTTPError as e:
        logger.error(f"❌ Ошибка HTTP при получении пользователей: {e}")
        return []
    except Exception as e:
        logger.error(f"❌ Неожиданная ошибка при получении пользователей: {e}")
        return []


async def send_daily_reminders() -> Dict[str, Any]:
    """
    Основная функция для отправки ежедневных напоминаний.

    Returns:
        Dict: Статистика отправки
    """
    logger.info("🔄 Старт ежедневных напоминаний...")

    if not settings.MAX_BOT_TOKEN:
        logger.error("❌ MAX_BOT_TOKEN не настроен")
        return {"error": "Bot token не настроен"}

    users = await get_users_with_habits()

    if not users:
        logger.info("ℹ️ Нет пользователей с активными привычками")
        return {"message": "Нет пользователей с активными привычками"}

    # Отправляем напоминания параллельно
    tasks = [
        send_reminder_to_user(
            user_data["user_id"],
            user_data["habits"],
            user_data["chat_id"]
        )
        for user_data in users
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Подсчет статистики
    successful = sum(1 for r in results if r is True)
    failed = len(results) - successful

    logger.info(f"✅ Напоминания отправлены: {successful} успешно, {failed} неуспешно")

    return {
        "total": len(users),
        "successful": successful,
        "failed": failed,
        "users": users
    }


def check_21_days_job() -> Dict[str, Any]:
    """
    Проверка правила 21 дня для всех пользователей.
    """
    logger.info("🔄 Проверка соблюдения правила 21 дня...")

    db = SessionLocal()
    try:
        result = HabitService.check_21_days(db)
        logger.info(
            f"✅ Проверка правила 21 дня: updated={result['updated']}, "
            f"completed={result['completed']}, errors={len(result.get('errors', []))}"
        )
        return result
    except Exception as e:
        logger.error(f"❌ Ошибка при проверке правила 21 дня: {e}")
        return {"error": str(e)}
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error(f"❌ Ошибка при закрытии сессии: {e}")


def job_function() -> None:
    """
    Обёртка для запуска асинхронной функции.
    """
    logger.info("🔄 Выполнение запланированного задания...")
    try:
        result = asyncio.run(send_daily_reminders())
        logger.info(f"✅ Запланированное задание выполнено: {result}")
    except Exception as e:
        logger.error(f"❌ Запланированное задание завершилось с ошибкой: {e}")


def start_scheduler() -> BackgroundScheduler:
    """
    Запуск планировщика с настройкой задач.

    Returns:
        BackgroundScheduler: Экземпляр планировщика
    """
    scheduler = BackgroundScheduler()

    # Очищаем существующие задачи
    scheduler.remove_all_jobs()

    # 1. Утренние напоминания (9:00 по Москве)
    scheduler.add_job(
        job_function,
        trigger=CronTrigger(hour=9, minute=0, timezone=MOSCOW_TZ),
        id="morning_reminder_09_00",
        replace_existing=True,
        name="Утренние напоминания в 9:00",
        max_instances=1,
        misfire_grace_time=3600  # 1 час на восстановление
    )
    logger.info("⏰ Добавлено утреннее напоминание в 9:00 по московскому времени")

    # 2. Вечерние напоминания (21:00 по Москве)
    scheduler.add_job(
        job_function,
        trigger=CronTrigger(hour=21, minute=0, timezone=MOSCOW_TZ),
        id="evening_reminder_21_00",
        replace_existing=True,
        name="Вечерние напоминания в 21:00",
        max_instances=1,
        misfire_grace_time=3600
    )
    logger.info("⏰ Добавлено вечернее напоминание в 21:00 по московскому времени")

    # 3. Проверка правила 21 дня (каждый день в полночь + 5 минут)
    scheduler.add_job(
        check_21_days_job,
        trigger=CronTrigger(hour=0, minute=5, timezone=MOSCOW_TZ),
        id="check_21_days",
        replace_existing=True,
        name="Правило 21 дня",
        max_instances=1,
        misfire_grace_time=3600
    )
    logger.info("⏰ Добавлена проверка правила 21 дня в 00:05 по московскому времени")

    # Запускаем планировщик
    scheduler.start()
    logger.info("✅ Планировщик успешно запущен")

    # Логируем все задачи
    for job in scheduler.get_jobs():
        logger.info(f"📋 Запланированное задание: {job.id} - {job.name}")

    return scheduler


async def send_test_reminder(user_id: int, chat_id: int) -> bool:
    """
    Отправка тестового напоминания конкретному пользователю.

    Args:
        user_id: ID пользователя
        chat_id: ID чата

    Returns:
        bool: True если успешно
    """
    logger.info(f"🧪 Отправка напоминания о тестировании пользователю {user_id}")

    # Получаем привычки пользователя
    users = await get_users_with_habits()
    user_data = next((u for u in users if u["user_id"] == user_id), None)

    if not user_data:
        logger.warning(f"⚠️ Пользователь {user_id} не найден или не имеет привычек")
        return False

    return await send_reminder_to_user(
        user_id,
        user_data["habits"],
        chat_id or user_data["chat_id"]
    )


async def run_reminder_now() -> Dict[str, Any]:
    """
    Принудительный запуск рассылки (для тестирования).

    Returns:
        Dict: Результаты рассылки
    """
    logger.info("🧪 Напоминания о выполнении по запросу...")
    return await send_daily_reminders()
