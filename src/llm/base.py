from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    @abstractmethod
    async def generate_sql(self, question: str) -> str:
        pass