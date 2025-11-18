from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database.base import async_session_maker
from repositories import UserContextRepository
from repositories.user_repository import UserRepository
import logging

logger = logging.getLogger(__name__)


class DatabaseMiddleware(BaseMiddleware):
    """
    Middleware для создания и закрытия сессии БД
    Добавляет сессию и репозитории в data для использования в хендлерах
    (session, user_repo, user_context_repo)
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with async_session_maker() as session:
            data["session"] = session
            data["user_repo"] = UserRepository(session)
            data["user_context_repo"] = UserContextRepository(session)

            logger.debug("Создана новая сессия БД")

            try:
                result = await handler(event, data)
                return result
            except Exception as e:
                logger.error(f"Ошибка в хендлере: {e}")
                await session.rollback()
                raise
            finally:
                logger.debug("Сессия БД закрыта")
