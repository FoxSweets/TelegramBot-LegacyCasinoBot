from data.database import request

from aiogram import Router, F, Bot, html
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from keyboards import inline

router = Router()


@router.callback_query(F.data.startswith("accept_add_coins"))
async def _accept_add_coins(callback: CallbackQuery, bot: Bot):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        _, user_id, coins = callback.data.split(":")

        user_id = int(user_id)
        coins = int(coins)

        await BotDB.update_add_coins(user_id, coins)

        chat_member = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
        username = chat_member.user.username

        text = f'ID {user_id} | {username}'
        await callback.message.answer(f'Добавлено {html.bold(coins)} монет.\nигроку {html.bold(text)}')
        await bot.send_message(user_id, f'Администрация добавила вам, {html.bold(coins)} монет')
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()


@router.callback_query(F.data.startswith("accept_remove_coins"))
async def _accept_add_coins(callback: CallbackQuery, bot: Bot):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        _, user_id, coins = callback.data.split(":")

        user_id = int(user_id)
        coins = int(coins)

        await BotDB.update_remove_coins(user_id, coins)

        chat_member = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
        username = chat_member.user.username

        text = f'ID {user_id} | {username}'
        await callback.message.answer(f'Убрано {html.bold(coins)} монет.\nу игрока {html.bold(text)}')
        await bot.send_message(user_id, f'Администрация забрала у вас, {html.bold(coins)} монет')
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()