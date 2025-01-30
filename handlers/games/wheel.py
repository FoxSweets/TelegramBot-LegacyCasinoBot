from random import choice, randint
import time
import asyncio

from data.database import request

from aiogram import Bot, Router, html
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

slots_wheel = ['🏆', '🎟', '💵', '☕', '🎃', '🃏']

win_slot_player = {
    '🏆': ['Вы выйграли 10.000 монет.', 10_000],
    '🎟': ['Вы выйграли 5.000 монет.', 5_000],
    '💵': ['Вы выйграли 1.000 монет.', 1_000],
    '☕': ['Вы выйграли чай.', 0],
    '🎃': ['Вы выйграли ничего.', 0],
    '🃏': ['Вы выйграли ничего.', 0]
}


@router.message(Command('wheel'))
async def _wheel(message: Message):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        user_id = message.from_user.id
        msg = await message.answer('Процесс...')

        if await BotDB.get_day_wheel(user_id):
            await BotDB.update_day_wheel(user_id, False)
            left_slot, player_win, player_slot, new_slot1, new_slot2 = [choice(slots_wheel) for _ in range(5)]
            wheel_scrolling = randint(25, 60)

            for _ in range(wheel_scrolling):
                text = f'{html.bold('║')}━━━━━   \\/   ━━━━━{html.bold('║')}\n{html.bold('║')} {left_slot} | {player_win} | {player_slot} | {new_slot1} | {new_slot2} {html.bold('║')}\n{html.bold('║')}━━━━━   /\\   ━━━━━{html.bold('║')}'
                await msg.edit_text(text)
                left_slot, player_win, player_slot, new_slot1, new_slot2 = player_win, player_slot, new_slot1, new_slot2, choice(slots_wheel)
            else:
                text, coins = win_slot_player[player_win]
                await BotDB.update_add_coins(user_id, coins)
                await msg.edit_text(f'WIN: {player_win}\n{text}')
        else:
            await msg.edit_text(f'Простите, но вы уже крути колесо, оно доступно один раз в сутки.')
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()
