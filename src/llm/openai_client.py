from openai import AsyncOpenAI
from src.llm.base import BaseLLMClient
from src.llm.prompts import SYSTEM_PROMPT, get_user_prompt
from src.config import config


class OpenAIClient(BaseLLMClient):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"

    async def generate_sql(self, question: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": get_user_prompt(question)}
                ],
                temperature=0,
                max_tokens=500
            )

            sql_query = response.choices[0].message.content.strip()

            if sql_query.startswith("```sql"):
                sql_query = sql_query[6:]
            if sql_query.startswith("```"):
                sql_query = sql_query[3:]
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3]

            return sql_query.strip()

        except Exception as e:
            raise Exception(f"Ошибка при генерации SQL через OpenAI: {str(e)}")