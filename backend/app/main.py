"""
Основной файл приложения TrackingHabits, построенный с использованием фреймворка FastAPI.
Приложение для отслеживания привычек, управления пользователями, напоминаниями и статистикой.
"""

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .api import habits_router, users_router, stats_router, reminders_router
from .api.auth import router as auth_router
from .core.config import settings
from .core.logging_config import setup_logging
from .scheduler import start_scheduler
from .services.habit_service import HabitService
from .utils.database import init_db, get_db
from .utils.auth import get_current_admin
from .models import User

# Настройка логирования
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Lifespan - контекстный менеджер жизненного цикла.
    Управляет стартом и остановкой приложения.
    """
    # Старт
    logger.info("🚀 Старт приложения...")

    # Инициализация БД
    try:
        init_db()
        logger.info("✅ База данных инициализирована")
    except Exception as e:
        logger.error(f"❌ Не удалось инициализировать базу данных: {e}")
        raise

    # Запуск планировщика
    try:
        scheduler = start_scheduler()
        _app.state.scheduler = scheduler
        logger.info("✅ Планировщик запущен")
    except Exception as e:
        logger.error(f"❌ Не удалось запустить планировщик: {e}")
        # Продолжаем работу без планировщика

    logger.info("✅ Приложение успешно запущено")

    yield

    # Остановка
    logger.info("🛑 Завершение работы приложения...")

    if hasattr(_app.state, "scheduler") and _app.state.scheduler:
        try:
            _app.state.scheduler.shutdown()
            logger.info("✅ Планировщик остановлен")
        except Exception as e:
            logger.error(f"❌ Ошибка в остановке планировщика: {e}")

    logger.info("✅ Приложение остановлено")


# Создание приложения
app = FastAPI(
    title="Habit Tracker API",
    description="API для отслеживания привычек по методу 21 дня",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Trusted Hosts (защита от Host header attacks)
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )


# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware для логирования всех HTTP запросов.
    """
    start_time = time.time()

    # Логируем входящий запрос
    logger.debug(f"➡️ {request.method} {request.url.path}")

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"❌ Ошибка обработки запроса {request.url.path}: {e}")
        raise

    # Логируем ответ
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"time={process_time:.3f}s"
    )

    response.headers["X-Process-Time"] = str(process_time)
    return response


# Глобальные обработчики исключений

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Обработчик HTTP исключений.
    """
    logger.warning(f"HTTP исключение: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "path": request.url.path,
        },
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Обработчик ошибок базы данных.
    """
    logger.error(f"Ошибка базы данных {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Database error occurred",
            "path": request.url.path,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Обработчик всех непредвиденных исключений.
    """
    logger.error(
        f"Необработанное исключение {request.url.path}: {exc}",
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "path": request.url.path,
        },
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    """
    Обработчик 404 ошибок.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "Endpoint not found",
            "path": request.url.path,
        },
    )


# Подключение роутеров

API_PREFIX = "/api/v1"

app.include_router(auth_router, prefix=f"{API_PREFIX}/auth", tags=["auth"])
app.include_router(habits_router, prefix=f"{API_PREFIX}/habits", tags=["habits"])
app.include_router(users_router, prefix=f"{API_PREFIX}/users", tags=["users"])
app.include_router(stats_router, prefix=f"{API_PREFIX}/stats", tags=["stats"])
app.include_router(reminders_router, prefix=f"{API_PREFIX}/reminders", tags=["reminders"])


# Корневые эндпоинты

@app.get("/")
async def read_root():
    """
    Проверка работоспособности API.
    """
    return {
        "message": "Habit Tracker API запущен",
        "version": app.version,
        "docs": "/api/docs",
    }


@app.get("/health")
async def health():
    """
    Эндпоинт для мониторинга состояния приложения.
    """
    return {
        "status": "ok",
        "version": app.version,
        "scheduler_running": hasattr(app.state, "scheduler"),
        "environment": settings.ENVIRONMENT,
    }


@app.get("/api")
async def api_info():
    """
    Информация о доступных API.
    """
    return {
        "api_version": "v1",
        "base_path": "/api/v1",
        "endpoints": [
            {"path": "/auth", "methods": ["POST", "GET"]},
            {"path": "/habits", "methods": ["GET", "POST", "PUT", "DELETE"]},
            {"path": "/users", "methods": ["GET", "PUT"]},
            {"path": "/stats", "methods": ["GET"]},
            {"path": "/reminders", "methods": ["POST", "GET", "PUT", "DELETE"]},
        ],
        "docs": "/api/docs",
    }


# Административные эндпоинты

@app.get("/api/v1/admin/stats")
async def admin_stats(
    current_user: User = Depends(get_current_admin),
):
    """
    Получение статистики по приложению для администраторов.
    """
    return {
        "status": "ok",
        "scheduler": "running" if hasattr(app.state, "scheduler") else "stopped",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
    }


@app.post("/api/v1/admin/trigger-scheduler")
async def trigger_scheduler(
    current_user: User = Depends(get_current_admin),
):
    """
    Ручной запуск планировщика для администраторов.
    """
    if hasattr(app.state, "scheduler"):
        # Здесь можно вызвать проверку привычек
        return {"message": "Scheduler triggered successfully"}
    return {"message": "Scheduler is not running"}, status.HTTP_400_BAD_REQUEST


@app.post("/api/v1/admin/check-21-days")
async def admin_check_21_days(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    """
    Ручная проверка правила 21 дня для администраторов.
    """
    result = HabitService.check_21_days(db, user_id=current_user.max_user_id)
    return result


# Запуск приложения (для разработки)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
