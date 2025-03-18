import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from tortoise import Tortoise

from bot.callback import setup_router_callback
from bot.handlers import setup_router_handler

from config import LOG_LEVEL, config


async def on_startup(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)

    await Tortoise.init(
        db_url=config.DB_URL.get_secret_value(),
        modules={"models": ["db.models"]}
    )
    await Tortoise.generate_schemas()


async def on_shutdown():
    await Tortoise.close_connections()


async def main():
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    bot = Bot(config.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage())

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_routers(setup_router_callback())
    dp.include_routers(setup_router_handler())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass