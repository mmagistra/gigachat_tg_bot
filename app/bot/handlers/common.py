# llm_query
# Default
import logging

from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards.reply import get_new_query_keyboard
from bot.services.gigachat_service import GigachatService
from config.settings import settings
from repositories import UserRepository, UserContextRepository

router = Router()
logger = logging.getLogger(__name__)

gigachat_service = GigachatService(
    credentials=settings.GIGACHAT_CREDENTIALS,
    scope='GIGACHAT_API_PERS',
    temperature=0.7,
    max_tokens=1024,
)


@router.message(F.text == settings.NEW_QUERY_BUTTON_TEXT)
async def new_query(message: Message, user_repo: UserRepository, user_context_repo: UserContextRepository):
    """
    Обрабатывает нажатие кнопки "Новый запрос"
    Название кнопки взято из ТЗ
    На деле же кнопка очищает историю
    """
    try:
        logger.info(f"Пользователь {message.from_user.username} ({message.from_user.id}) нажал кнопку 'Новый запрос'")
        await message.answer('🧹 Очищаю историю диалога...', reply_markup=get_new_query_keyboard())
        await message.bot.send_chat_action(message.chat.id, action="typing")
        await user_context_repo.clear_context(message.from_user.id)
        await message.answer(
            '✅ История успешно очищена!\n\n'
            'Теперь мы можем начать новую беседу с чистого листа. '
            'Напиши мне что-нибудь! 💬',
            reply_markup=get_new_query_keyboard(has_history=False)
        )

    except Exception as e:
        logger.error(f"Ошибка при обращении к нейросети: {e}")
        await message.answer(
            "❌️ **Упс! Что-то пошло не так**\n\n"
            "Не удалось обработать ваш запрос. Пожалуйста, попробуйте:\n"
            "• Отправить сообщение снова\n"
            "• Начать новый диалог через /start\n\n"
            "Если проблема повторяется — сообщите разработчику 🛠️",
            reply_markup=get_new_query_keyboard(),
            parse_mode="Markdown"
        )


@router.message(F.text)
async def default(message: Message, user_repo: UserRepository, user_context_repo: UserContextRepository):
    """
    При получении любого текста от пользователя
    делает запрос к нейросети и отправляет ответ
    """
    logger.info(f"Пользователь {message.from_user.username} ({message.from_user.id}) написал: {message.text[:20]}...")
    try:
        await user_context_repo.add_message(
            user_id=message.from_user.id,
            is_from_user=True,
            message_text=message.text,
        )
    except Exception as e:
        logger.error(f"Ошибка при обращении к БД: {e}")
        await message.answer(
            "❌️ **Упс! Что-то пошло не так**\n\n"
            "Не удалось обработать ваш запрос. Пожалуйста, попробуйте:\n"
            "• Отправить сообщение снова\n"
            "• Начать новый диалог через /start\n\n"
            "Если проблема повторяется — сообщите разработчику 🛠️",
            reply_markup=get_new_query_keyboard(),
            parse_mode="Markdown"
        )
        return
    try:
        chat_context = await user_context_repo.get_context(message.from_user.id)
        await message.bot.send_chat_action(message.chat.id, action="typing")

        response = await gigachat_service.generate_response(chat_context)
        # response = f"Это ответ от нейросети"  # Заглушка

        await user_context_repo.add_message(
            user_id=message.from_user.id,
            is_from_user=False,
            message_text=response
        )

        await message.answer(
            response,
            reply_markup=get_new_query_keyboard()
        )

    except Exception as e:
        logger.error(f"Ошибка при обращении к нейросети: {e}")
        await message.answer(
            "❌️ **Упс! Что-то пошло не так**\n\n"
            "Не удалось обработать ваш запрос. Пожалуйста, попробуйте:\n"
            "• Отправить сообщение снова\n"
            "• Начать новый диалог через /start\n\n"
            "Если проблема повторяется — сообщите разработчику 🛠️",
            reply_markup=get_new_query_keyboard(),
            parse_mode="Markdown"
        )
