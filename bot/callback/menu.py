import asyncio

from aiogram import Router, F, Bot, html
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command

from db import requests
from games import blackjack
from bot.keyboards import inline

router = Router()


@router.callback_query(F.data.startswith("game_menu"))
async def _give_cards(callback: CallbackQuery):
    try:
        _, msg = callback.data.split(":")
    except ValueError:
        msg = await callback.message.answer("...")
        msg = msg.message_id

    text = '🎰 - слоты\n🃏 - 21'
    await callback.bot.edit_message_text(chat_id=callback.message.chat.id,
                                         message_id=msg,
                                         text=text,
                                         reply_markup=inline.game_menu())

    await callback.answer()


@router.callback_query(F.data.startswith("profile"))
async def _profile(callback: CallbackQuery):
    try:
        _, msg = callback.data.split(":")
    except ValueError:
        msg = await callback.message.answer("...")
        msg = msg.message_id

    user_id = callback.message.chat.id
    username = callback.message.chat.full_name

    status, balance = await requests.profile(user_id)
    await callback.bot.edit_message_text(chat_id=callback.message.chat.id,
                                         message_id=msg,
                                         text=f"━━━━━━━━━━━━━━━━━\n"
                                              f"👤 {html.bold('Имя')}: {html.code(username)}\n"
                                              f"🆔 {html.bold('ID')}: {html.code(user_id)}\n"
                                              f"━━━━━━━━━━━━━━━━━\n"
                                              f"📜 {html.bold('Статус')}: {html.code(status)}\n"
                                              f"💰 {html.bold('Баланс')}: {html.code(balance)}\n"
                                              f"━━━━━━━━━━━━━━━━━\n")

    await callback.answer()