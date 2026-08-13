# 🏆 Чат-бот *Трекер привычек*

<div align="center">

[![CI - Code Check](https://github.com/Lenar24/TrackingHabits/actions/workflows/ci.yml/badge.svg)](https://github.com/Lenar24/TrackingHabits/actions/workflows/ci.yml)
[![Pylint](https://img.shields.io/badge/pylint-10.00%2F10-brightgreen)](https://github.com/Lenar24/TrackingHabits)
[![Mypy](https://img.shields.io/badge/mypy-passing-brightgreen)](https://github.com/Lenar24/TrackingHabits)
[![Tests](https://img.shields.io/badge/tests-124%20passed-brightgreen)](https://github.com/Lenar24/TrackingHabits)
[![Python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.13-green)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-ready-blue)](https://www.docker.com)
[![MAX Platform](https://img.shields.io/badge/MAX-Platform-orange)](https://max.ru)

**Чат-бот для трекинга привычек по методу 21 дня на платформе MAX**

[Демо бота в MAX](https://max.ru/se13645210_bot) • [Документация API](#-api-документация) • [Установка](#-установка)

</div>

## 📖 Оглавление

- [О проекте](#-о-проекте)
- [Скриншоты](#-скриншоты)
- [Технологии](#-технологии)
- [Архитектура](#-архитектура)
- [Установка](#-установка)
- [Запуск](#-запуск)
- [API Документация](#-api-документация)
- [Работа с ботом](#-работа-с-ботом)
- [Тестирование](#-тестирование)
- [CI/CD](#-cicd)
- [Структура проекта](#-структура-проекта)
- [Вклад в проект](#-вклад-в-проект)
- [Лицензия](#-лицензия)

---

## 📱 О проекте

Чат-бот **Трекер привычек** — это чат-бот для платформы **MAX**, 
который помогает пользователям формировать полезные привычки по методу "21 день". 
Бот интегрируется с MAX через API MAX и предоставляет удобный интерфейс 
для отслеживания прогресса.

### 🌟 Основные возможности

| Функция                     | Описание                                 |
|-----------------------------|------------------------------------------|
| 📋 **Создание привычек**    | Добавление привычек с описанием          |
| ✅ **Ежедневное выполнение** | Отметка выполнения привычек              |
| 📊 **Статистика**           | Визуализация прогресса и серий           |
| 🔥 **Серии (стрики)**       | Отслеживание непрерывных дней выполнения |
| 🏁 **Правило 21 дня**       | Автоматическое завершение привычки       |
| ⏰ **Напоминания**           | Ежедневные уведомления (9:00 и 21:00)    |
| 🎯 **Досрочное завершение** | Возможность завершить привычку раньше    |

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

### Bot (MAX Платформа)
| Технология  | Версия   | Назначение                 |
|-------------|----------|----------------------------|
| **MAX API** | 1.2.1    | Платформа для чат-ботов    |
| **httpx**   | 0.27     | Асинхронный HTTP клиент    |
| **Uvicorn** | 0.34     | ASGI сервер                |
| **FastAPI** | 0.115.13 | Веб-фреймворк для вебхуков |

### Инструменты
| Инструмент | Версия | Назначение               |
|------------|--------|--------------------------|
| **Poetry** | -      | Управление зависимостями |
| **Docker** | -      | Контейнеризация          |
| **Pytest** | 7.0    | Тестирование             |
| **Pylint** | 3.0    | Качество кода            |
| **Mypy**   | 1.7    | Типизация                |
| **Black**  | 23.0   | Форматирование           |
| **Isort**  | 5.12   | Сортировка импортов      |

---

## 🏗 Архитектура

```mermaid
flowchart TB
    subgraph MAX["MAX Platform (Telegram)"]
        MAX1["API для чат-ботов"]
    end
    
    MAX -->|"Webhook"| BOT
    
    subgraph BOT["Bot (FastAPI) — порт 8001"]
        direction LR
        B1["Handlers<br/>(message, callback, command)"]
        B2["Keyboards<br/>(inline keyboards)"]
        B3["HabitService<br/>(client для backend API)"]
    end
    
    BOT -->|"HTTP"| BACKEND
    
    subgraph BACKEND["Backend (FastAPI) — порт 8000"]
        direction LR
        C1["API Routes"]
        C2["Services<br/>(Business Logic)"]
        C3["Models<br/>(SQLAlchemy)"]
    end
    
    BACKEND --> DB[("PostgreSQL<br/>habit_tracker")]
    
    DB --> TABLES["users, habits, habit_logs"]
    
    style MAX fill:#f9f,stroke:#333,stroke-width:2px,color:#fff
    style BOT fill:#bbf,stroke:#333,stroke-width:2px,color:#fff
    style BACKEND fill:#bfb,stroke:#333,stroke-width:2px
    style DB fill:#fbb,stroke:#333,stroke-width:2px
    style TABLES fill:#eee,stroke:#333,stroke-width:1px
```
---

## 🚀 Установка

### Требования

- Python 3.13+
- Docker & Docker Compose
- Poetry
- PostgreSQL (для локальной разработки)
- Аккаунт на платформе [MAX](https://max.ru)
- Ngrok или Cloudflare Tunnel (для вебхуков)

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/TrackingHabits.git
cd TrackingHabits
2. Настройка переменных окружения
bash
# Создать .env файл
cp .env.example .env

# Отредактировать .env
nano .env
.env.example:

bash
# Backend
DATABASE_URL=postgresql://postgresql:postgresql@db:5432/habit_tracker
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Bot (MAX Platform)
MAX_BOT_TOKEN=your-max-bot-token
API_URL=http://backend:8000
WEBHOOK_URL=https://your-domain.com/webhook

# Docker
POSTGRES_USER=postgresql
POSTGRES_PASSWORD=postgresql
POSTGRES_DB=habit_tracker
3. Получение токена бота в MAX
Зарегистрируйтесь на платформе MAX

Создайте нового бота в личном кабинете

Получите токен бота

Добавьте токен в .env как MAX_BOT_TOKEN

4. Настройка вебхука
Для разработки (через Cloudflare Tunnel):

bash
# Скачать cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64

# Запустить туннель
./cloudflared-linux-amd64 tunnel --url http://localhost:8001

# Добавить полученный URL в WEBHOOK_URL
WEBHOOK_URL=https://xxx.trycloudflare.com/webhook
Для продакшена:

bash
WEBHOOK_URL=https://your-domain.com/webhook
🐳 Запуск
Вариант 1: Docker Compose (рекомендуется)
bash
# Запуск всех сервисов
docker compose up -d

# Просмотр логов
docker compose logs -f

# Остановка
docker compose down

# Пересборка с обновлением
docker compose up -d --build
Вариант 2: Локальный запуск
bash
# Установка зависимостей
poetry install

# Запуск backend
cd backend
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Запуск bot (в другом терминале)
cd bot
poetry run python main.py
Вариант 3: Через Makefile
makefile
# Создать Makefile
.PHONY: up down logs test lint format

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

test:
	poetry run pytest -v

lint:
	poetry run mypy . && poetry run pylint .

format:
	poetry run black . && poetry run isort .
bash
make up   # Запуск
make logs # Логи
make test # Тесты
make down # Остановка
📚 API Документация
Доступ к документации
После запуска backend доступна интерактивная документация:

URL	Описание
http://localhost:8000/docs	Swagger UI
http://localhost:8000/redoc	ReDoc
http://localhost:8000/openapi.json	OpenAPI спецификация
Эндпоинты
Пользователи (/users)
Метод	Эндпоинт	Описание
POST	/users/	Создание пользователя
GET	/users/	Получение всех пользователей
GET	/users/{user_id}	Получение пользователя
PUT	/users/{user_id}/chat_id	Обновление chat_id
Привычки (/habits)
Метод	Эндпоинт	Описание
POST	/habits/	Создание привычки
GET	/habits/{user_id}	Активные привычки
GET	/habits/{user_id}/all	Все привычки
GET	/habits/item/{habit_id}	Привычка по ID
PUT	/habits/{habit_id}	Обновление привычки
DELETE	/habits/{habit_id}	Удаление привычки
POST	/habits/{habit_id}/complete	Отметка выполнения
POST	/habits/{habit_id}/skip	Пропуск
POST	/habits/{habit_id}/complete-early	Досрочное завершение
Статистика (/habits)
Метод	Эндпоинт	Описание
GET	/habits/{user_id}/stats	Статистика привычек
Примеры запросов
Создание пользователя:

bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123456789, "username": "john_doe", "chat_id": 987654321}'
Создание привычки:

bash
curl -X POST "http://localhost:8000/habits/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123456789, "name": "Утренняя зарядка", "description": "10 минут"}'
Отметка выполнения:

bash
curl -X POST "http://localhost:8000/habits/1/complete"
Получение статистики:

bash
curl "http://localhost:8000/habits/123456789/stats"
🤖 Работа с ботом
Команды
Команда	Описание
/start	Главное меню
/habits	Список привычек
/add	Добавить привычку
/complete	Отметить выполнение
/finish	Досрочное завершение
/stats	Статистика
/help	Помощь
Кнопки меню
text
📋 Мои привычки    ➕ Добавить привычку
✅ Отметить выполнение    🏁 Завершить привычку
📊 Статистика
Пример диалога
text
👤 Пользователь: /start
🤖 Бот: 🌟 Добро пожаловать в Трекер привычек!
Выберите действие в меню ниже:

📋 Мои привычки    ➕ Добавить привычку
✅ Отметить выполнение    🏁 Завершить привычку
📊 Статистика
text
👤 Пользователь: ➕ Добавить привычку
🤖 Бот: ✏️ Введите название новой привычки:
Например: «Читать 30 минут» или «Заниматься спортом»
text
👤 Пользователь: Утренняя зарядка
🤖 Бот: ✅ Привычка добавлена!

📌 Название: Утренняя зарядка
🎯 Цель: 21 дней
📊 Текущий прогресс: 0/21 дней

💡 Отмечайте выполнение каждый день через меню!
text
👤 Пользователь: ✅ Отметить выполнение
🤖 Бот: ✅ **Привычка выполнена!**

📌 Привычка: Утренняя зарядка
📊 Прогресс: 1/21 дней
💪 Осталось: 20 дней до цели
🧪 Тестирование
Запуск тестов
bash
# Все тесты
poetry run pytest -v

# С покрытием
poetry run pytest --cov=backend --cov=bot -v

# Только unit тесты
poetry run pytest -m unit -v

# Только интеграционные тесты
poetry run pytest -m integration -v

# С HTML отчетом
poetry run pytest --cov-report=html -v
Результаты тестов
text
===================== 124 passed, 4 warnings in 16.78s =====================

---------- coverage: platform linux, python 3.13.15-final-0 ----------
Name                                    Stmts   Miss  Cover
---------------------------------------------------------------------
backend/app/api/habits.py                  76      5    93%
backend/app/api/stats.py                   26      0   100%
backend/app/api/users.py                   41      0   100%
backend/app/models/*                       43      0   100%
backend/app/schemas/*                      51      0   100%
backend/app/services/user_service.py       22      0   100%
...
TOTAL                                     981    483    51%
Проверка качества кода
bash
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
🔄 CI/CD
GitHub Actions
Проект настроен на автоматическую проверку кода через GitHub Actions.

Что проверяется:

✅ Форматирование (Black)

✅ Сортировка импортов (Isort)

✅ Типизация (Mypy)

✅ Качество кода (Pylint)

✅ Тесты (Pytest)

.github/workflows/ci.yml:

yaml
name: CI - Code Check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    services:
      postgres: ...
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: poetry install
      - run: poetry run black --check .
      - run: poetry run isort --check-only .
      - run: poetry run mypy . --no-error-summary
      - run: poetry run pylint . --score=n
      - run: poetry run pytest -v
Badges статуса
https://github.com/yourusername/TrackingHabits/actions/workflows/ci.yml/badge.svg

markdown
[![CI](https://github.com/yourusername/TrackingHabits/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/TrackingHabits/actions/workflows/ci.yml)
📁 Структура проекта
text
TrackingHabits/
├── backend/                     # Backend сервер
│   ├── app/
│   │   ├── api/                 # API эндпоинты
│   │   │   ├── habits.py
│   │   │   ├── users.py
│   │   │   ├── stats.py
│   │   │   └── reminders.py
│   │   ├── core/                # Конфигурация
│   │   │   └── config.py
│   │   ├── models/              # SQLAlchemy модели
│   │   │   ├── user.py
│   │   │   ├── habit.py
│   │   │   └── habit_log.py
│   │   ├── schemas/             # Pydantic схемы
│   │   │   ├── user.py
│   │   │   ├── habit.py
│   │   │   └── habit_log.py
│   │   ├── services/            # Бизнес-логика
│   │   │   ├── user_service.py
│   │   │   └── habit_service.py
│   │   ├── utils/               # Утилиты
│   │   │   ├── database.py
│   │   │   └── keyboards.py
│   │   ├── scheduler.py         # Планировщик
│   │   └── main.py              # Точка входа
│   └── migrations/              # Alembic миграции
│
├── bot/                         # Чат-бот (MAX Platform)
│   ├── core/
│   │   └── config.py
│   ├── handlers/                # Обработчики
│   │   ├── message_handlers.py
│   │   ├── callback_handlers.py
│   │   └── command_handlers.py
│   ├── keyboards/               # Клавиатуры
│   │   └── keyboards.py
│   ├── services/                # Клиентские сервисы
│   │   ├── api_client.py
│   │   └── habit_service.py
│   ├── utils/                   # Утилиты бота
│   │   ├── formatters.py
│   │   └── validators.py
│   └── main.py                  # Точка входа
│
├── tests/                       # Тесты
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_habits.py
│   ├── test_stats.py
│   └── ...
│
├── docker-compose.yml           # Docker Compose
├── Dockerfile                   # Docker для backend
├── Dockerfile.bot               # Docker для bot
├── pyproject.toml               # Poetry конфиг
├── poetry.lock                  # Зависимости
├── mypy.ini                     # Mypy конфиг
├── alembic.ini                  # Alembic конфиг
├── .github/
│   └── workflows/
│       └── ci.yml               # CI/CD
└── README.md                    # Документация
👥 Вклад в проект
Как помочь
Fork репозитория

Создать ветку (git checkout -b feature/amazing-feature)

Внести изменения

Запустить проверки

Создать Pull Request

Требования к коду
bash
# Проверка перед коммитом
poetry run black .              # Форматирование
poetry run isort .              # Сортировка импортов
poetry run mypy .               # Проверка типов
poetry run pylint .             # Качество кода
poetry run pytest -v            # Тесты
📄 Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. файл LICENSE.

📞 Контакты
Автор: Zinnurov Lenar

Email: zinnurov.lenar@gmail.com

Telegram: @your_telegram

GitHub: yourusername

🙏 Благодарности
FastAPI - За отличный фреймворк

MAX API - За платформу для чат-ботов

SQLAlchemy - За мощный ORM

Telegram - За мессенджер

<div align="center">
Сделано с ❤️ для формирования полезных привычек

⬆ Наверх

</div> ```

