from src.llm.base import BaseLLMClient
from src.llm.openai_client import OpenAIClient
from src.llm.anthropic_client import AnthropicClient
from src.config import config
import logging

logger = logging.getLogger(__name__)


class QueryParser:
    def __init__(self):
        self.llm_client: BaseLLMClient = self._get_llm_client()

    def _get_llm_client(self) -> BaseLLMClient:
        if config.LLM_PROVIDER == "openai":
            logger.info("Используется OpenAI для генерации SQL")
            return OpenAIClient()
        elif config.LLM_PROVIDER == "anthropic":
            logger.info("Используется Anthropic Claude для генерации SQL")
            return AnthropicClient()
        else:
            raise ValueError(f"Неизвестный LLM провайдер: {config.LLM_PROVIDER}")

    async def parse_question(self, question: str) -> str:
        logger.info(f"Парсинг вопроса: {question}")

        try:
            sql_query = await self.llm_client.generate_sql(question)
            logger.info(f"Сгенерирован SQL: {sql_query}")
            return sql_query
        except Exception as e:
            logger.error(f"Ошибка парсинга вопроса: {e}")
            raise