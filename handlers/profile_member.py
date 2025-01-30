from data.database import request
from utils.datatime_parse import time_until

from aiogram import Bot, Router, html
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import inline

router = Router()


@router.message(Command('profile'))
async def _profile(message: Message, bot: Bot):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        member_id = message.from_user.id
        name, status, date_status, LocalBoost, date_LocalBoost, coins, CharacterDealer = await BotDB.users_profile(member_id)

        if not (date_status == 'INFINITY'):
            date_status = time_until(date_status)

        if not (date_LocalBoost == 'INFINITY'):
            date_LocalBoost = time_until(date_LocalBoost)

        text = f'👾Имя: {html.bold(name)}\n\n☣Статус: {html.bold(status)} | {html.bold(date_status)}\n\n🔼Буст монет: {html.bold(LocalBoost)} | {html.bold(date_LocalBoost)}\n💵Монеты: {html.bold(coins)}'

        user_profile_photos = await bot.get_user_profile_photos(member_id)
        if user_profile_photos.total_count > 0:
            await message.answer_photo(
                user_profile_photos.photos[0][0].file_id,
                text,
                reply_markup=inline.profile_keyboard(CharacterDealer)
            )
        else:
            await message.answer(
                text
            )
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()