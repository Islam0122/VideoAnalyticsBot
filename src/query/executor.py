from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)


class QueryExecutor:
    """Исполнитель SQL запросов"""

    async def execute(self, session: AsyncSession, sql_query: str) -> int:
        """
        Выполнить SQL запрос и вернуть результат

        Args:
            session: Асинхронная сессия БД
            sql_query: SQL запрос

        Returns:
            Число - результат запроса

        Raises:
            Exception: При ошибке выполнения запроса
        """
        try:
            logger.info(f"Выполнение SQL: {sql_query}")

            # Проверка на потенциально опасные операции
            dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE', 'CREATE']
            sql_upper = sql_query.upper()

            # Разбиваем на слова и проверяем только целые слова
            import re
            sql_words = set(re.findall(r'\b\w+\b', sql_upper))

            for keyword in dangerous_keywords:
                if keyword in sql_words:
                    raise ValueError(f"Запрос содержит запрещенную операцию: {keyword}")

            # Выполнение запроса
            result = await session.execute(text(sql_query))
            row = result.fetchone()

            if row is None:
                logger.warning("Запрос не вернул результатов")
                return 0

            # Получаем первое значение из строки
            value = row[0]

            try:
                return int(value)
            except (ValueError, TypeError):
                logger.error(f"Не удалось преобразовать результат в число: {value}")
                raise ValueError(f"Результат запроса не является числом: {value}")

        except Exception as e:
            logger.error(f"Ошибка выполнения SQL: {e}")
            raise