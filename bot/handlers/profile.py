from aiogram import Router, Bot, html
from aiogram.types import Message
from aiogram.filters import Command

from db import requests

from bot.keyboards import inline

router = Router()


@router.message(Command("profile"))
async def _profile(message: Message):
    user_id = message.from_user.id
    username = message.from_user.full_name
    status, balance = await requests.profile(user_id)
    await message.answer(text=f"━━━━━━━━━━━━━━━━━\n"
                              f"👤 {html.bold('Имя')}: {html.code(username)}\n"
                              f"🆔 {html.bold('ID')}: {html.code(user_id)}\n"
                              f"━━━━━━━━━━━━━━━━━\n"
                              f"📜 {html.bold('Статус')}: {html.code(status)}\n"
                              f"💰 {html.bold('Баланс')}: {html.code(balance)}\n"
                              f"━━━━━━━━━━━━━━━━━")
