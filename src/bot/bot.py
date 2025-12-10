import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from src.config import config
from src.bot.handlers import router
from src.database.database import init_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    try:
        config.validate()
    except ValueError as e:
        logger.error(f"Ошибка конфигурации: {e}")
        return

    logger.info("Инициализация базы данных...")
    await init_db()

    bot = Bot(
        token=config.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(router)
    logger.info("Бот запущен!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()