from data.database import request

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from keyboards import inline

router = Router()


def get_next_character(current_key, player_status):
    transitions = {
        'evil': 'neutral',
        'neutral': {
            'PLAYER': 'evil',
            'default': 'good'
        },
        'good': 'evil'
    }

    if current_key == 'neutral':
        return transitions['neutral'].get(player_status, transitions['neutral']['default'])
    return transitions[current_key]


@router.callback_query(F.data == "character_dealer_markup")
async def character_dealer_markup(callback: CallbackQuery):
    BotDB = request.BotBD()
    await BotDB.connect()

    try:
        user_id = callback.message.chat.id
        character = get_next_character(await BotDB.get_character_dealer(user_id), await BotDB.get_profile_status(user_id))
        await BotDB.update_character_dealer(user_id, character)

        await callback.message.edit_reply_markup(reply_markup=inline.profile_keyboard(character))
        await callback.answer()
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()