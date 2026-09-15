"""
Отдельный процесс для запуска планировщика в Docker.
"""

import logging
import signal
import sys
import time

from .scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def signal_handler(signum, frame):
    """Обработчик сигналов для graceful shutdown."""
    logger.info(f"🛑 Получен сигнал {signum}, завершаем работу...")
    sys.exit(0)


def main():
    """Запуск планировщика в отдельном процессе."""
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    logger.info("🚀 Запуск планировщика...")
    scheduler = start_scheduler()

    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Остановка планировщика...")
        scheduler.shutdown()
        logger.info("✅ Планировщик остановлен")


if __name__ == "__main__":
    main()
