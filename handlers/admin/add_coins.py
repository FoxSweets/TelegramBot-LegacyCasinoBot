from data.database import request

from aiogram import Bot, Router, html
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from keyboards.inline import accept_add_coins_keyboard
from filters.is_admin import IsAdmin

router = Router()


@router.message(Command('add_coins'), IsAdmin())
async def _add_coins(message: Message, bot: Bot, command: CommandObject):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        if not command.args:
            await message.reply('Нету аргумента\n "/add-money (@username игрока) (Число)"')
        else:
            try:
                args = command.args.split()
                user_id, coins = int(args[0]), int(args[1])

                reply_markup = accept_add_coins_keyboard(user_id, coins)

                chat_member = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
                username = chat_member.user.username

                await message.reply(f'Вы правда хотите добавить {html.bold(coins)} монет.\nигроку {html.bold(username)}', reply_markup=reply_markup)
            except ValueError:
                await message.reply("Аргументы должны быть числами")
            except IndexError:
                await message.reply('Нужно указать два аргумента: ID игрока и число.')
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()