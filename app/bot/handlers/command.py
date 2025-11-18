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
        await message.answer(f'Очищаю историю...')
    await message.bot.send_chat_action(message.chat.id, action="typing")
    await user_repo.get_or_create_user(message.from_user.id, message.from_user.username)
    await user_context_repo.clear_context(message.from_user.id)
    await message.answer(f"Привет, {message.from_user.first_name}! Я бот, который умеет взаимодействие с Gigachat API. "
                         f"Напиши /help, чтобы узнать, что я умею",
                         reply_markup=get_new_query_keyboard(has_history=False))

    logger.info(f"Пользователь {await user_repo.get_user_by_id(message.from_user.id)} завершил команду /start")


# @router.message(Command("test"))
# async def cmd_test(message: Message):
#     logger.info(f"Пользователь {message.from_user.username} ({message.from_user.id}) запустил команду /test")
#     pass


@router.message(Command("help"))
async def cmd_help(message: Message):
    logger.info(f"Пользователь {message.from_user.username} ({message.from_user.id}) запустил команду /help")
    await message.answer("Ты обратился за помощью? Я помогу!\n\n"
                         "Все очень просто: напиши мне что угодно и Gigachat ответит тебе. "
                         "Если ты хочешь чтобы нейросеть забыла историю переписки с тобой, "
                         "выбери 'Новый запрос' на клавиатуре или напиши /start\n\n"
                         "Если у тебя есть вопросы по теме того, как я работаю, "
                         f"то вот ссылка на github: {settings.GITHUB_LINK}."
                         "Тут ты сможешь найти мой код и более подробное описание моей работы.",
                         reply_markup=get_new_query_keyboard())


