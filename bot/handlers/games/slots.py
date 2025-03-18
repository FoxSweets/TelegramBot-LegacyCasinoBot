import asyncio

from aiogram import Router, Bot, html, exceptions
from aiogram.types import Message
from aiogram.filters import Command

from db import requests
from games import slots

router = Router()


@router.message(Command("slots"))
async def _slots(message: Message):
    user_id = message.from_user.id
    if await requests.get_balance(user_id) <= 19:
        await message.reply('Не хватает средств на балансе! 😥')
        return

    msg = await message.answer('Запуск слотов...')
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
    await msg.edit_text(text)
