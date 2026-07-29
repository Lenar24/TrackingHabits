import os
import asyncio
import logging
from dotenv import load_dotenv
import httpx
from fastapi import FastAPI, Request, Response
import uvicorn
from datetime import datetime, date

from maxapi import Bot
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Конфигурация
MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://backend:8000")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL не задан в .env файле!")

bot = Bot(token=MAX_BOT_TOKEN)
client = httpx.AsyncClient(timeout=30.0, verify=False)


def format_date(date_str):
    """Форматирует дату в ДД-ММ-ГГГГ"""
    if not date_str:
        return None
    try:
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            dt = date_str
        return dt.strftime('%d-%m-%Y')
    except:
        return str(date_str)


def create_main_keyboard():
    """Создает главную клавиатуру (меню)"""
    builder = InlineKeyboardBuilder()
    builder.add(
        {"type": "callback", "text": "📋 Мои привычки", "payload": "my_habits"},
        {"type": "callback", "text": "➕ Добавить привычку", "payload": "add_habit"},
        {"type": "callback", "text": "✅ Отметить выполнение", "payload": "mark_complete"},
        {"type": "callback", "text": "🏁 Завершить привычку", "payload": "complete_early"},
        {"type": "callback", "text": "📊 Статистика", "payload": "stats"}
    )
    builder.adjust(1)
    return [builder.as_markup()]


def create_habit_keyboard(habit_id: int, habit_name: str):
    """Создает клавиатуру для управления конкретной привычкой"""
    builder = InlineKeyboardBuilder()
    builder.add(
        {"type": "callback", "text": "✅ Выполнено", "payload": f"complete_{habit_id}"},
        {"type": "callback", "text": "❌ Пропустить", "payload": f"skip_{habit_id}"},
        {"type": "callback", "text": "🏁 Завершить досрочно", "payload": f"finish_{habit_id}"}
    )
    builder.adjust(1)
    return [builder.as_markup()]


async def send_welcome(chat_id):
    """Отправляет приветственное сообщение с кнопками"""
    await bot.send_message(
        chat_id=chat_id,
        text=(
            "🌟 Добро пожаловать в Трекер привычек!\n\n"
            "Я помогу вам:\n"
            "✅ Отслеживать ежедневные привычки\n"
            "📊 Видеть прогресс\n"
            "⏰ Напоминать о задачах\n\n"
            "Выберите действие в меню ниже:"
        ),
        attachments=create_main_keyboard()
    )


async def send_habit_list(chat_id: int, user_id: int, username: str = None, active_only: bool = True):
    """Показывает список привычек с подробной информацией"""
    url = f"{API_URL}/habits/{user_id}"
    if not active_only:
        url = f"{API_URL}/habits/{user_id}/all"
    response = await client.get(url)

    if response.status_code != 200:
        await bot.send_message(
            chat_id=chat_id,
            text="❌ Не удалось получить список привычек. Попробуйте позже.",
            attachments=create_main_keyboard()
        )
        return

    habits = response.json()

    if not habits:
        text = "📋 У вас пока нет привычек.\n\nНажмите «➕ Добавить привычку», чтобы создать первую!"
        await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())
        return

    username_text = f"👤 {username}" if username else ""
    text = f"📋 **Ваши привычки** {username_text}:\n\n"

    for i, habit in enumerate(habits, 1):
        name = habit.get('name', 'Без названия')
        days = habit.get('days_completed', 0)
        max_days = habit.get('max_days', 21)
        is_active = habit.get('is_active', True)

        if is_active:
            status_emoji = "✅" if days > 0 else "⏳"
            status_text = "активна" if days > 0 else "ожидает начала"
        else:
            status_emoji = "🏁"
            status_text = "завершена"

        progress = min(int((days / max_days) * 20), 20)
        bar = "█" * progress + "░" * (20 - progress)

        text += f"{i}. **{name}**\n"
        text += f"   Статус: {status_emoji} {status_text}\n"
        text += f"   Прогресс: {days}/{max_days} дней\n"
        text += f"   [{bar}] {int((days / max_days) * 100)}%\n"
        text += "\n"

    text += "\n💡 **Управление привычками:**\n"
    text += "• Нажмите «✅ Отметить выполнение» для отметки сегодня\n"
    text += "• Нажмите «🏁 Завершить привычку» для досрочного завершения"

    await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())


async def send_complete_habits_list(chat_id: int, user_id: int, action_type: str):
    """Показывает список привычек для выполнения действия"""
    response = await client.get(f"{API_URL}/habits/{user_id}")
    if response.status_code != 200:
        await bot.send_message(
            chat_id=chat_id,
            text="❌ Не удалось получить список привычек.",
            attachments=create_main_keyboard()
        )
        return

    habits = response.json()
    active_habits = [h for h in habits if h.get("is_active", True)]

    if not active_habits:
        text = "📋 У вас нет активных привычек для управления.\n\n"
        if action_type == 'complete':
            text += "Добавьте новую привычку через «➕ Добавить привычку»"
        else:
            text += "Все привычки уже завершены или ещё не созданы"
        await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())
        return

    if action_type == 'complete':
        title = "✅ **Отметить выполнение привычки**"
        hint = "Выберите привычку, которую хотите отметить сегодня:"
    else:
        title = "🏁 **Завершить привычку досрочно**"
        hint = "Выберите привычку, которую хотите завершить (даже если 21 день не прошёл):"

    text = f"{title}\n\n{hint}\n\n"
    for habit in active_habits:
        name = habit.get('name', 'Без названия')
        days = habit.get('days_completed', 0)
        max_days = habit.get('max_days', 21)
        text += f"📌 **{name}**\n"
        text += f"   Прогресс: {days}/{max_days} дней\n\n"

    await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())

    for habit in active_habits:
        habit_id = habit.get('id')
        name = habit.get('name', 'Без названия')
        days = habit.get('days_completed', 0)
        max_days = habit.get('max_days', 21)

        text = f"📌 **{name}**\n"
        text += f"📊 Прогресс: {days}/{max_days} дней\n"
        if action_type == 'complete':
            text += "\n✅ Отметить как выполненную сегодня?\n"
            text += "❌ Или пропустить сегодняшний день?"
        else:
            text += "\n🏁 Завершить привычку досрочно?"

        await bot.send_message(
            chat_id=chat_id,
            text=text,
            attachments=create_habit_keyboard(habit_id, name)
        )


async def send_statistics(chat_id: int, user_id: int, username: str = None):
    """Отправляет подробную статистику по привычкам"""
    response = await client.get(f"{API_URL}/habits/{user_id}/stats")
    if response.status_code != 200:
        await bot.send_message(
            chat_id=chat_id,
            text="❌ Не удалось получить статистику. Попробуйте позже.",
            attachments=create_main_keyboard()
        )
        return

    stats = response.json()

    if not stats:
        text = "📊 У вас пока нет привычек для статистики.\n\n"
        text += "Нажмите «➕ Добавить привычку», чтобы начать!"
        await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())
        return

    username_text = f"👤 {username}" if username else ""
    text = f"📊 **Ваша статистика** {username_text}:\n\n"

    total_habits = len(stats)
    completed_habits = sum(1 for h in stats if not h.get('is_active', True))
    active_habits = total_habits - completed_habits

    text += f"📌 **Всего привычек:** {total_habits}\n"
    text += f"✅ **Активных:** {active_habits}\n"
    text += f"🏁 **Завершено:** {completed_habits}\n"
    text += "\n\n"

    for habit in stats:
        name = habit.get('name', 'Без названия')
        is_active = habit.get('is_active', True)
        days = habit.get('days_completed', 0)
        max_days = habit.get('max_days', 21)
        best_streak = habit.get('best_streak', 0)
        completed_logs = habit.get('completed_logs', 0)
        total_logs = habit.get('total_logs', 0)

        if is_active:
            status = "✅ Активна"
        else:
            status = "🏁 Завершена"

        text += f"📌 **{name}**\n"
        text += f"   Статус: {status}\n"
        text += f"   Прогресс: {days}/{max_days} дней\n"
        text += f"   🔥 Лучшая серия: {best_streak} дней\n"

        if total_logs > 0:
            percent = int((completed_logs / total_logs) * 100)
            text += f"   📈 Эффективность: {percent}% ({completed_logs}/{total_logs})\n"

        last_7 = habit.get('last_7_days', [])
        if last_7:
            week_display = ""
            for day in last_7[:7]:
                if day.get('completed'):
                    week_display += "✅"
                else:
                    week_display += "⬜"
            text += f"   📅 Неделя: {week_display}\n"

        text += "\n"

    text += "\n💡 **Советы:**\n"
    if active_habits > 0:
        text += f"• У вас {active_habits} активных привычек. Продолжайте в том же духе! 💪\n"
    if completed_habits > 0:
        text += f"• Вы уже сформировали {completed_habits} привычек! 🎉\n"
    if active_habits == 0 and completed_habits > 0:
        text += "• Добавьте новую привычку для продолжения пути! 🚀\n"

    await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())


async def get_habit_name(habit_id: int):
    """Получает название привычки по ID"""
    response = await client.get(f"{API_URL}/habits/item/{habit_id}")
    if response.status_code == 200:
        habit = response.json()
        return habit.get('name', 'Без названия')
    return None


async def get_user_name(user_id: int):
    """Получает имя пользователя"""
    response = await client.get(f"{API_URL}/users/{user_id}")
    if response.status_code == 200:
        user = response.json()
        return user.get('username', 'Пользователь')
    return None


async def handle_habit_action(chat_id: int, user_id: int, payload: str):
    """Обрабатывает действия с привычками с подробной информацией"""
    action, habit_id = payload.split('_')
    habit_id = int(habit_id)

    habit_name = await get_habit_name(habit_id)
    if not habit_name:
        await bot.send_message(
            chat_id=chat_id,
            text="❌ Не удалось найти привычку. Возможно, она была удалена.",
            attachments=create_main_keyboard()
        )
        return

    username = await get_user_name(user_id) or "Пользователь"

    # Проверяем, активна ли привычка
    current_habit = await client.get(f"{API_URL}/habits/item/{habit_id}")
    if current_habit.status_code != 200:
        await bot.send_message(
            chat_id=chat_id,
            text=f"❌ Не удалось найти привычку **{habit_name}**.",
            attachments=create_main_keyboard()
        )
        return

    is_active = current_habit.json().get('is_active', True)

    if not is_active:
        await bot.send_message(
            chat_id=chat_id,
            text=f"ℹ️ Привычка **{habit_name}** уже завершена. Это действие недоступно.",
            attachments=create_main_keyboard()
        )
        return

    if action == "complete":
        old_days = current_habit.json().get('days_completed', 0)

        response = await client.post(f"{API_URL}/habits/{habit_id}/complete")
        if response.status_code == 200:
            habit = response.json()
            days = habit.get('days_completed', 0)
            max_days = habit.get('max_days', 21)
            is_completed = not habit.get('is_active', True)
            last_completed = habit.get('last_completed')

            if days > old_days:
                text = f"✅ **Привычка выполнена!**\n\n"
                text += f"📌 Привычка: **{habit_name}**\n"
                text += f"👤 Отметил(а): {username}\n"
                text += f"📊 Прогресс: {days}/{max_days} дней\n"
                if is_completed:
                    completed_at = habit.get('completed_at')
                    formatted_date = format_date(completed_at) or "сегодня"
                    text += f"📅 Завершена: {formatted_date}\n"
                    text += f"🎉 **Поздравляю! Привычка сформирована через {max_days} дней!** 🏁"
                else:
                    text += f"💪 Осталось: {max_days - days} дней до цели"
            else:
                text = f"ℹ️ **Привычка уже отмечена сегодня!**\n\n"
                text += f"📌 Привычка: **{habit_name}**\n"
                text += f"📊 Текущий прогресс: {days}/{max_days} дней\n"
                text += f"📅 Отмечена: сегодня\n\n"
                text += "💡 Возвращайтесь завтра, чтобы продолжить!"

            await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=f"❌ Не удалось отметить привычку **{habit_name}**. Попробуйте позже.",
                attachments=create_main_keyboard()
            )

    elif action == "skip":
        response = await client.post(f"{API_URL}/habits/{habit_id}/skip")
        if response.status_code == 200:
            habit = response.json()
            days = habit.get('days_completed', 0)

            text = f"❌ **Привычка пропущена**\n\n"
            text += f"📌 Привычка: **{habit_name}**\n"
            text += f"👤 Пропустил(а): {username}\n"
            text += f"📊 Прогресс сброшен до {days} дней\n\n"
            text += "💡 Счётчик дней обнулён. Вы можете начать заново в любой день!"

            await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=f"❌ Не удалось пропустить привычку **{habit_name}**.",
                attachments=create_main_keyboard()
            )

    elif action == "finish":
        was_active = current_habit.json().get('is_active', True)
        was_completed_early = current_habit.json().get('completed_early', False)

        response = await client.post(f"{API_URL}/habits/{habit_id}/complete-early")
        if response.status_code == 200:
            habit = response.json()
            days = habit.get('days_completed', 0)
            max_days = habit.get('max_days', 21)
            is_active = habit.get('is_active', True)
            completed_at = habit.get('completed_at')
            completed_early = habit.get('completed_early', False)

            if was_active:
                text = f"🏁 **Привычка завершена досрочно!**\n\n"
                text += f"📌 Привычка: **{habit_name}**\n"
                text += f"👤 Завершил(а): {username}\n"
                text += f"📊 Прогресс: {days}/{max_days} дней\n\n"
                text += "🎉 **Отличная работа!** Вы решили, что привычка сформирована раньше срока!"
            else:
                formatted_date = format_date(completed_at) or "ранее"
                if completed_early:
                    text = f"ℹ️ **Привычка уже завершена досрочно**\n\n"
                    text += f"📌 Привычка: **{habit_name}**\n"
                    text += f"📊 Прогресс: {days}/{max_days} дней\n"
                    text += f"📅 Завершена: {formatted_date}\n\n"
                    text += "🏁 Привычка уже сформирована. Отличная работа!"
                else:
                    text = f"🎉 **Привычка сформирована за 21 день!**\n\n"
                    text += f"📌 Привычка: **{habit_name}**\n"
                    text += f"📊 Прогресс: {days}/{max_days} дней\n"
                    text += f"📅 Завершена: {formatted_date}\n\n"
                    text += "🌟 Отличная работа! Привычка успешно сформирована!"

            await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=f"❌ Не удалось завершить привычку **{habit_name}**.",
                attachments=create_main_keyboard()
            )


# ============================================
# ОБРАБОТЧИКИ СОБЫТИЙ
# ============================================

async def get_or_create_user(user_id: int, username: str = None, chat_id: int = None):
    """Получить или создать пользователя в БД"""
    response = await client.get(f"{API_URL}/users/{user_id}")
    if response.status_code == 200:
        user_data = response.json()
        if chat_id and user_data.get('chat_id') != chat_id:
            await client.put(
                f"{API_URL}/users/{user_id}/chat_id",
                json={"chat_id": chat_id}
            )
        return user_data

    response = await client.post(
        f"{API_URL}/users/",
        json={"user_id": user_id, "username": username, "chat_id": chat_id}
    )
    if response.status_code == 200:
        return response.json()

    logger.error(f"❌ Ошибка создания пользователя: {response.text}")
    return None


async def handle_bot_started(update_data: dict):
    try:
        chat_id = update_data.get('chat_id')
        user_id = update_data.get('user_id')
        logger.info(f"✅ Событие bot_started: chat_id={chat_id}")
        await get_or_create_user(user_id, None, chat_id)
        await send_welcome(chat_id)
    except Exception as e:
        logger.error(f"❌ Ошибка в bot_started: {e}")


async def handle_message_created(update_data: dict):
    try:
        message_data = update_data.get('message')
        if not message_data:
            return

        chat_id = message_data.get('recipient', {}).get('chat_id')
        user_id = message_data.get('sender', {}).get('user_id')
        username = message_data.get('sender', {}).get('first_name')
        text = message_data.get('body', {}).get('text')

        logger.info(f"📩 Получено сообщение от {user_id} в чат {chat_id}")

        if not chat_id or not user_id:
            logger.warning("⚠️ Не удалось получить chat_id или user_id")
            return

        user = await get_or_create_user(user_id, username, chat_id)

        if not text:
            return

        logger.info(f"💬 Текст: {text}")

        if text.lower() in ["начать", "/start", "start"]:
            await send_welcome(chat_id)
            return

        if text.startswith('/'):
            return

        response = await client.post(
            f"{API_URL}/habits/",
            json={"user_id": user_id, "name": text}
        )

        if response.status_code == 200:
            habit = response.json()
            days = habit.get('days_completed', 0)
            max_days = habit.get('max_days', 21)

            text_msg = f"✅ **Привычка добавлена!**\n\n"
            text_msg += f"📌 Название: **{text}**\n"
            text_msg += f"👤 Владелец: {username or 'Пользователь'}\n"
            text_msg += f"🎯 Цель: {max_days} дней\n"
            text_msg += f"📊 Текущий прогресс: {days}/{max_days} дней\n\n"
            text_msg += "💡 Отмечайте выполнение каждый день через меню!"

            await bot.send_message(chat_id=chat_id, text=text_msg, attachments=create_main_keyboard())
        else:
            await bot.send_message(
                chat_id=chat_id,
                text="❌ Не удалось добавить привычку. Возможно, она уже существует.",
                attachments=create_main_keyboard()
            )
    except Exception as e:
        logger.error(f"❌ Ошибка в message_created: {e}")


async def handle_message_callback(update_data: dict):
    try:
        callback = update_data.get('callback')
        if not callback:
            return

        payload = callback.get('payload')
        user_id = callback.get('user', {}).get('user_id')
        message = update_data.get('message', {})
        chat_id = message.get('recipient', {}).get('chat_id')
        username = callback.get('user', {}).get('first_name')

        logger.info(f"🔘 Получен callback: {payload}")

        if not chat_id or not user_id:
            return

        await get_or_create_user(user_id, None, chat_id)

        if payload == "my_habits":
            await send_habit_list(chat_id, user_id, username, active_only=True)

        elif payload == "add_habit":
            text = "✏️ **Введите название новой привычки:**\n\n"
            text += "Например: «Читать 30 минут» или «Заниматься спортом»\n\n"
            text += "💡 Цель будет автоматически установлена на 21 день."
            await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())

        elif payload == "mark_complete":
            await send_complete_habits_list(chat_id, user_id, 'complete')

        elif payload == "complete_early":
            await send_complete_habits_list(chat_id, user_id, 'finish')

        elif payload == "stats":
            await send_statistics(chat_id, user_id, username)

        elif payload.startswith("complete_") or payload.startswith("skip_") or payload.startswith("finish_"):
            await handle_habit_action(chat_id, user_id, payload)

        else:
            logger.warning(f"⚠️ Неизвестный callback: {payload}")

    except Exception as e:
        logger.error(f"❌ Ошибка в message_callback: {e}")


# ============================================
# FASTAPI ПРИЛОЖЕНИЕ
# ============================================

app = FastAPI(title="Habit Tracker Bot Webhook")


@app.post("/webhook")
async def webhook(request: Request):
    try:
        update_data = await request.json()
        update_type = update_data.get('update_type')
        logger.info(f"📨 Получен вебхук: {update_type}")

        if update_type == 'message_created':
            await handle_message_created(update_data)
        elif update_type == 'message_callback':
            await handle_message_callback(update_data)
        elif update_type == 'bot_started':
            await handle_bot_started(update_data)
        else:
            logger.warning(f"⚠️ Неизвестный тип обновления: {update_type}")

        return Response(status_code=200)
    except Exception as e:
        logger.error(f"❌ Ошибка обработки вебхука: {e}")
        import traceback
        traceback.print_exc()
        return Response(status_code=500)


@app.get("/health")
async def health():
    return {"status": "ok"}


# ============================================
# ЗАПУСК
# ============================================

async def set_webhook():
    url = "https://platform-api2.max.ru/subscriptions"
    headers = {
        "Authorization": f"{MAX_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "url": f"{WEBHOOK_URL}",
        "events": ["message_created", "message_callback", "bot_started"]
    }

    async with httpx.AsyncClient(verify=False) as webhook_client:
        response = await webhook_client.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            logger.info(f"✅ Вебхук установлен: {WEBHOOK_URL}")
        else:
            logger.error(f"❌ Ошибка установки вебхука: {response.text}")


async def main():
    await set_webhook()
    print("🚀 Бот запущен с Webhook!")
    print(f"📡 Webhook URL: {WEBHOOK_URL}")
    config = uvicorn.Config(app, host="0.0.0.0", port=8001, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
