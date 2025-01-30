import random
from data.database import request

from aiogram import Bot, Router, html
from aiogram.types import Message
from aiogram.filters import Command

from filters.is_admin import IsAdmin

router = Router()


@router.message(Command('work'))
async def _work(message: Message):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        member_id = message.from_user.id
        coins = random.randint(30, 200)
        await BotDB.update_add_coins(member_id, coins)
        await message.answer(f'Вы заработали {coins} монет 💵')
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()