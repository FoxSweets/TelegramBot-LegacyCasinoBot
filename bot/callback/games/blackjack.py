import asyncio

from aiogram import Router, F, Bot, html
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command

from db import requests
from games import blackjack
from bot.keyboards import inline

router = Router()


@router.callback_query(F.data.startswith("blackjack_give_player_cards"))
async def _give_cards(callback: CallbackQuery):
    try:
        _, msg = callback.data.split(":")
    except ValueError:
        msg = await callback.message.answer("...")
        msg = msg.message_id

    user_id = callback.message.chat.id

    bet = 100
    balance = await requests.get_balance(user_id)
    if balance <= bet:
        await msg.edit_text('Не хватает средств на балансе! 😥')
        return

    text = await blackjack.give_player_cards(user_id, bet)
    await callback.bot.edit_message_text(chat_id=callback.message.chat.id,
                                         message_id=msg,
                                         text=text,
                                         reply_markup=inline.blackjack_keyboard(msg))


@router.callback_query(F.data.startswith("blackjack_pass_player_card"))
async def _pass_card(callback: CallbackQuery):
    _, msg = callback.data.split(":")
    user_id = callback.message.chat.id

    if await requests.get_balance(user_id) <= 99:
        await msg.edit_text('Не хватает средств на балансе! 😥')
        return

    text = await blackjack.pass_player_card(user_id)
    await callback.bot.edit_message_text(chat_id=callback.message.chat.id,
                                         message_id=msg,
                                         text=text)


@router.callback_query(F.data.startswith("blackjack_dealer_walk"))
async def _dealer_walk(callback: CallbackQuery):
    _, msg = callback.data.split(":")
    user_id = callback.message.chat.id

    text = await blackjack.dealer_walk(user_id)
    await callback.bot.edit_message_text(chat_id=callback.message.chat.id,
                                         message_id=msg,
                                         text=text)