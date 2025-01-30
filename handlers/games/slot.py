from collections import Counter
import asyncio
from cachetools import TTLCache
from datetime import datetime, timedelta

from data.database import request
from data.phrases import dealer_phrase
from utils.datatime_parse import x2_payday

from aiogram import Bot, Router, html
from aiogram.types import Message
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters import Command

from keyboards import inline

# Конфигурация кэша и ограничений по времени
COMMAND_TTL = timedelta(seconds=10)
user_command_cache = TTLCache(maxsize=1000, ttl=COMMAND_TTL.total_seconds())

router = Router()


def get_combo_text(dice_value: int):
    values = ["BAR", "виноград", "лимон", "семь"]

    dice_value -= 1
    data = []
    for _ in range(3):
        data.append(values[dice_value % 4])
        dice_value //= 4

    result = Counter(data)
    return result


@router.message(Command('game_slot'))
async def _slot(message: Message):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        member_id = message.from_user.id
        character_dealer = await BotDB.get_character_dealer(member_id)
        text = await dealer_phrase(character_dealer, 'NoMoney')

        if await BotDB.amount_coins(member_id) >= 50:
            await BotDB.update_remove_coins(member_id, 50)

            data = await message.answer_dice(DiceEmoji.SLOT_MACHINE)
            values_slot = get_combo_text(data.dice.value)

            win_player, coins = 0, 0
            for key, values in values_slot.items():
                if key == 'BAR':
                    if values == 1:
                        win_player = 1
                        coins = 30 * x2_payday()
                        await BotDB.update_add_coins(member_id, coins)
                    elif values == 2:
                        win_player = 1
                        coins = 100 * x2_payday()
                        await BotDB.update_add_coins(member_id, coins)
                    elif values == 3:
                        win_player = 1
                        coins = 300 * x2_payday()
                        await BotDB.update_add_coins(member_id, coins)
                elif key == 'виноград':
                    if values == 3:
                        win_player = 1
                        coins = 500 * x2_payday()
                        await BotDB.update_add_coins(member_id, coins)
                elif key == 'лимон':
                    if values == 3:
                        win_player = 1
                        coins = 700 * x2_payday()
                        await BotDB.update_add_coins(member_id, coins)
                elif key == 'семь':
                    if values == 3:
                        win_player = 1
                        coins = 1000 * x2_payday()
                        await BotDB.update_add_coins(member_id, coins)

            await asyncio.sleep(2)
            if win_player == 1:
                text = await dealer_phrase(character_dealer, 'win', coins)
            else:
                text = await dealer_phrase(character_dealer, 'loss')
        await message.answer(text)

    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()