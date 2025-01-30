from data.database import request

from aiogram import Bot, Router, html
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from filters.is_admin import IsAdmin

from keyboards import inline

router = Router()


@router.message(Command('test'), IsAdmin())
async def test(message: Message):
    chat_member = await message.bot.get_chat(4594507870)
    await message.answer(str(chat_member))