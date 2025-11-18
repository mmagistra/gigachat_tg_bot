import logging
from typing import Optional

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import User

logger = logging.getLogger(__name__)


class UserRepository:
    """
    Репозиторий для работы с пользователями
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def user_exists(self, user_id: int) -> bool:
        logger.debug(f"Проверка существования пользователя: {user_id}")
        result = await self.session.execute(
            select(User).where(User.user_id == user_id)
        )
        return bool(result.scalar_one_or_none())

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        logger.debug(f"Получение пользователя по id: {user_id}")
        result = await self.session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        logger.debug(f"Получение пользователя по username: {username}")
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_id: int, username: str) -> User:
        logger.debug(f"Создание пользователя: {user_id }, {username}")
        user = User(user_id=user_id, username=username)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.debug(f"Создан новый пользователь: {user_id}")
        return user

    async def get_or_create_user(self, user_id: int, username: str) -> User:
        logger.debug(f"Получение или создание пользователя: {user_id}, {username}")
        user = await self.get_user_by_id(user_id)
        if user:
            await self.update_user(user_id, username)
            return user
        return await self.create_user(user_id, username)

    async def update_user(self, user_id: int, username: str):
        logger.debug(f"Обновление пользователя: {user_id}, {username}")
        await self.session.execute(
            update(User).where(User.user_id == user_id).values(username=username)
        )
        await self.session.commit()
        logger.debug(f"Пользователь обновлен: {user_id}")

    async def delete_user(self, user_id: int):
        logger.debug(f"Удаление пользователя: {user_id}")
        await self.session.execute(
            delete(User).where(User.user_id == user_id)
        )
        await self.session.commit()
        logger.debug(f"Пользователь удален: {user_id}")
