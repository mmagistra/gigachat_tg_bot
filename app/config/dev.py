from config.base import BaseConfig


class DevelopmentConfig(BaseConfig):
    """Настройки для разработки"""

    ENV: str = "development"
    LOG_LEVEL: str = "DEBUG"

    DEBUG: bool = True

    class Config:
        env_file = ".env.dev"
