import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.settings import settings
from database.base import create_tables, engine
from bot.handlers import command, common
from bot.middlewares.db_session_middleware import DatabaseMiddleware
from utils.logger import logger


dp = Dispatcher(storage=MemoryStorage())


@dp.startup()
async def on_startup():
    logger.info(f"\n{'=' * 60}\n"
                f"ЗАПУСК БОТА В РЕЖИМЕ: {settings.ENV}\n"
                f"{'=' * 60}")

    # Создание таблиц
    await create_tables()
    logger.info("База данных готова к работе!")


@dp.shutdown()
async def on_shutdown():
    logger.info(f"\n{'=' * 60}\n"
                f"ОСТАНОВКА БОТА...\n"
                f"{'=' * 60}\n")

    await engine.dispose()
    logger.info("Соединение с БД закрыто")


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # middlewares
    dp.message.middleware(DatabaseMiddleware())
    logger.info("Миддлвары зарегистрированы")

    # routers
    dp.include_router(command.router)
    dp.include_router(common.router)
    logger.info("Роутеры зарегистрированы")

    try:
        logger.info("Запуск polling...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.exception(f"Критическая ошибка: {e}")
