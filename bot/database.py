"""
Модуль предоставляет класс TokenDB для хранения и управления JWT-токенами бота.

Использует SQLite для легковесного хранения токенов пользователей.
"""

import logging
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

# ✅ Абсолютный путь к БД (в директории bot/)
BASE_DIR = Path(__file__).parent
DEFAULT_DB_PATH = BASE_DIR / "bot_tokens.db"


class TokenDB:
    """
    Класс для управления JWT-токенами в SQLite базе данных.

    Attributes:
        db_path: Путь к файлу базы данных
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Инициализация базы данных токенов.

        Args:
            db_path: Путь к файлу SQLite БД (по умолчанию bot/bot_tokens.db)
        """
        if db_path is None:
            db_path = str(DEFAULT_DB_PATH)

        self.db_path = db_path

        # ✅ Создать директорию, если её нет
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        try:
            self._init_db()
            logger.info(f"✅ TokenDB инициализирована: {db_path}")
        except sqlite3.Error as e:
            logger.error(f"❌ Ошибка инициализации TokenDB: {e}")
            raise

    def _init_db(self) -> None:
        """Создание таблиц и индексов."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    user_id INTEGER PRIMARY KEY,
                    access_token TEXT NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_expires_at 
                ON sessions(expires_at)
            """)
            conn.commit()

    def save_token(self, user_id: int, access_token: str, expires_in: int) -> None:
        """Сохранение или обновление токена пользователя."""
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO sessions 
                    (user_id, access_token, expires_at, created_at)
                    VALUES (?, ?, ?, ?)
                """, (
                    user_id,
                    access_token,
                    expires_at.isoformat(),
                    datetime.now(timezone.utc).isoformat()
                ))
                conn.commit()
                logger.debug(f"✅ Токен сохранён для user_id={user_id}")
        except sqlite3.Error as e:
            logger.error(f"❌ Ошибка сохранения токена для {user_id}: {e}")
            raise

    def get_token(self, user_id: int) -> Optional[str]:
        """Получение валидного токена пользователя."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT access_token, expires_at FROM sessions WHERE user_id = ?",
                    (user_id,)
                )
                row = cursor.fetchone()

                if row:
                    token, expires_at = row
                    try:
                        expires_at_dt = datetime.fromisoformat(expires_at)
                        if expires_at_dt.tzinfo is None:
                            expires_at_dt = expires_at_dt.replace(tzinfo=timezone.utc)

                        if datetime.now(timezone.utc) < expires_at_dt:
                            return token
                        else:
                            logger.info(f"⏰ Токен истёк для {user_id}, удаляем")
                            self.delete_token(user_id)
                            return None
                    except (ValueError, TypeError) as e:
                        logger.error(f"❌ Ошибка парсинга даты для {user_id}: {e}")
                        self.delete_token(user_id)
                        return None
                return None
        except sqlite3.Error as e:
            logger.error(f"❌ Ошибка получения токена для {user_id}: {e}")
            return None

    def delete_token(self, user_id: int) -> None:
        """Удаление токена пользователя."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
                conn.commit()
                logger.debug(f"🗑️ Токен удалён для {user_id}")
        except sqlite3.Error as e:
            logger.error(f"❌ Ошибка удаления токена для {user_id}: {e}")
            raise

    def delete_expired_tokens(self) -> int:
        """Удаление всех истёкших токенов."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "DELETE FROM sessions WHERE expires_at < ?",
                    (datetime.now(timezone.utc).isoformat(),)
                )
                count = cursor.rowcount
                conn.commit()
                if count > 0:
                    logger.info(f"🧹 Удалено {count} истёкших токенов")
                return count
        except sqlite3.Error as e:
            logger.error(f"❌ Ошибка очистки токенов: {e}")
            return 0

    def get_token_info(self, user_id: int) -> Optional[Dict]:
        """Получение информации о токене пользователя."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT access_token, expires_at, created_at "
                    "FROM sessions WHERE user_id = ?",
                    (user_id,)
                )
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except sqlite3.Error as e:
            logger.error(f"❌ Ошибка получения информации о токене {user_id}: {e}")
            return None

    def count_tokens(self) -> int:
        """Подсчёт количества активных токенов."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM sessions")
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            logger.error(f"❌ Ошибка подсчёта токенов: {e}")
            return 0

    def close(self) -> None:
        """Закрытие соединения с БД."""
        logger.debug("🔒 TokenDB закрыта")

    def __repr__(self) -> str:
        return f"<TokenDB db_path={self.db_path}>"
