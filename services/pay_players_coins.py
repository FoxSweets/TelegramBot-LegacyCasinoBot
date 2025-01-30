from aiogram import Bot
from datetime import datetime

from data.database import request
from utils.datatime_parse import x2_payday


async def pay_players_coins_interval(bot: Bot):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        coins = 500 * x2_payday()

        for users in await BotDB.get_all_users():
            await BotDB.update_add_coins(users, coins)
            await bot.send_message(users, f'Вам начислено {coins} монет, как участнику клуба!')
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()