import os
from config.dev import DevelopmentConfig
from config.prod import ProductionConfig
from config.base import BaseConfig


def get_settings() -> BaseConfig:
    """
    Получение настроек в зависимости от окружения
    Окружение определяется переменной ENV из .env файла
    """
    env = os.getenv("ENV", "development")

    if env == "production":
        return ProductionConfig()
    elif env == "development":
        return DevelopmentConfig()
    else:
        return DevelopmentConfig()


settings = get_settings()

# BOT_TOKEN = settings.BOT_TOKEN
# DATABASE_URL = settings.get_database_url()
# LOG_LEVEL = settings.LOG_LEVEL
