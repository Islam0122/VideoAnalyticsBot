from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from src.database.database import AsyncSessionLocal
from src.query.parser import QueryParser
from src.query.executor import QueryExecutor
import logging

logger = logging.getLogger(__name__)
router = Router()

query_parser = QueryParser()
query_executor = QueryExecutor()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для аналитики по видео.\n\n"
        "Задавайте мне вопросы на русском языке, например:\n"
        "• Сколько всего видео есть в системе?\n"
        "• Сколько видео у креатора с id 123?\n"
        "• Сколько видео набрало больше 100000 просмотров?\n"
        "• На сколько просмотров выросли все видео 28 ноября 2025?\n\n"
        "Я отвечу одним числом 📊"
    )


@router.message(F.text)
async def handle_question(message: Message):
    question = message.text.strip()

    if not question:
        await message.answer("❌ Пустой вопрос. Пожалуйста, задайте вопрос.")
        return

    logger.info(f"Получен вопрос от пользователя {message.from_user.id}: {question}")

    await message.bot.send_chat_action(message.chat.id, "typing")

    try:
        sql_query = await query_parser.parse_question(question)
        async with AsyncSessionLocal() as session:
            result = await query_executor.execute(session, sql_query)

        logger.info(f"Результат для пользователя {message.from_user.id}: {result}")
        await message.answer(str(result))

    except ValueError as e:
        logger.error(f"Ошибка валидации: {e}")
        await message.answer(f"❌ Ошибка: {str(e)}")

    except Exception as e:
        logger.error(f"Ошибка обработки вопроса: {e}", exc_info=True)
        await message.answer(
            "❌ Произошла ошибка при обработке вашего вопроса.\n"
            "Попробуйте переформулировать или упростить вопрос."
        )