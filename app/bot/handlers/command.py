# Start
# Help
# New query
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config.settings import settings
# from bot.services.handler_utils import
from repositories import UserRepository, UserContextRepository
from bot.keyboards.reply import get_new_query_keyboard

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, user_repo: UserRepository, user_context_repo: UserContextRepository):
    logger.info(f"Пользователь {message.from_user.username} ({message.from_user.id}) запустил команду /start")
    await message.bot.send_chat_action(message.chat.id, action="typing")
    if await user_repo.user_exists(message.from_user.id):
        await message.answer('🧹 Очищаю историю диалога...')
    await message.bot.send_chat_action(message.chat.id, action="typing")
    await user_repo.get_or_create_user(message.from_user.id, message.from_user.username)
    await user_context_repo.clear_context(message.from_user.id)
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        f"Я чат-бот на базе нейросети **GigaChat** от Сбербанка. "
        f"Я помню историю нашей беседы и могу поддержать диалог на любую тему! 💬\n\n"
        f"Напиши мне что угодно или используй /help для подробной справки.",
        reply_markup=get_new_query_keyboard(has_history=False),
        parse_mode="Markdown"
    )

    logger.info(f"Пользователь {await user_repo.get_user_by_id(message.from_user.id)} завершил команду /start")


# @router.message(Command("test"))
# async def cmd_test(message: Message):
#     logger.info(f"Пользователь {message.from_user.username} ({message.from_user.id}) запустил команду /test")
#     pass


@router.message(Command("help"))
async def cmd_help(message: Message):
    logger.info(f"Пользователь {message.from_user.username} ({message.from_user.id}) запустил команду /help")
    await message.answer(
        "ℹ️ **Как пользоваться ботом**\n\n"
        "📝 **Общение:** Просто напиши мне что угодно — я отвечу с помощью нейросети GigaChat!\n\n"
        "🧠 **Память:** Я помню контекст нашего разговора и могу отвечать на вопросы по предыдущим сообщениям.\n\n"
        "🔄 **Сброс истории:** Нажми кнопку **«Новый запрос»** или отправь команду /start, чтобы начать новый диалог.\n\n"
        "💻 **Исходный код:** Хочешь узнать, как я устроен? "
        f"Загляни в мой [GitHub]({settings.GITHUB_LINK})!\n\n"
        "Задавай любые вопросы — я готов помочь! 🚀",
        reply_markup=get_new_query_keyboard(),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )




