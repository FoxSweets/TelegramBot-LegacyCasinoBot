from aiogram import Bot, html
from datetime import datetime

from data.database import request


async def check_and_update_statuses(bot: Bot):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        current_time = datetime.utcnow()

        users = await BotDB.get_all_users_status()
        for user_id, user_status_time in users:
            user_status_time = datetime.strptime(user_status_time, "%Y-%m-%d %H:%M:%S")
            if user_status_time <= current_time:
                await BotDB.update_status(user_id, 'PLAYER', 'INFINITY')
                await BotDB.update_character_dealer(user_id, 'neutral')
                await bot.send_message(user_id, f'Вы снова стали {html.bold('PLAYER')}')
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()


async def update_day_wheel_players(bot: Bot):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        users = await BotDB.get_all_users()
        for user_id in users:
            await BotDB.update_day_wheel(user_id, True)
            await bot.send_message(user_id, f'{html.bold('КОЛЕСО ФОРТУНЫ')} обновлено\nВы можете снова крутить его командой: {html.blockquote('/wheel')}')
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()