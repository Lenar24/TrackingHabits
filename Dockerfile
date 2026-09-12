# Stage 1: Builder (установка зависимостей)

FROM python:3.13-slim AS builder

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry==$POETRY_VERSION

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости в виртуальное окружение
RUN poetry install --no-interaction --no-ansi --no-root --only main

# Stage 2: Runtime (финальный образ)

FROM python:3.13-slim AS runtime

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/app/.venv/bin:$PATH"

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Для psycopg2 (PostgreSQL)
    libpq5 \
    # Для работы с датами
    tzdata \
    # Для curl в healthcheck
    curl \
    # Утилиты
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Создаём non-root пользователя
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --shell /bin/bash --create-home appuser

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем виртуальное окружение из builder
COPY --from=builder /app/.venv /app/.venv

# Копируем исходный код
COPY --chown=appuser:appuser backend/ ./backend/
COPY --chown=appuser:appuser pyproject.toml ./
COPY --chown=appuser:appuser alembic.ini* ./

# Создаём директорию для логов
RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs

# Переключаемся на non-root пользователя
USER appuser

# Порты
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

# Команда запуска
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
