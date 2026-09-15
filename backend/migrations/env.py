"""
Alembic environment configuration.

Этот модуль отвечает за настройку Alembic для работы с миграциями.
Он читает DATABASE_URL из переменных окружения (settings),
что позволяет использовать разные БД для разработки и продакшена.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# ✅ Импорт моделей (обязательно для autogenerate!)
from backend.app.models import Base
from backend.app.models.user import User  # noqa: F401
from backend.app.models.habit import Habit  # noqa: F401
from backend.app.models.habit_log import HabitLog  # noqa: F401

# ✅ Импорт настроек (читает DATABASE_URL из .env)
from backend.app.core.config import settings

# Alembic Config object
config = context.config

# Настройка логирования из alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Metadata для autogenerate
target_metadata = Base.metadata


def get_url() -> str:
    """
    Получение URL БД из настроек приложения.

    Это позволяет использовать DATABASE_URL из .env,
    а не хардкодить его в alembic.ini.

    Returns:
        str: URL подключения к БД
    """
    return settings.DATABASE_URL


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    В этом режиме migrations генерируются как SQL-скрипты
    без подключения к БД.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    В этом режиме migrations применяются к реальной БД.
    """
    # ✅ Переопределяем URL из settings
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
