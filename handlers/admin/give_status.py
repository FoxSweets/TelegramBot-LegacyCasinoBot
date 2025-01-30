from data.database import request

from aiogram import Bot, Router, html
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from filters.is_admin import IsAdmin
from utils.datatime_parse import definition_of_time, time_until

router = Router()


@router.message(Command('give_status'), IsAdmin())
async def _give_status(message: Message, bot: Bot, command: CommandObject):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        if not command.args:
            await message.answer('Нету аргумента\n "/give-status (ID игрок) (Статус) (Период (0 или "INFINITY" - вечно))"')
        else:
            try:
                args = command.args.split()
                user_id, status, times = int(args[0]), args[1], args[2]
                reduced_time = 'INFINITY'
                text_time = ''
                if times == '0':
                    times = 'INFINITY'

                if times != 'INFINITY':
                    times = definition_of_time(times)
                    reduced_time = time_until(str(times))
                    text_time = f' ( {html.bold(times)} )'

                if status.upper() != ['ADMIN', 'VIP', 'PLAYER']:
                    await message.answer('Такой роли нет.\nМожно выдать только: ADMIN, VIP, PLAYER')
                    return

                chat_member = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
                username = chat_member.user.username

                await BotDB.update_status(user_id, status, times)
                await message.answer(f'игроку с ID: {html.bold(user_id)} | {html.bold(username)}\nВыдана роль {html.bold(status)} на {html.bold(reduced_time)}{text_time}')
            except ValueError:
                await message.answer("Аргумент ID должен быть числом")
            except IndexError:
                await message.answer('Нужно указать три аргумента:\n "/give-status (ID игрок) (Статус) (Период (0 или "INFINITY" - вечно))"')
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()