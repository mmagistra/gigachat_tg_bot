from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config.settings import settings


def get_new_query_keyboard(has_history: bool = True) -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой 'Новый запрос'"""
    placeholder = "Напишите что угодно, чтобы начать новый разговор..." if not has_history else "Напишите что угодно..."
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=settings.NEW_QUERY_BUTTON_TEXT)]
        ],
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )