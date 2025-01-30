import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from zoneinfo import ZoneInfo

from aiogram import Dispatcher, Bot

from handlers import start, echo_commands, profile_member
from handlers.games import slot, blackjack, wheel
from handlers.admin import add_coins, remove_coins, give_status, test
from handlers.work import work
from callback import profile_callback
from callback.admin import accept_coins_callback
from callback.games import blackjack_callback

from middleware.anti_flood import AntiFloodMiddleware

from services import pay_players_coins
from services import time_checks

from data.database import create


async def on_startup(bot: Bot):
    await bot.send_message(1069370364, "Бот успешно запущен! 😎")


async def on_shutdown(bot: Bot):
    await bot.send_message(1069370364, "Выключение 😰")


async def setup_dp(bot: Bot, dp: Dispatcher):
    await create.create_database()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(pay_players_coins.pay_players_coins_interval, 'interval', minutes=60, args=(bot,))
    scheduler.add_job(time_checks.check_and_update_statuses, 'interval', minutes=10, args=(bot,))

    trigger = CronTrigger(hour=0, minute=0, timezone=ZoneInfo("Etc/GMT-3"))
    scheduler.add_job(time_checks.update_day_wheel_players, trigger, args=(bot,))
    scheduler.start()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.message.middleware(AntiFloodMiddleware())

    dp.include_routers(
        add_coins.router,
        remove_coins.router,
        give_status.router,
        test.router,
        slot.router,
        blackjack.router,
        wheel.router,
        work.router,
        profile_member.router,
        start.router,
        profile_callback.router,
        accept_coins_callback.router,
        blackjack_callback.router,
        echo_commands.router,
    )