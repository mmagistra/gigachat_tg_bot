from config.base import BaseConfig


class ProductionConfig(BaseConfig):
    """Настройки для продакшена"""

    ENV: str = "production"
    LOG_LEVEL: str = "INFO"

    DEBUG: bool = False

    class Config:
        env_file = ".env.prod"
