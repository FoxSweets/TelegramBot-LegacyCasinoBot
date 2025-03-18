import asyncio

from aiogram import Router, F, Bot, html, exceptions
from aiogram.types import CallbackQuery, Message

from db import requests
from games import slots
from bot.keyboards import inline

router = Router()


@router.callback_query(F.data.startswith("slots"))
async def _slots(callback: CallbackQuery):
    user_id = callback.message.chat.id
    msg = await callback.message.answer('Запуск слотов...')

    if await requests.get_balance(user_id) <= 19:
        await msg.edit_text('Не хватает средств на балансе! 😥')
        return

    text = grid = stop_columns = None
    for count in range(18):
        text, grid, stop_columns = await slots.game_slots(count, grid, stop_columns)

        await asyncio.sleep(0.2)

        if msg.text != text:  # Проверяем, изменился ли текст
            try:
                await msg.edit_text(text)
            except exceptions.TelegramBadRequest:
                pass

    result = await slots.result_slots(user_id, grid)

    text += result
    await msg.edit_text(text, reply_markup=inline.retry('slots'))