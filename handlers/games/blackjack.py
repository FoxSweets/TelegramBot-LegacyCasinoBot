import json
import os
from random import choice

from data.database import request

from aiogram import Bot, Router, html
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject

from callback.games.blackjack_callback import give_cards
from keyboards import inline

router = Router()


def read_cards(user_id):
    with open(f'data/users/{user_id}.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
        return data['game']


def write_json(user_id: int, msg: int, coins: int):
    data = {
        'game': 'Blackjack',
        'username': user_id,
        'coins': coins,
        'message': msg,
        'cards_player': '',
        'cards_dealer': '',
    }

    with open(f'data/users/{user_id}.json', 'w', encoding='UTF-8') as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))


async def buy_game(user_id: int, coins: int):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        coins_user_amount = await BotDB.amount_coins(user_id)
        if not (coins_user_amount >= coins):
            return True
        await BotDB.update_remove_coins(user_id, coins)
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()


@router.message(Command('blackjack'))
async def _blackjack(message: Message, command: CommandObject):
    user_id = message.from_user.id
    try:
        coins = int(command.args.split()[0])
    except AttributeError:
        coins = 100

    if not os.path.exists(f'data/users/{user_id}.json'):
        if await buy_game(user_id, coins):
            await message.answer('У вас нет монет!')
            return
        msg = await message.answer('Процесс...', reply_markup=inline.blackjack_keyboard())
        write_json(user_id, msg.message_id, coins)

    if read_cards(user_id) == 'Blackjack':
        fake_callback_query = CallbackQuery(
            id='fake_id',
            from_user=message.from_user,
            message=message,
            chat_instance='fake_chat_instance',
            data='give_cards',
        )
        await give_cards(fake_callback_query, message.bot)
    else:
        await message.answer('Вы уже играете в другую игру.')