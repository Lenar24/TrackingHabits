# 🏆 Чат-бот на платформе MAX **Трекер привычек**

---

<div align="center">

[![CI - Code Check](https://github.com/Lenar24/TrackingHabits/actions/workflows/ci.yml/badge.svg)](https://github.com/Lenar24/TrackingHabits/actions/workflows/ci.yml)
[![Pylint](https://img.shields.io/badge/pylint-10.00%2F10-brightgreen)](https://github.com/Lenar24/TrackingHabits)
[![Mypy](https://img.shields.io/badge/mypy-passing-brightgreen)](https://github.com/Lenar24/TrackingHabits)
[![Tests](https://img.shields.io/badge/tests-59%20passed-brightgreen)](https://github.com/Lenar24/TrackingHabits)
[![Coverage](https://img.shields.io/badge/coverage-46%25-yellowgreen)](https://github.com/Lenar24/TrackingHabits)
[![Python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.13-green)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-ready-blue)](https://www.docker.com)
[![MAX Platform](https://img.shields.io/badge/MAX-Platform-orange)](https://max.ru)

**Чат-бот для трекинга привычек по методу 21 дня на платформе MAX**

[Демо бота в MAX](https://max.ru/se13645210_bot) • [Документация API](#-api-документация) • [Установка](#-установка)

</div>

---

## 📖 Оглавление:

- [О проекте](#-о-проекте)
- [Скриншоты](#-скриншоты)
- [Технологии](#-технологии)
- [Архитектура](#-архитектура)
- [Установка](#-установка)
- [Запуск](#-запуск)
- [API Документация](#-api-документация)
- [Эндпоинты](#-эндпоинты)
- [Работа с ботом](#-работа-с-ботом)
- [Тестирование](#-тестирование)
- [CI/CD](#-cicd)
- [Структура проекта](#-структура-проекта)
- [Подробное описание работы бота и приложения](#-подробное-описание-работы-бота-и-приложения)
- [Backend и база данных](#-backend-и-база-данных)
- [Безопасность и надёжность](#-безопасность-и-надёжность)
- [Вклад в проект](#-вклад-в-проект)
- [Лицензия](#-лицензия)
- [Контакты](#-контакты)
- [Благодарности](#-благодарности)

---

## 📱 О проекте

Чат-бот **Трекер привычек** — это чат-бот для платформы **MAX**, 
который помогает пользователям формировать полезные привычки по методу "21 день". 
Бот интегрируется с MAX через API MAX и предоставляет удобный интерфейс 
для отслеживания прогресса.

### 🌟 Основные возможности:

| Функция                     | Описание                                 |
|-----------------------------|------------------------------------------|
| 📋 **Создание привычек**    | Добавление привычек с описанием          |
| ✅ **Ежедневное выполнение** | Отметка выполнения привычек              |
| 📊 **Статистика**           | Визуализация прогресса и серий           |
| 🔥 **Серии (стрики)**       | Отслеживание непрерывных дней выполнения |
| 🏁 **Правило 21 дня**       | Автоматическое завершение привычки       |
| ⏰ **Напоминания**           | Ежедневные уведомления (9:00 и 21:00)    |
| 🎯 **Досрочное завершение** | Возможность завершить привычку раньше    |
| 🔐 **JWT аутентификация**   | Безопасный доступ к API                  |

---

## 📸 Скриншоты

### Описание бота, ссылка приглашение, QR-код:

<div align="center">
  <img src="screenshots/Чат-бот.jpg" width="250"/>
  <p><i>Страница с описанием.</i></p>
</div>

<div align="center">
  <img src="screenshots/Ссылка приглашение.jpg" width="250"/>
  <p><i>Ссылка приглашение.</i></p>
</div>

<div align="center">
  <img src="screenshots/QR-код.jpg" width="250"/>
  <p><i>QR-код.</i></p>
</div>

### Титульная и стартовая страницы бота:

<div align="center">
  <img src="screenshots/Титульная страница.jpg" width="250"/>
  <p><i>Титульная страница.</i></p>
</div>

<div align="center">
  <img src="screenshots/Стартовая страница.jpg" width="250"/>
  <p><i>Стартовая страница.</i></p>
</div>

### Мои привычки:

<div align="center">
  <img src="screenshots/Мои привычки.jpg" width="250"/>
  <p><i>Мои привычки.</i></p>
</div>

### Добавить привычку:

<div align="center">
  <img src="screenshots/Добавить привычку. Шаг 1.jpg" width="250"/>
  <p><i>Добавить привычку. Шаг 1.</i></p>
</div>

<div align="center">
  <img src="screenshots/Добавить привычку. Шаг 2.jpg" width="250"/>
  <p><i>Добавить привычку. Шаг 2.</i></p>
</div>

<div align="center">
  <img src="screenshots/Добавить привычку. Шаг 3.jpg" width="250"/>
  <p><i>Добавить привычку. Шаг 3.</i></p>
</div>

### Отметка выполнения привычки сегодня:

<div align="center">
  <img src="screenshots/Выполнение привычки.jpg" width="250"/>
  <p><i>Выполнение привычки.</i></p>
</div>

<div align="center">
  <img src="screenshots/Привычка уже отмечена сегодня.jpg" width="250"/>
  <p><i>Привычка уже отмечена сегодня.</i></p>
</div>

### Пропуск отметки привычки:

<div align="center">
  <img src="screenshots/Пропуск привычки.jpg" width="250"/>
  <p><i>Пропуск привычки.</i></p>
</div>

### Завершить привычку досрочно:

<div align="center">
  <img src="screenshots/Завершить привычку досрочно. Шаг 1.jpg" width="250"/>
  <p><i>Завершить привычку досрочно. Шаг 1.</i></p>
</div>

<div align="center">
  <img src="screenshots/Завершить привычку досрочно. Шаг 2.jpg" width="250"/>
  <p><i>Завершить привычку досрочно. Шаг 2.</i></p>
</div>

### Статистика:

<div align="center">
  <img src="screenshots/Статистика. Начало.jpg" width="250"/>
  <p><i>Статистика. Начало.</i></p>
</div>

<div align="center">
  <img src="screenshots/Статистика. Конец.jpg" width="250"/>
  <p><i>Статистика. Конец.</i></p>
</div>

### Ежедневные напоминания:

<div align="center">
  <img src="screenshots/Напоминания.jpg" width="250"/>
  <p><i>Напоминания в 09:00 и 21:00 часов по Московскому времени.</i></p>
</div>

---

## 🛠 Технологии

### Backend
| Технология      | Версия   | Назначение            |
|-----------------|----------|-----------------------|
| **Python**      | 3.13     | Язык программирования |
| **FastAPI**     | 0.115.13 | Веб-фреймворк для API |
| **SQLAlchemy**  | 2.0      | ORM для работы с БД   |
| **PostgreSQL**  | 15       | Основная база данных  |
| **Alembic**     | 1.12     | Миграции базы данных  |
| **APScheduler** | 3.10     | Планировщик задач     |
| **Pydantic**    | 2.0      | Валидация данных      |
| **python-jose** | 3.3      | JWT токены            |

### Bot (MAX Платформа)
| Технология  | Версия   | Назначение                 |
|-------------|----------|----------------------------|
| **MAX API** | 1.2.1    | Платформа для чат-ботов    |
| **httpx**   | 0.27     | Асинхронный HTTP клиент    |
| **Uvicorn** | 0.34     | ASGI сервер                |
| **FastAPI** | 0.115.13 | Веб-фреймворк для вебхуков |
| **SQLite**  | -        | Хранение JWT токенов       |

### Инструменты
| Инструмент | Версия | Назначение               |
|------------|--------|--------------------------|
| **Poetry** | -      | Управление зависимостями |
| **Docker** | -      | Контейнеризация          |
| **Pytest** | 8.4    | Тестирование             |
| **Pylint** | 3.3    | Качество кода            |
| **Mypy**   | 1.20   | Типизация                |
| **Black**  | 24.10  | Форматирование           |
| **Isort**  | 5.13   | Сортировка импортов      |

### Основные зависимости (Poetry)

Управление зависимостями осуществляется через **Poetry**.<br> 
Все зависимости описаны в `pyproject.toml`.

| Категория         | Пакеты                                       |
|-------------------|----------------------------------------------|
| **Web-фреймворк** | FastAPI 0.115.13, Uvicorn 0.34.0             |
| **База данных**   | SQLAlchemy 2.0, Alembic 1.12, asyncpg 0.30.0 |
| **Валидация**     | Pydantic 2.0, pydantic-settings              |
| **Безопасность**  | python-jose 3.3, passlib 1.7, bcrypt 4.2     |
| **Бот**           | maxapi 1.2.1, httpx 0.27                     |
| **Планировщик**   | APScheduler 3.10                             |
| **Retry**         | tenacity 8.5                                 |
| **Утилиты**       | python-dotenv 1.0, pytz 2024.1               |

### Dev-зависимости

| Инструмент     | Версия | Назначение               |
|----------------|--------|--------------------------|
| **Pytest**     | 8.4    | Тестирование             |
| **Pylint**     | 3.3    | Качество кода            |
| **Mypy**       | 1.20   | Типизация                |
| **Black**      | 24.10  | Форматирование           |
| **Isort**      | 5.13   | Сортировка импортов      |
| **pytest-cov** | 4.1    | Покрытие кода            |
| **freezegun**  | 1.5    | Мокирование времени      |

### Установка Poetry

```
# Установка Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Установка зависимостей:

# Все зависимости
poetry install --with dev

# Только основные
poetry install --no-dev

# Проверка
poetry --version

# Настройка виртуального окружения
poetry config virtualenvs.in-project true
```
---

## 🏗 Архитектура

```mermaid
flowchart TB
    subgraph MAX["MAX Platform"]
        MAX1["API для чат-ботов"]
    end
    
    MAX -->|"Webhook (POST /webhook)"| BOT
    
    subgraph BOT["Bot (FastAPI) — порт 8001"]
        direction LR
        B1["Handlers<br/>(message, callback, command)"]
        B2["Keyboards<br/>(inline keyboards)"]
        B3["HabitService<br/>(client для backend API)"]
        B4["AuthService<br/>(JWT)"]
        B5["TokenDB<br/>(SQLite)"]
    end
    
    BOT -->|"HTTP API (JSON + JWT)"| BACKEND
    
    subgraph BACKEND["Backend (FastAPI) — порт 8000"]
        direction LR
        C1["API Routes<br/>(auth, habits, users, stats)"]
        C2["Services<br/>(Business Logic)"]
        C3["Models<br/>(SQLAlchemy)"]
    end
    
    BACKEND --> |"SQL"| DB[("PostgreSQL<br/>habit_tracker")]
    
    DB --> TABLES["users, habits, habit_logs"]
    
    style MAX fill:#f9f,stroke:#333,stroke-width:2px,color:#fff
    style BOT fill:#bbf,stroke:#333,stroke-width:2px,color:#fff
    style BACKEND fill:#bfb,stroke:#333,stroke-width:2px
    style DB fill:#fbb,stroke:#333,stroke-width:2px
    style TABLES fill:#eee,stroke:#333,stroke-width:1px
```

---

## 🚀 Установка

### Требования:

* Python 3.13+
* Docker и Docker Compose
* Poetry (для управления зависимостями)
* PostgreSQL (для локальной разработки)
* Аккаунт на платформе MAX
* Cloudflare Tunnel, ngrok или serveo.net (для вебхуков)

1. Клонирование репозитория
```
git clone https://github.com/Lenar24/TrackingHabits.git
cd TrackingHabits
```

2. Установка зависимостей
```
# Установить все зависимости (основные + dev)
poetry install --with dev

# Или только основные
poetry install --no-dev
```

3. Настройка переменных окружения
```
# Создать .env файл
cp .env.example .env

# Отредактировать .env
nano .env
.env.example:

env
# ============================================
# ENVIRONMENT
# ============================================
ENVIRONMENT=development
DEBUG=True

# ============================================
# DATABASE (PostgreSQL)
# ============================================
# Для локальной разработки: localhost
# Для Docker: db
DATABASE_URL=postgresql://postgresql:postgresql@localhost:5432/habit_tracker
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# ============================================
# JWT
# ============================================
# Сгенерировать: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-secret-key-here-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ============================================
# BOT (MAX Messenger)
# ============================================
MAX_BOT_TOKEN=your-max-bot-token-here
API_URL=http://backend:8000
WEBHOOK_URL=https://your-domain.com/webhook
BOT_PORT=8001
BOT_WORKERS=4
TOKEN_DB_PATH=bot_tokens.db

# ============================================
# LOGGING
# ============================================
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE=logs/app.log

# ============================================
# CORS
# ============================================
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*

# ============================================
# SECURITY
# ============================================
ALLOWED_HOSTS=localhost,127.0.0.1

# ============================================
# DOCKER (PostgreSQL)
# ============================================
POSTGRES_USER=postgresql
POSTGRES_PASSWORD=postgresql
POSTGRES_DB=habit_tracker
```

4. Получение токена бота в MAX
```
1. Зарегистрируйтесь на платформе MAX.
2. Создайте нового бота в личном кабинете.
3. Получите токен бота.
4. Добавьте токен в .env как MAX_BOT_TOKEN.
```

5. Настройка вебхука<br>
Для разработки (через Cloudflare Tunnel):
```
# Скачать cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

# Установить
sudo dpkg -i cloudflared-linux-amd64.deb

# Запустить туннель
cloudflared tunnel --url http://localhost:8001 --protocol http2

# Скопировать URL (например, https://xxx.trycloudflare.com)
# Добавить в WEBHOOK_URL с /webhook
WEBHOOK_URL=https://xxx.trycloudflare.com/webhook

Для продакшена:
env
WEBHOOK_URL=https://your-domain.com/webhook
```
---

## 🐳 Запуск

### Docker Compose (рекомендуется)
```
# Запуск всех сервисов
docker compose up -d

# Просмотр логов
docker compose logs -f

# Остановка
docker compose down

# Пересборка с обновлением
docker compose up -d --build
```

### Локальный запуск

Терминал 1: PostgreSQL
```
cd TrackingHabits
docker compose up -d db
```

Терминал 2: Backend
```
cd backend
export DATABASE_URL=postgresql://postgresql:postgresql@localhost:5432/habit_tracker
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Терминал 3: Cloudflare Tunnel
```
cloudflared tunnel --url http://localhost:8001 --protocol http2
```

Терминал 4: Bot
```
cd bot
export API_URL=http://localhost:8000
python -m bot.main
```
---

## 📚 API Документация

После запуска backend доступна интерактивная документация:

| URL	                                    | Описание             |
|-----------------------------------------|----------------------|
| http://localhost:8000/api/docs	         | Swagger UI           |
| http://localhost:8000/api/redoc	        | ReDoc                |
| http://localhost:8000/api/openapi.json	 | OpenAPI спецификация |
---

## 🗺 Эндпоинты

### 🔐 Аутентификация (/api/v1/auth):

| Метод	 | Эндпоинт	             | Описание             |
|--------|-----------------------|----------------------|
| POST	  | /api/v1/auth/login	   | Логин (JWT)          |
| POST	  | /api/v1/auth/refresh	 | Обновление токена    |
| GET	   | /api/v1/auth/me	      | Текущий пользователь |
| POST	  | /api/v1/auth/logout	  | Выход                |

### 👥 Пользователи (/api/v1/users):

| Метод  | 	Эндпоинт                 | 	Описание                 |
|--------|---------------------------|---------------------------|
| GET    | 	/api/v1/users/           | 	Все пользователи (админ) |
| GET    | 	/api/v1/users/me         | 	Текущий пользователь     |
| GET    | 	/api/v1/users/{user_id}  | 	Пользователь по ID       |
| PUT    | 	/api/v1/users/{user_id}  | 	Обновление пользователя  |
| PUT    | 	/api/v1/users/me/chat-id | 	Обновление chat_id       |
| DELETE | 	/api/v1/users/{user_id}  | 	Удаление (админ)         |

### 📋 Привычки (/api/v1/habits):

| Метод  | 	Эндпоинт                                 | 	Описание             |
|--------|-------------------------------------------|-----------------------|
| POST   | 	/api/v1/habits/                          | 	Создание привычки    |
| GET    | 	/api/v1/habits/                          | 	Список привычек      |
| GET    | 	/api/v1/habits/{habit_id}                | 	Привычка по ID       |
| PUT    | 	/api/v1/habits/{habit_id}                | 	Обновление           |
| DELETE | 	/api/v1/habits/{habit_id}                | 	Удаление             |
| POST   | 	/api/v1/habits/{habit_id}/complete       | 	Отметка выполнения   |
| POST   | 	/api/v1/habits/{habit_id}/skip           | 	Пропуск              |
| POST   | 	/api/v1/habits/{habit_id}/complete-early | 	Досрочное завершение |
| POST   | 	/api/v1/habits/{habit_id}/reset          | 	Сброс прогресса      |
| POST   | 	/api/v1/habits/{habit_id}/activate       | 	Активация            |
| GET    | 	/api/v1/habits/{habit_id}/progress       | 	Прогресс             |
| GET    | 	/api/v1/habits/{habit_id}/streak         | 	Стрик                |
| POST   | 	/api/v1/habits/check-21-days             | 	Проверка 21 дня      |

### 📊 Статистика (/api/v1/stats):

| Метод | 	Эндпоинт                                 | 	Описание           |
|-------|-------------------------------------------|---------------------|
| GET   | 	/api/v1/stats/overall                    | 	Общая статистика   |
| GET   | 	/api/v1/stats/habits/{habit_id}	         | Статистика привычки |
| GET   | 	/api/v1/stats/habits/{habit_id}/progress | 	Прогресс           |
| GET   | 	/api/v1/stats/habits/{habit_id}/history  | 	История            |

### ⏰ Напоминания (/api/v1/reminders):

| Метод | 	Эндпоинт                  | 	Описание                 |
|-------|----------------------------|---------------------------|
| POST  | 	/api/v1/reminders/test    | 	Тест напоминания (админ) |
| POST  | 	/api/v1/reminders/run-now | 	Запуск рассылки (админ)  |

### Примеры запросов:

Логин и получение токена
```
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"max_user_id": 12345, "chat_id": 67890, "username": "john_doe"}'

Ответ:
json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Создание привычки
```
TOKEN="your_access_token"
curl -X POST "http://localhost:8000/api/v1/habits/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Утренняя зарядка", "description": "10 минут"}'
```

Отметка выполнения
```
curl -X POST "http://localhost:8000/api/v1/habits/1/complete" \
  -H "Authorization: Bearer $TOKEN"
```

Получение статистики
```
curl "http://localhost:8000/api/v1/stats/overall" \
  -H "Authorization: Bearer $TOKEN"
```
---

## 🤖 Работа с ботом

### Команды:

| Команда   | 	Описание             |
|-----------|-----------------------|
| /start    | 	Главное меню         |
| /habits   | 	Список привычек      |
| /add      | 	Добавить привычку    |
| /complete | 	Отметить выполнение  |
| /finish   | 	Досрочное завершение |
| /stats    | 	Статистика           |

### Кнопки меню:
```
📋 Мои привычки    
➕ Добавить привычку
✅ Отметить выполнение    
🏁 Завершить привычку
📊 Статистика
```

### Пример диалога:
```
👤 Пользователь: Начать
🤖 Бот: 🌟 Добро пожаловать в Трекер привычек!
Выберите действие в меню ниже:
📋 Мои привычки    
➕ Добавить привычку
✅ Отметить выполнение    
🏁 Завершить привычку
📊 Статистика
```
```
👤 Пользователь: ➕ Добавить привычку
🤖 Бот: ✏️ Введите название новой привычки:
Например: «Читать 30 минут» или «Заниматься спортом»

👤 Пользователь: Утренняя зарядка
🤖 Бот: ✅ Привычка добавлена!

📌 Название: Утренняя зарядка
🎯 Цель: 21 дней
📊 Текущий прогресс: 0/21 дней

💡 Отмечайте выполнение каждый день через меню!
```
```
👤 Пользователь: ✅ Отметить выполнение
🤖 Бот: ✅ **Привычка выполнена!**

📌 Привычка: Утренняя зарядка
📊 Прогресс: 1/21 дней
💪 Осталось: 20 дней до цели
```
---

## 🧪 Тестирование

Запуск тестов
```
# Все тесты
pytest tests/ -v

# С покрытием
pytest tests/ --cov=backend --cov=bot -v

# С HTML отчётом
pytest tests/ --cov=backend --cov=bot --cov-report=html

# Только unit тесты
pytest tests/ -m unit -v

# Только интеграционные
pytest tests/ -m integration -v
```

Результаты тестов
```
============================= 59 passed, 48 warnings in 2.32s ==============================

---------- coverage: platform linux, python 3.13.15-final-0 ----------
Name                                    Stmts   Miss  Cover
---------------------------------------------------------------------
backend/app/api/auth.py                    48      5    90%
backend/app/api/habits.py                  86     24    72%
backend/app/api/stats.py                   37      5    86%
backend/app/api/users.py                   49     20    59%
backend/app/models/habit.py               154     32    79%
backend/app/models/user.py                 12      0   100%
backend/app/schemas/*                      51      0   100%
backend/app/utils/validators.py            22      1    95%
backend/app/core/config.py                 37      0   100%
---------------------------------------------------------------------
TOTAL                                    2433   1323    46%
Покрытие по модулям
Модуль	Покрытие	Статус
Backend API	59-90%	✅
Backend Models	79-100%	✅
Backend Schemas	86-100%	✅
Backend Utils	41-95%	✅
Bot Formatters	60%	✅
Bot Validators	52%	✅
Scheduler	33%	⚠️
```

Проверка качества кода
```
# Проверка типов
poetry run mypy .
# Success: no issues found in 54 source files

# Проверка качества
poetry run pylint .
# Your code has been rated at 10.00/10

# Проверка форматирования
poetry run black --check .
# All done! ✨ 🍰 ✨

# Проверка импортов
poetry run isort --check-only .
# SUCCESS
```
---

## 🔄 CI/CD
GitHub Actions

Проект настроен на автоматическую проверку кода через GitHub Actions.

Что проверяется:
```
✅ Форматирование (Black)
✅ Сортировка импортов (Isort)
✅ Типизация (Mypy)
✅ Качество кода (Pylint)
✅ Тесты (Pytest)
```

.github/workflows/ci.yml:
```
yaml
name: CI - Code Check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgresql
          POSTGRES_PASSWORD: postgresql
          POSTGRES_DB: habit_tracker
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: poetry install
      - run: poetry run black --check .
      - run: poetry run isort --check-only .
      - run: poetry run mypy .
      - run: poetry run pylint .
      - run: poetry run pytest -v
```

Badges статуса:<br>
[![CI - Code Check](https://github.com/Lenar24/TrackingHabits/actions/workflows/ci.yml/badge.svg)](https://github.com/Lenar24/TrackingHabits/actions/workflows/ci.yml)

---

## 📁 Структура проекта
```
TrackingHabits/
├── backend/                     # Backend сервер
│   ├── app/
│   │   ├── api/                 # API эндпоинты
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # JWT аутентификация
│   │   │   ├── dependencies.py  # Общие зависимости
│   │   │   ├── habits.py        # Привычки
│   │   │   ├── reminders.py     # Напоминания
│   │   │   ├── stats.py         # Статистика
│   │   │   └── users.py         # Пользователи
│   │   ├── core/                # Конфигурация
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── logging_config.py
│   │   ├── models/              # SQLAlchemy модели
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── habit.py
│   │   │   ├── habit_log.py
│   │   │   └── user.py
│   │   ├── schemas/             # Pydantic схемы
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── common.py
│   │   │   ├── habit.py
│   │   │   ├── habit_log.py
│   │   │   ├── stats.py
│   │   │   └── user.py
│   │   ├── services/            # Бизнес-логика
│   │   │   ├── __init__.py
│   │   │   ├── habit_service.py
│   │   │   └── user_service.py
│   │   ├── utils/               # Утилиты
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # JWT утилиты
│   │   │   ├── database.py
│   │   │   ├── keyboards.py
│   │   │   └── validators.py
│   │   ├── __init__.py
│   │   ├── main.py              # Точка входа
│   │   └── scheduler.py         # Планировщик
│   └── migrations/              # Alembic миграции
│       ├── env.py
│       ├── __init__.py
│       ├── script.py.mako
│       └── versions/
│           ├── __init__.py
│           └── 0ed0588d5583_initial_migration.py
│
├── bot/                         # Чат-бот (MAX Platform)
│   ├── core/                    # Конфигурация
│   │   ├── __init__.py
│   │   └── config.py
│   ├── handlers/                # Обработчики
│   │   ├── __init__.py
│   │   ├── callback_handlers.py
│   │   ├── command_handlers.py
│   │   └── message_handlers.py
│   ├── keyboards/               # Клавиатуры
│   │   ├── __init__.py
│   │   └── keyboards.py
│   ├── services/                # Клиентские сервисы
│   │   ├── __init__.py
│   │   ├── api_client.py
│   │   ├── auth_service.py
│   │   └── habit_service.py
│   ├── utils/                   # Утилиты бота
│   │   ├── __init__.py
│   │   ├── formatters.py
│   │   ├── messages.py
│   │   └── validators.py
│   ├── __init__.py
│   ├── bot_tokens.db            # SQLite (НЕ в Git)
│   ├── database.py              # TokenDB
│   └── main.py                  # Точка входа
│
├── tests/                       # Тесты (59 тестов)
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_bot.py
│   ├── test_edge_cases.py
│   ├── test_habits.py
│   ├── test_integration.py
│   ├── test_scheduler.py
│   ├── test_stats.py
│   ├── test_users.py
│   └── test_validation.py
│
├── screenshots/                 # 19 скриншотов
│   ├── QR-код.jpg
│   ├── Выполнение привычки.jpg
│   ├── Добавить привычку. Шаг 1.jpg
│   ├── Добавить привычку. Шаг 2.jpg
│   ├── Добавить привычку. Шаг 3.jpg
│   ├── Завершить привычку досрочно. Шаг 1.jpg
│   ├── Завершить привычку досрочно. Шаг 2.jpg
│   ├── Мои привычки.jpg
│   ├── Напоминания.jpg
│   ├── Привычка уже отмечена сегодня.jpg
│   ├── Пропуск привычки.jpg
│   ├── Ссылка приглашение.jpg
│   ├── Стартовая страница.jpg
│   ├── Статистика. Конец.jpg
│   ├── Статистика. Начало.jpg
│   ├── Титульная страница.jpg
│   └── Чат-бот.jpg
│
├── .github/workflows/
│   └── ci.yml                   # CI/CD
├── docker-compose.yml           # Docker Compose
├── Dockerfile                   # Docker для backend
├── Dockerfile.bot               # Docker для bot
├── pyproject.toml               # Poetry конфиг
├── poetry.lock                  # Зависимости
├── mypy.ini                     # Mypy конфиг
├── pytest.ini                   # Pytest конфиг
├── alembic.ini                  # Alembic конфиг
├── .env.example                 # Шаблон переменных
├── .gitignore                   # Git ignore
├── .dockerignore                # Docker ignore
├── LICENSE                      # MIT License
└── README.md                    # Документация
```
---

## 📖 Подробное описание работы бота и приложения

### 🎯 Общее описание
```
Бот **Трекер привычек** — это полноценная система для формирования полезных привычек, 
состоящая из двух основных компонентов: 
MAX-бота (на платформе MAX) и Backend-сервера (FastAPI). 
Бот помогает пользователям отслеживать ежедневные привычки по методу "21 день", 
отправляет напоминания, показывает статистику и автоматически завершает привычки 
при достижении цели.
```

### 🔐 JWT Аутентификация

Все запросы к API защищены JWT токенами:
```
1. Пользователь логинится через /api/v1/auth/login
2. Backend выдаёт access_token и refresh_token
3. Бот сохраняет токены в SQLite (bot_tokens.db)
4. При каждом запросе бот передаёт access_token
5. Если токен истёк — бот автоматически обновляет его через refresh_token
```

### 🤖 Как работает бот

Взаимодействие с пользователем
```
Пользователь общается с ботом через MAX. 
Бот поддерживает два способа взаимодействия:
- Команды (через меню или ввод /команда)
- Инлайн-кнопки (нажатие на кнопки в сообщениях)
```

Регистрация пользователя
```
Когда пользователь впервые запускает бота (Начать), 
происходит автоматическая регистрация:
1. Бот получает max_user_id и chat_id из MAX.
2. Отправляет запрос на Backend для создания пользователя.
3. Backend возвращает JWT токены.
4. Бот сохраняет токены в SQLite.
5. Отправляет приветственное сообщение с главным меню.
```

Главное меню
```
После регистрации пользователь видит главное меню с кнопками:
📋 Мои привычки    
➕ Добавить привычку
✅ Отметить выполнение    
🏁 Завершить привычку
📊 Статистика
```

> Каждая кнопка запускает определённое действие.

### 📋 Управление привычками

Добавление привычки
```
Как это работает:
1. Пользователь нажимает кнопку «➕ Добавить привычку».
2. Бот запрашивает название привычки.
3. Пользователь вводит название (например, «Утренняя зарядка»).
4. Бот отправляет POST запрос на /api/v1/habits/ с JWT.
5. Backend создаёт привычку в базе данных со статусом is_active = true и days_completed = 0.
6. Бот подтверждает создание и показывает цель (21 день).
```

Просмотр привычек
```
Как это работает:
1. Пользователь нажимает кнопку «📋 Мои привычки».
2. Бот запрашивает у Backend список привычек пользователя.
3. Backend возвращает активные привычки.
4. Бот форматирует список с прогрессом и статусами.
5. Показывает пользователю.

Пример вывода:
📋 Ваши привычки
1. ✅ Утренняя зарядка
   Прогресс: 15/21 дней
   [███████████████░░░░░] 71%
2. 🏁 Чтение книги
   Прогресс: 21/21 дней
   [████████████████████] 100%
```

Отметка выполнения
```
Как это работает:
1. Пользователь нажимает кнопку «✅ Отметить выполнение».
2. Бот получает список активных привычек.
3. Для каждой привычки отправляет отдельное сообщение с кнопками:
   - ✅ Выполнено
   - ❌ Пропустить
   - 🏁 Завершить досрочно
4. Пользователь выбирает действие.
5. Бот отправляет POST запрос на /api/v1/habits/{id}/complete.
6. Backend обновляет прогресс и создаёт лог.
```

### 📋 Механизм сброса привычки

Ручной пропуск (mark_skipped)
```
Пользователь нажал кнопку «❌ Пропустить»:
1. Проверка, что привычка существует и активна.
2. days_completed = 0 — сброс прогресса.
3. last_completed = None — очистка даты последнего выполнения.
4. Создаётся лог с completed = False.

Пример: Ручной пропуск
День 1: ✅ Выполнено → days_completed = 1
День 2: ✅ Выполнено → days_completed = 2
День 3: ❌ Пропустить → days_completed = 0
День 4: ✅ Выполнено → days_completed = 1 (начало заново)
Пример 2: Автоматический сброс (пропуск > 1 дня)
```

Автоматический сброс при пропуске дня
```
Пользователь пропустил более 1 дня:
1. При следующем выполнении проверяется last_completed.
2. Если прошло > 1 дня — days_completed = 0.
3. Затем +1 за текущее выполнение.

Пример: Автоматический сброс (пропуск > 1 дня)
День 1: ✅ Выполнено → days_completed = 1, last_completed = 01.09
День 2: ✅ Выполнено → days_completed = 2, last_completed = 02.09
День 3: (ничего не делал)
День 4: (ничего не делал)
День 5: ✅ Выполнено → days_completed = 0 (сброс!), затем +1 = 1
```

### 📊 Статистика и аналитика

Что показывает статистика
```
При нажатии кнопки «📊 Статистика» пользователь видит:
Общая информация:
- Всего привычек
- Активных привычек
- Завершённых привычек
- Всего выполнено дней
- Лучшая серия (стрик)
- Эффективность (процент выполненных дней)

Пример вывода статистики:
📊 Ваша статистика
📌 Всего привычек: 5
✅ Активных: 3
🏁 Завершено: 2
📅 Всего выполнено дней: 45
🔥 Лучшая серия: 7 дней
📈 Эффективность: 75%
⏰ Напоминания
```

### Как работают напоминания

```
Бот автоматически отправляет напоминания дважды в день:
- 09:00 — утреннее напоминание
- 21:00 — вечернее напоминание

Логика работы:
1. Планировщик (APScheduler) запускает задачу в указанное время.
2. Backend получает список всех пользователей с активными привычками.
3. Для каждого пользователя формируется сообщение со списком привычек.
4. Сообщение отправляется через Bot API.
```

Формат напоминания
```
📋 Ваши привычки на сегодня:
1. Утренняя зарядка ✅ (15/21 дн.)
2. Чтение книги ❌ (7/21 дн.)

⚠️ Не забывайте отмечать выполнение привычек!
❤️ Для отметки выполнения нажмите кнопку ниже:

📋 Мои привычки
➕ Добавить привычку
✅ Отметить выполнение
🏁 Завершить привычку
📊 Статистика
```
---

## 🗄 Backend и база данных

Архитектура Backend
```
Backend построен на FastAPI и предоставляет REST API для бота:
- API Routes — обработка HTTP запросов
- Services — бизнес-логика
- Models — SQLAlchemy модели для работы с БД
- Scheduler — планировщик напоминаний
- Auth — JWT аутентификация
```

Структура базы данных:

Таблица users
```
sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    max_user_id INTEGER UNIQUE NOT NULL,  -- ID из MAX
    chat_id INTEGER NOT NULL,             -- chat_id для отправки
    username VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

Таблица habits
```
sql
CREATE TABLE habits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    completed_early BOOLEAN DEFAULT FALSE,
    days_completed INTEGER DEFAULT 0,
    max_days INTEGER DEFAULT 21,
    last_completed DATE,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE INDEX ix_habits_user_active ON habits(user_id, is_active);
```

Таблица habit_logs
```
sql
CREATE TABLE habit_logs (
    id SERIAL PRIMARY KEY,
    habit_id INTEGER REFERENCES habits(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    UNIQUE(habit_id, date)
);

CREATE INDEX ix_habit_logs_date_completed ON habit_logs(date, completed);
```
---

## 🛡 Безопасность и надёжность

Обработка ошибок
```
✅ Все запросы к API обрабатываются с try/except
✅ При ошибках пользователь получает понятное сообщение
✅ Логирование всех ошибок для отладки
```

Защита данных
```
✅ Использование параметризованных SQL-запросов
✅ Валидация входных данных через Pydantic схемы
✅ Хранение токена бота в переменных окружения
✅ JWT токены с ограниченным сроком действия
```

Отказоустойчивость
```
✅ Повторные попытки при сбоях (tenacity retry)
✅ Автоматическое восстановление соединения с БД
✅ Graceful shutdown при остановке
```
---

## 👥 Вклад в проект

Как помочь
```
# Создать ветку
git checkout -b feature/amazing-feature

# Внести изменения
git add .
git commit -m "feat: add amazing feature"

# Запустить проверки
poetry run black .
poetry run isort .
poetry run mypy .
poetry run pylint .
poetry run pytest -v

# Создать Pull Request
git push origin feature/amazing-feature
```

Требования к коду
```
# Проверка перед коммитом
poetry run black .              # Форматирование
poetry run isort .              # Сортировка импортов
poetry run mypy .               # Проверка типов
poetry run pylint .             # Качество кода
poetry run pytest -v            # Тесты
```
---

## 📄 Лицензия

> Этот проект распространяется под лицензией MIT.<br>
> Подробнее см. файл LICENSE.
---

## 📞 Контакты
Автор: Zinnurov Lenar

Email: zinnurov.lenar@gmail.com

Telegram: @Zinnurov_Lenar

MAX: Lenar Zinnurov

GitHub: Lenar24

---

## 🙏 Благодарности

FastAPI — За отличный фреймворк

MAX API — За платформу для чат-ботов

SQLAlchemy — За мощный ORM

PostgreSQL — За надёжную базу данных

APScheduler — За планировщик задач

---

<div align="center"> Сделано с ❤️ для формирования полезных привычек </div>

---
