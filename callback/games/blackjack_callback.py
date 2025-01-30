import json
import os
from random import choice

from data.database import request
from utils.datatime_parse import x2_payday

from aiogram import Router, F, Bot, html
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from keyboards import inline

router = Router()

translation_values = {
    '1': '🃏',  # 1 or 11
    '2': '2️⃣',
    '3': '3️⃣',
    '4': '4️⃣',
    '5': '5️⃣',
    '6': '6️⃣',
    '7': '7️⃣',
    '8': '8️⃣',
    '9': '9️⃣',
    '0': '🔟',
    'j': '👳',  # 10
    'q': '👸',  # 10
    'k': '🤴',  # 10
}


def get_combo_text():
    """
    Создаёт и даёт комбинацию карт.
    Формат масть|значение
    """
    suits = ['♠', '♣', '♥', '♦']
    values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'j', 'q', 'k']  # 0 = 10

    suit = choice(suits)
    value = choice(values)
    return suit, value, translation_values[value]


def read_cards(user_id):
    with open(f'data/users/{user_id}.json', 'r', encoding='UTF-8') as file:
        data = json.load(file)
        if data['cards_player']:
            return sorted(data['cards_player'].split(':')), data['message'], data['coins']
    return [], data['message'], data['coins']


def write_json(user_id, cards, msg, coins):
    data = {
        'game': 'Blackjack',
        'username': user_id,
        'coins': coins,
        'message': msg,
        'cards_player': f'{cards}',
        'cards_dealer': '',
    }

    with open(f'data/users/{user_id}.json', 'w', encoding='UTF-8') as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))


def sum_card(cards_player):
    text = '|'
    ace, sum_values = 0, 0
    for i in cards_player:
        text_suit, text_translation_value = i[0], translation_values[i[1]]
        if i[1] == '1':
            ace += 1
        elif i[1] in ['0', 'j', 'q', 'k']:
            sum_values += 10
        else:
            sum_values += int(i[1])

        text += f'{text_suit}{text_translation_value}|'
    for _ in range(ace):
        sum_values += 11 if sum_values + 11 <= 21 else 1
    return text, sum_values


def new_give_card(cards_player):
    while True:
        suit, value, translation_value = get_combo_text()
        cards = f'{suit}{value}'
        if not cards_player:
            return cards

        if not (cards in cards_player):
            return cards


async def win_player(user_id: int, coins: int):
    BotDB = request.BotBD()
    await BotDB.connect()
    try:
        await BotDB.update_add_coins(user_id, coins)
    except Exception as ex:
        print(ex)
    finally:
        await BotDB.close_database()


@router.callback_query(F.data.startswith("give_cards"))
async def give_cards(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    card_player, msg, coins = read_cards(user_id)

    # начало перебора и выдачи значения пользователю.
    n = 2 if not card_player else 1
    for _ in range(n):
        cards = new_give_card(card_player)
        card_player.append(cards)

    text, sum_card_player = sum_card(card_player)

    text = f'Рука: {text}\nЗначение карт: {sum_card_player}'
    await bot.edit_message_text(text, chat_id=callback.message.chat.id, message_id=msg, reply_markup=inline.blackjack_keyboard())
    if sum_card_player == 21:
        await bot.edit_message_text('Вы выйграли у вас 21!', chat_id=callback.message.chat.id, message_id=msg)
        coins *= x2_payday()
        await win_player(user_id, coins)
        os.remove(f'data/users/{user_id}.json')
    elif sum_card_player > 21:
        await bot.edit_message_text('Вы проиграли у вас больше 21!', chat_id=callback.message.chat.id, message_id=msg)
        os.remove(f'data/users/{user_id}.json')
    else:
        cards = ':'.join(card_player)
        write_json(user_id, cards, msg, coins)


@router.callback_query(F.data.startswith("pass_card"))
async def _pass_card(callback: CallbackQuery):
    user_id = callback.message.chat.id
    cards, msg, coins = read_cards(user_id)
    if os.path.exists(f'data/users/{user_id}.json'):
        os.remove(f'data/users/{user_id}.json')
        await callback.bot.edit_message_text('Вы скинули карты!', chat_id=callback.message.chat.id, message_id=msg)
    else:
        await callback.bot.edit_message_text('У вас нет карт!', chat_id=callback.message.chat.id, message_id=msg)


@router.callback_query(F.data.startswith("dealer_walk"))
async def _dealer_walk(callback: CallbackQuery):
    user_id = callback.message.chat.id
    cards_player, msg, coins = read_cards(user_id)
    if cards_player:
        cards_dealer = []

        sum_card_dealer = 0
        while sum_card_dealer < 17:
            cards = new_give_card((cards_dealer + cards_player))
            cards_dealer.append(cards)
            text_cards_dealer, sum_card_dealer = sum_card(cards_dealer)

        text_cards_dealer = f'Карты дилера: {text_cards_dealer}\nЗначение карт: {sum_card_dealer}'

        text_cards_player, sum_card_player = sum_card(cards_player)
        text_cards_player = f'Карты игрока: {text_cards_player}\nЗначение карт: {sum_card_player}'

        if sum_card_dealer > 21:
            win_or_loss = 'Игрок'
            coins *= (2 * x2_payday())
            win_text = f'\nВы выйграли {html.bold(coins)} монет'
            await win_player(user_id, coins)
        elif sum_card_player > sum_card_dealer:
            win_or_loss = 'Игрок'
            coins *= (2 * x2_payday())
            win_text = f'\nВы выйграли {html.bold(coins)} монет'
            await win_player(user_id, coins)
        elif sum_card_player == sum_card_dealer:
            win_or_loss = 'Ничья'
            win_text = f'\nВы выйграли {html.bold(coins)} монет'
            await win_player(user_id, coins)
        else:
            win_or_loss = 'Дилер'
            win_text = ''

        n = 16 + (max([len(cards_dealer), len(cards_player)]) * 8)
        await callback.bot.edit_message_text(f'{text_cards_dealer}\n{'_' * n}\n{text_cards_player}\n{'_' * n}\nВыйграл: {html.bold(win_or_loss)}{win_text}', chat_id=callback.message.chat.id, message_id=msg)
        os.remove(f'data/users/{user_id}.json')
    else:
        await callback.bot.edit_message_text('У вас нету карт!', chat_id=callback.message.chat.id, message_id=msg)
