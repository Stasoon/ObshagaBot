import asyncio

from src.database.models import register_models
from src.start_bot import start_bot
from src.utils import setup_logger


if __name__ == "__main__":
    # Конфигурация логирования
    setup_logger()

    # Запуск базы данных
    register_models()

    asyncio.run(start_bot())
