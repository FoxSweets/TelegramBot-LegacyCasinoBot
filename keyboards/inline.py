from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def profile_keyboard(character):
    character_dealer = {
        'evil': 'Злой',
        'neutral': 'Нейтральный',
        'good': 'Добрый'
    }

    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Дилер: {character_dealer[character]}', callback_data='character_dealer_markup'),
            ]
        ]
    )
    return main


def accept_add_coins_keyboard(user_id, coins):
    callback_data = f'accept_add_coins:{user_id}:{coins}'

    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'✅Подтвердить', callback_data=callback_data),
            ]
        ]
    )
    return main


def accept_remove_coins_keyboard(user_id, coins):
    callback_data = f'accept_remove_coins:{user_id}:{coins}'

    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'✅Подтвердить', callback_data=callback_data),
            ]
        ]
    )
    return main


def blackjack_keyboard():

    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'🃏', callback_data='give_cards'),
                InlineKeyboardButton(text=f'🤵', callback_data='dealer_walk'),
                InlineKeyboardButton(text=f'❌', callback_data='pass_card'),
            ]
        ]
    )
    return main