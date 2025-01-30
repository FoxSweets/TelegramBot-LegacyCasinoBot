from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message

from data.database import request


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        BotDB = request.BotBD()
        await BotDB.connect()
        try:
            return message.from_user.id in await BotDB.get_all_admins()
        except Exception as ex:
            print(ex)
        finally:
            await BotDB.close_database()