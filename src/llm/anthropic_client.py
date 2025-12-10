from anthropic import AsyncAnthropic
from src.llm.base import BaseLLMClient
from src.llm.prompts import SYSTEM_PROMPT, get_user_prompt
from src.config import config


class AnthropicClient(BaseLLMClient):
    def __init__(self):
        self.client = AsyncAnthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = "claude-3-5-haiku-20241022"

    async def generate_sql(self, question: str) -> str:
        try:
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0,  # Детерминированный вывод
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": get_user_prompt(question)}
                ]
            )

            sql_query = message.content[0].text.strip()

            if sql_query.startswith("```sql"):
                sql_query = sql_query[6:]
            if sql_query.startswith("```"):
                sql_query = sql_query[3:]
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3]

            return sql_query.strip()

        except Exception as e:
            raise Exception(f"Ошибка при генерации SQL через Anthropic: {str(e)}")