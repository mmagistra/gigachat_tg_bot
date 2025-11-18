import logging

from sqlalchemy import select, delete, update

from database import UserContext

logger = logging.getLogger(__name__)


class UserContextRepository:
    def __init__(self, session):
        self.session = session

    async def get_context(self, user_id) -> list[UserContext]:
        logger.debug(f"Получение истории для пользователя: {user_id}")
        result = await self.session.execute(
            select(UserContext).where(UserContext.user_id == user_id).order_by(UserContext.created_at)
        )
        return result.scalars().all()

    async def get_message(self, message_id) -> UserContext:
        logger.debug(f"Получение сообщения из истории: {message_id}")
        result = await self.session.execute(
            select(UserContext).where(UserContext.id == message_id)
        )
        return result.scalar_one_or_none()

    async def add_message(self, user_id, is_from_user, message_text) -> UserContext:
        logger.debug(f"Добавление сообщения в историю: {user_id}, {is_from_user}, {message_text[:20]}...")
        context = UserContext(user_id=user_id, is_from_user=is_from_user, message_text=message_text)
        self.session.add(context)
        await self.session.commit()
        await self.session.refresh(context)
        logger.debug(f"Сообщение добавлено в историю: {message_text[:20]}...")
        return context

    async def delete_message(self, message_id):
        logger.debug(f"Удаление сообщения из истории: {message_id}")
        await self.session.execute(
            delete(UserContext).where(UserContext.id == message_id)
        )
        await self.session.commit()
        logger.debug(f"Сообщение удалено из истории: {message_id}")

    async def update_message(self, message_id, message_text):
        logger.debug(f"Обновление сообщения в истории: {message_id}, {message_text}")
        await self.session.execute(
            update(UserContext).where(UserContext.id == message_id).values(message_text=message_text)
        )
        await self.session.commit()
        logger.debug(f"Сообщение обновлено в истории: {message_id}")

    async def clear_context(self, user_id):
        logger.debug(f"Очистка истории для пользователя: {user_id}")
        await self.session.execute(
            delete(UserContext).where(UserContext.user_id == user_id)
        )
        await self.session.commit()
        logger.debug(f"История очищена для пользователя: {user_id}")
