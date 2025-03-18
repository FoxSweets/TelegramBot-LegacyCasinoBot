from aiogram import Router, Bot, html
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from db import requests

from bot.keyboards import inline

router = Router()


@router.message(CommandStart())
async def _start(message: Message):
    msg = await message.answer('...')

    text = f"Добро пожаловать в казино {html.bold('FoxNightCasino')} 🎃.\nЯ ваш личный дилер, моё имя {html.bold('Джон 2.0')} 🃏\n\n"

    if await requests.create_user(user_id=message.from_user.id):
        text += f"Новичкам дают:\n- 1000 монет 💵\n- статус 'PLAYER' 😎"

    await msg.edit_text(text, reply_markup=inline.start_menu(msg.message_id))
