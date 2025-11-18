import logging
import sys
from config.settings import settings

LOG_LEVEL = settings.LOG_LEVEL


def setup_logger():
    """Настройка логирования для всего приложения"""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('bot.log', encoding='utf-8')
        ]
    )

    # Отдельный логгер для aiogram
    aiogram_logger = logging.getLogger("aiogram")
    aiogram_logger.setLevel(logging.INFO)

    return logging.getLogger(__name__)


logger = setup_logger()
