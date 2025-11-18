from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

engine = create_async_engine(
    url=settings.get_database_url(),
)

async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


async def create_tables():
    logger.debug('Создание таблиц...')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info('Таблицы успешно созданы')

async def drop_tables():
    logger.debug('Удаление таблиц...')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    logger.info('Таблицы успешно удалены')