import asyncio
import logging
from functools import partial
from typing import List

from gigachat import GigaChat
from gigachat.models import Messages, MessagesRole, Chat

from config.settings import settings
from database import UserContext

logger = logging.getLogger(__name__)


class GigachatService:
    """
    Класс для работы с сервисом Gigachat
    """
    def __init__(
            self, credentials: str, scope: str='GIGACHAT_API_PERS',
            temperature: float=settings.TEMPERATURE,
            max_tokens: int=settings.MAX_TOKENS
    ):
        self.credentials = credentials
        self.scope = scope
        self.temperature = temperature
        self.max_tokens = max_tokens
        logger.info("GigachatService инициализирован")

    def change_temperature(self, temperature: float=settings.TEMPERATURE):
        self.temperature = temperature

    def change_max_tokens(self, max_tokens: int=settings.MAX_TOKENS):
        self.max_tokens = max_tokens

    async def generate_response(self, context: List[UserContext]) -> str:
        """Генерирует ответ от нейросети на базе истории сообщений"""
        logger.debug(f"Получение истории: {context[-1].message_text[:20]}...")
        history = [
            Messages(
                role=MessagesRole(MessagesRole.USER
                                  if msg.is_from_user
                                  else MessagesRole.ASSISTANT
                                  ),
                content=msg.message_text
            )
            for msg in context
        ]
        history = history[settings.MAX_HISTORY_LENGTH*-1:]

        loop = asyncio.get_event_loop()

        # Запускаем синхронный запрос в executor (не блокирует event loop)
        response = await loop.run_in_executor(
            None,
            partial(
                self._sync_generate,
                history=history,
            )
        )
        return response

    def _sync_generate(self, history: List[Messages]) -> str:
        """Метод для выполнения синхронного запроса к Gigachat."""
        try:
            with GigaChat(
                credentials=self.credentials,
                scope=self.scope,
                verify_ssl_certs=False
            ) as giga:
                logger.info(f"Создание чата с {self.temperature} температурой и {self.max_tokens} токенами")
                chat = Chat(messages=history, temperature=self.temperature, max_tokens=self.max_tokens)

                logger.info(f"Запрос к Gigachat из истории в {len(history)} сообщений")
                response = giga.chat(chat)

                answer = response.choices[0].message.content
                return answer
        except Exception as e:
            logger.error(f"Ошибка при обращении к Gigachat: {e}")
            raise e
