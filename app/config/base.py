from pydantic_settings import BaseSettings
from typing import Literal


class BaseConfig(BaseSettings):
    """Базовые настройки приложения"""

    # Окружение
    ENV: Literal["development", "production", "testing"] = "development"

    # Telegram Bot
    BOT_TOKEN: str

    # Gigachat
    GIGACHAT_CREDENTIALS: str
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1024
    MAX_HISTORY_LENGTH: int = 10

    # Логирование
    LOG_LEVEL: str = "INFO"

    # База данных
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "bot.db"
    DB_NAME: str = "bot.db"

    # Button text
    NEW_QUERY_BUTTON_TEXT: str = f"Новый{'\u3164'}запрос"

    # Other
    GITHUB_LINK: str = "https://github.com/mmagistra/gigachat_tg_bot"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def get_database_url(self) -> str:
        """Формирование URL для подключения к БД"""
        if self.ENV == "development":
            return f"sqlite+aiosqlite:///{self.DB_NAME}"
        elif self.ENV == "production":
            return (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@bot_db:5432/{self.POSTGRES_DB}"
            )
        else:
            raise ValueError(f"Неподдерживаемый тип ENV")
