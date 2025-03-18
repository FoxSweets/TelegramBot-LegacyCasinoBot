import asyncio

from aiogram import Router, Bot, html, exceptions
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from db import requests
from games import blackjack
from bot.keyboards import inline

router = Router()


@router.message(Command("blackjack"))
async def _blackjack(message: Message, command: CommandObject):
    user_id = message.from_user.id
    args = command.args.split() if command.args else []

    try:
        bet = int(args[0]) if len(args) >= 1 else 100
        if bet <= 0:
            raise ValueError("Ставка должна быть больше 0")
    except ValueError:
        await message.reply("Ошибка! Укажите корректное число.")
        return

    balance = await requests.get_balance(user_id)
    if balance < bet:
        await message.reply(f"Недостаточно средств! Ваш баланс: {balance} монет.")
        return

    msg = await message.answer('Запуск слотов...')
    text = await blackjack.give_player_cards(user_id, bet)
    await msg.edit_text(text, reply_markup=inline.blackjack_keyboard(msg.message_id))
