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
- [Эндпоинты](#-эндпоинты)
- [Работа с ботом](#-работа-с-ботом)
- [Тестирование](#-тестирование)
- [CI/CD](#-cicd)
- [Структура проекта](#-структура-проекта)
- [Подробное описание работы бота и приложения](#-подробное описание работы бота и приложения)
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
    subgraph MAX["MAX Platform"]
        MAX1["API для чат-ботов"]
    end
    
    MAX -->|"Webhook (POST /webhook)"| BOT
    
    subgraph BOT["Bot (FastAPI) — порт 8001"]
        direction LR
        B1["Handlers<br/>(message, callback, command)"]
        B2["Keyboards<br/>(inline keyboards)"]
        B3["HabitService<br/>(client для backend API)"]
    end
    
    BOT -->|"HTTP API (JSON)"| BACKEND
    
    subgraph BACKEND["Backend (FastAPI) — порт 8000"]
        direction LR
        C1["API Routes"]
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

### Требования

- Python 3.13+
- Docker & Docker Compose
- Poetry
- PostgreSQL (для локальной разработки)
- Аккаунт на платформе [MAX](https://max.ru)
- Ngrok, Cloudflare Tunnel или serveo.net (для вебхуков)

### 1. Клонирование репозитория

```
git clone https://github.com/Lenar24/TrackingHabits.git
cd TrackingHabits
```

### 2. Настройка переменных окружения

```
# Создать .env файл
cp .env.example .env

# Отредактировать .env
nano .env
.env.example:

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
```

### 3. Получение токена бота в MAX

```
Зарегистрируйтесь на платформе MAX.
Создайте нового бота в личном кабинете.
Получите токен бота.
Добавьте токен в .env как MAX_BOT_TOKEN.
```

### 4. Настройка вебхука

Для разработки (через Cloudflare Tunnel или serveo.net):

```
# Скачать cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64

# Запустить туннель
./cloudflared-linux-amd64 tunnel --url http://localhost:8001 --protocol http2 для Cloudflare Tunnel
ssh -R 80:localhost:8001 serveo.net для serveo.net 

# Добавить полученный URL в WEBHOOK_URL
WEBHOOK_URL=https://xxx.trycloudflare.com/webhook
```

Для продакшена:

```
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

```
# Установка зависимостей
poetry install

# Запуск backend
cd backend
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Запуск bot (в другом терминале)
cd bot
poetry run python main.py
```

---

## 📚 API Документация

Доступ к документации.<br>
После запуска backend доступна интерактивная документация:

| URL	                                | Описание             |
|-------------------------------------|----------------------|
| http://localhost:8000/docs	         | Swagger UI           |
| http://localhost:8000/redoc	        | ReDoc                |
| http://localhost:8000/openapi.json	 | OpenAPI спецификация |

---

## 🗺 Эндпоинты

### 👥 Пользователи (/users)

| Метод	 | Эндпоинт	                 | Описание                     |
|--------|---------------------------|------------------------------|
| POST	  | /users/	                  | Создание пользователя        |
| GET	   | /users/	                  | Получение всех пользователей |
| GET	   | /users/{user_id}	         | Получение пользователя       |
| PUT	   | /users/{user_id}/chat_id	 | Обновление chat_id           |

### 📋 Привычки (/habits)

| Метод	  | Эндпоинт	                          | Описание             |
|---------|------------------------------------|----------------------|
| POST	   | /habits/	                          | Создание привычки    |
| GET	    | /habits/{user_id}	                 | Активные привычки    |
| GET	    | /habits/{user_id}/all	             | Все привычки         |
| GET	    | /habits/item/{habit_id}	           | Привычка по ID       |
| PUT	    | /habits/{habit_id}	                | Обновление привычки  |
| DELETE	 | /habits/{habit_id}	                | Удаление привычки    |
| POST	   | /habits/{habit_id}/complete	       | Отметка выполнения   |
| POST	   | /habits/{habit_id}/skip	           | Пропуск              |
| POST	   | /habits/{habit_id}/complete-early	 | Досрочное завершение |

### 📊 Статистика (/habits)

| Метод	 | Эндпоинт	                | Описание            |
|--------|--------------------------|---------------------|
| GET	   | /habits/{user_id}/stats	 | Статистика привычек |

### Примеры запросов

Создание пользователя:

```
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123456789, "username": "john_doe", "chat_id": 987654321}'
```

Создание привычки:

```
curl -X POST "http://localhost:8000/habits/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123456789, "name": "Утренняя зарядка", "description": "10 минут"}'
```

Отметка выполнения:

```
curl -X POST "http://localhost:8000/habits/1/complete"
```

Получение статистики:

```
curl "http://localhost:8000/habits/123456789/stats"
```

---

## 🤖 Работа с ботом

### Команды:

| Команда	   | Описание             |
|------------|----------------------|
| /start	    | Главное меню         |
| /habits	   | Список привычек      |
| /add	      | Добавить привычку    |
| /complete	 | Отметить выполнение  |
| /finish	   | Досрочное завершение |
| /stats	    | Статистика           |

### Кнопки меню:

```
📋 Мои привычки    
➕ Добавить привычку
✅ Отметить выполнение    
🏁 Завершить привычку
📊 Статистика
```

### Пример диалога

```
👤 Пользователь: /start
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

### Запуск тестов

```
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
```

### Результаты тестов

```
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
```

### Проверка качества кода

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

GitHub Actions<br>
Проект настроен на автоматическую проверку кода через GitHub Actions.

Что проверяется:

```
✅ Форматирование (Black)
✅ Сортировка импортов (Isort)
✅ Типизация (Mypy)
✅ Качество кода (Pylint)
✅ Тесты (Pytest)
```

```
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
```

### Badges статуса
[![CI - Code Check](https://github.com/Lenar24/TrackingHabits/actions/workflows/ci.yml/badge.svg)](https://github.com/Lenar24/TrackingHabits/actions/workflows/ci.yml)

---

### 📁 Структура проекта

```
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
Бот получает user_id и chat_id из MAX.
Отправляет запрос на Backend для создания пользователя.
Сохраняет пользователя в базу данных.
Отправляет приветственное сообщение с главным меню.
```

Главное меню
```
После регистрации пользователь видит главное меню с кнопками:

📋 Мои привычки    
➕ Добавить привычку
✅ Отметить выполнение    
🏁 Завершить привычку
📊 Статистика

Каждая кнопка запускает определённое действие.
```

### 📋 Управление привычками

Добавление привычки
```
Как это работает:
Пользователь нажимает кнопку «➕ Добавить привычку».
Бот запрашивает название привычки.
Пользователь вводит название (например, «Утренняя зарядка»).
Бот отправляет запрос на Backend.
Backend создаёт привычку в базе данных со статусом is_active = true и days_completed = 0.
Бот подтверждает создание и показывает цель (21 день).
```

Пример диалога:
```
👤 Пользователь: ➕ Добавить привычку
🤖 Бот: ✏️ Введите название новой привычки:
👤 Пользователь: Утренняя зарядка
🤖 Бот: ✅ Привычка добавлена! Цель: 21 дней.
```

Просмотр привычек
```
Как это работает:
Пользователь нажимает кнопку «📋 Мои привычки».
Бот запрашивает у Backend список привычек пользователя.
Backend возвращает активные привычки.
Бот форматирует список с прогрессом и статусами.
Показывает пользователю.
```

Пример вывода:
```
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
Пользователь нажимает кнопку «✅ Отметить выполнение».
Бот получает список активных привычек.
Для каждой привычки отправляет отдельное сообщение с кнопками:
✅ Выполнено
❌ Пропустить
🏁 Завершить досрочно
Пользователь выбирает действие.
Бот отправляет запрос на Backend.
Backend обновляет прогресс и создаёт лог.
```

Логика отметки выполнения:
```
python
def mark_completed(habit):
    # Проверка, выполнялась ли сегодня
    if habit.last_completed == today:
        return "Уже отмечено сегодня"
    
    # Проверка пропуска дней
    if habit.last_updated < today - 1 day:
        habit.days_completed = 0  # Сброс прогресса
    
    # Увеличение прогресса
    habit.days_completed += 1
    habit.last_completed = today
    
    # Проверка достижения цели
    if habit.days_completed >= 21:
        habit.is_active = False
        habit.completed_at = now()
        return "🎉 Поздравляю! Привычка сформирована!"
    
    return f"✅ Прогресс: {habit.days_completed}/21"
```

Пропуск выполнения
```
Как это работает:
Пользователь нажимает кнопку «❌ Пропустить».
Бот отправляет запрос на Backend.
Backend сбрасывает days_completed = 0.
Создаёт лог с completed = false.
Показывает сообщение о сбросе прогресса.
```

>Важно: Пропуск обнуляет прогресс, но не удаляет привычку. 
> Пользователь может начать заново в любой день.

Досрочное завершение
```
Как это работает:
Пользователь нажимает кнопку «🏁 Завершить досрочно».
Бот отправляет запрос на Backend.
Backend устанавливает:
is_active = false
completed_early = true
completed_at = now()
days_completed = 21 (для статистики)
Показывает сообщение о досрочном завершении.
```

>Когда использовать: Если пользователь уверен, что привычка сформировалась раньше 21 дня, 
> или хочет переключиться на другую привычку.

### 📊 Статистика и аналитика

Что показывает статистика
```
При нажатии кнопки «📊 Статистика» пользователь видит:
Общая информация:
Всего привычек
Активных привычек
Завершённых привычек
По каждой привычке:
Название и статус
Прогресс (дней выполнено / всего)
Лучшая серия (стрик)
Эффективность (процент выполненных дней)
Последние 7 дней (визуальный календарь)
```

Как рассчитывается статистика
```
python
def get_stats(habit):
    # 1. Лучшая серия
    best_streak = 0
    current_streak = 0
    
    for log in logs:
        if log.completed:
            current_streak += 1
            best_streak = max(best_streak, current_streak)
        else:
            current_streak = 0
    
    # 2. Эффективность
    total_logs = len(logs)
    completed_logs = sum(1 for log in logs if log.completed)
    efficiency = (completed_logs / total_logs) * 100
    
    # 3. Последние 7 дней
    last_7_days = []
    for log in logs[:7]:
        last_7_days.append({
            "date": log.date.strftime("%d.%m"),
            "completed": log.completed
        })
```

Пример вывода статистики
```
📊 Ваша статистика
📌 Всего привычек: 5
✅ Активных: 3
🏁 Завершено: 2
📌 Утренняя зарядка
   Статус: ✅ Активна
   Прогресс: 15/21 дней
   🔥 Лучшая серия: 7 дней
   📈 Эффективность: 75%
   📅 Неделя: ✅✅⬜✅✅✅⬜
```

### ⏰ Напоминания

Как работают напоминания
```
Бот автоматически отправляет напоминания дважды в день:
09:00 — утреннее напоминание
21:00 — вечернее напоминание
Логика работы:
Планировщик (APScheduler) запускает задачу в указанное время.
Backend получает список всех пользователей с активными привычками.
Для каждого пользователя формируется сообщение со списком привычек.
Сообщение отправляется через Bot API.
```

Формат напоминания
```
📋 Ваши привычки на сегодня:
1. Утренняя зарядка ✅ (15/21 дн.)
2. Чтение книги ❌ (7/21 дн.)
⚠️ Не забывайте отмечать выполнение привычек!
❤️ Для отметки выполнения нажмите кнопку ниже.
📋 Мои привычки
➕ Добавить привычку
✅ Отметить выполнение
🏁 Завершить привычку
📊 Статистика
```

### 🗄️ Backend и база данных

Архитектура Backend
```
Backend построен на FastAPI и предоставляет REST API для бота:
API Routes — обработка HTTP запросов
Services — бизнес-логика
Models — SQLAlchemy модели для работы с БД
Scheduler — планировщик напоминаний
```

Структура базы данных
```
Таблица users:
sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE,      -- Telegram user_id
    chat_id INTEGER,             -- Telegram chat_id
    username VARCHAR,
    created_at TIMESTAMP
);

Таблица habits:
sql
CREATE TABLE habits (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    name VARCHAR,
    description VARCHAR,
    created_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    days_completed INTEGER DEFAULT 0,
    max_days INTEGER DEFAULT 21,
    last_completed DATE,
    completed_at TIMESTAMP,
    completed_early BOOLEAN DEFAULT FALSE
);

Таблица habit_logs:
sql
CREATE TABLE habit_logs (
    id SERIAL PRIMARY KEY,
    habit_id INTEGER REFERENCES habits(id),
    date DATE DEFAULT CURRENT_DATE,
    completed BOOLEAN DEFAULT FALSE
);
```

Правило 21 дня
```
Как это работает:
Пользователь создаёт привычку с целью 21 день.
Каждый день отмечает выполнение.
При пропуске > 1 дня прогресс сбрасывается.
При достижении 21 дня привычка завершается автоматически.
Пользователь получает поздравление
```

Почему 21 день?
```
Согласно исследованиям, для формирования новой привычки требуется в среднем 21 день. 
Этот метод широко используется в психологии и саморазвитии.
```

### 🔄 Полный цикл работы приложения

1. Создание привычки
```
Пользователь → Бот → Backend → База данных → Backend → Бот → Пользователь
    1           2       3            4           5       6           7
Пользователь нажимает "➕ Добавить привычку".
Бот запрашивает название.
Пользователь вводит название.
Бот отправляет POST запрос на /habits/
Backend создаёт запись в БД.
Backend возвращает данные привычки.
Бот показывает подтверждение.
```

Отметка выполнения
```
Пользователь → Бот → Backend → База данных → Backend → Бот → Пользователь
    1           2       3            4           5       6           7
Пользователь нажимает "✅ Отметить выполнение".
Бот показывает список привычек.
Пользователь выбирает привычку и нажимает "✅ Выполнено".
Бот отправляет POST запрос на /habits/{id}/complete
Backend обновляет прогресс и создаёт лог.
Backend возвращает обновлённые данные.
Бот показывает результат.
```

Получение статистики
```
Пользователь → Бот → Backend → База данных → Backend → Бот → Пользователь
    1           2       3            4           5       6           7
Пользователь нажимает "📊 Статистика".
Бот отправляет GET запрос на /habits/{user_id}/stats
Backend запрашивает данные из БД.
Backend рассчитывает статистику.
Backend возвращает данные.
Бот форматирует статистику.
Пользователь видит результат.
```

Ежедневные напоминания
```
Scheduler → Backend → База данных → Backend → Bot API → Пользователь
    1           2           3           4          5           6
APScheduler запускает задачу в 09:00 или 21:00.
Backend запрашивает пользователей с активными привычками.
База данных возвращает список.
Backend формирует сообщения.
Backend отправляет сообщения через Bot API.
Пользователь получает напоминание.
```

### 🛡️ Безопасность и надёжность

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
```

Отказоустойчивость
```
✅ Повторные попытки при сбоях (retry)
✅ Автоматическое восстановление соединения с БД
✅ Graceful shutdown при остановке
```

### 📱 Примеры взаимодействия

Пример 1: Полный цикл привычки
```
День 1:
👤: Начать
🤖: Добро пожаловать! Выберите действие.
👤: ➕ Добавить привычку
🤖: Введите название:
👤: Утренняя зарядка
🤖: ✅ Привычка добавлена! Цель: 21 дней.

День 1-20:
👤: ✅ Отметить выполнение
🤖: Выберите привычку:
👤: Утренняя зарядка → ✅ Выполнено
🤖: ✅ Прогресс: 1/21... 20/21

День 21:
👤: ✅ Отметить выполнение
🤖: ✅ Прогресс: 21/21
🤖: 🎉 Поздравляю! Привычка сформирована!
```

Пример 2: Пропуск дня
```
День 5:
👤: ✅ Отметить выполнение
🤖: ✅ Прогресс: 5/21
День 6 (пропуск):
(Пользователь ничего не делает)
День 7:
👤: ✅ Отметить выполнение
🤖: ⚠️ Был пропущен день. Прогресс сброшен до 0.
🤖: ✅ Прогресс: 1/21
```

Пример 3: Досрочное завершение
```
👤: 🏁 Завершить привычку
🤖: Выберите привычку:
👤: Чтение книги → 🏁 Завершить досрочно
🤖: 🏁 Привычка завершена досрочно!
📊 Прогресс: 21/21 дней
🎉 Отличная работа!
```

### 🔧 Технические детали

Используемые технологии

| Компонент	   | Технология   | Назначение           |
|--------------|--------------|----------------------|
| Backend	     | FastAPI	     | Веб-фреймворк        |
| База данных	 | PostgreSQL	  | Хранение данных      |
| ORM	         | SQLAlchemy	  | Работа с БД          |
| Бот	         | MAX API	     | MAX интеграция       |
| Планировщик	 | APScheduler	 | Напоминания          |
| Миграции	    | Alembic	     | Управление схемой БД |

Переменные окружения
```
# База данных
DATABASE_URL=postgresql://user:pass@host:5432/db
# Бот
MAX_BOT_TOKEN=your_bot_token
WEBHOOK_URL=https://your-domain.com/webhook
# Безопасность
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```

### 📈 Масштабирование и производительность

Оптимизация запросов
```
✅ Использование индексов в БД
✅ Пагинация для больших списков
✅ Кэширование часто запрашиваемых данных
```

Асинхронность
```
✅ Все запросы к API асинхронные
✅ Параллельная отправка напоминаний
✅ Нет блокировок при обработке
```

Docker контейнеризация
```
✅ Изоляция компонентов
✅ Лёгкое масштабирование
✅ Единая среда разработки
```

### 🎯 Итог
```
Бот **Трекер привычек** — это полноценная система для формирования полезных привычек, которая:
**Автоматизирует процесс** — пользователь просто отмечает выполнение, всё остальное делает бот.
*8Мотивирует пользователя** — статистика, серии, напоминания.
**Надёжна и масштабируема** — современный стек технологий.
**Проста в использовании** — интуитивный интерфейс через MAX.
```

### Метод 21 дня работает! 🎯

---

## 👥 Вклад в проект

### Как помочь

```
Создать ветку (git checkout -b feature/amazing-feature)
Внести изменения
Запустить проверки
Создать Pull Request
```

### Требования к коду

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

Этот проект распространяется под лицензией MIT.<br>
Подробнее см. файл LICENSE.

---

## 📞 Контакты

Автор: **Zinnurov Lenar**

Email:<br> 
zinnurov.lenar@gmail.com<br>
Zinnurov.lenar.1981@yandex.ru

Telegram: @Zinnurov_Lenar

MAX: Lenar Zinnurov

GitHub: Lenar24

---

## 🙏 Благодарности

FastAPI - За отличный фреймворк

MAX API - За платформу для чат-ботов

SQLAlchemy - За мощный ORM

---

<br>

<div align="center">
Сделано с ❤️ для формирования полезных привычек
</div>

---
