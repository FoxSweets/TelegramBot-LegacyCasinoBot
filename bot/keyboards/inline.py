from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def start_menu(msg):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'Игры 🎰', callback_data=f'game_menu:{msg}'),
                InlineKeyboardButton(text=f'Помощь 😣', callback_data=f'help:{msg}'),
            ],
            [
                InlineKeyboardButton(text=f"Профиль 🎃", callback_data=f'profile:{msg}')
            ]
        ]
    )
    return main


def game_menu():
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'🎰', callback_data='slots'),
                InlineKeyboardButton(text=f'🃏', callback_data='blackjack_give_player_cards'),
            ]
        ]
    )
    return main


def blackjack_keyboard(msg):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'🃏', callback_data=f'blackjack_give_player_cards:{msg}'),
                InlineKeyboardButton(text=f'🤵', callback_data=f'blackjack_dealer_walk:{msg}'),
                InlineKeyboardButton(text=f'❌', callback_data=f'blackjack_pass_player_card:{msg}'),
            ]
        ]
    )
    return main


def retry(game):
    main = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'🔄', callback_data=f'{game}'),
                InlineKeyboardButton(text=f"🎃", callback_data=f'profile')
            ]
        ]
    )
    return main