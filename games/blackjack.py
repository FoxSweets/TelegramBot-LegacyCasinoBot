from random import choice

from aiogram import html

from db import requests

TRANSLATION_VALUES = {
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


def sum_card(cards_player):
    text = '| '
    ace, sum_values = 0, 0

    for card in cards_player:
        suit, value = card[0], card[1]  # Разделяем масть и значение
        text_translation_value = TRANSLATION_VALUES[value]  # Перевод значения в эмодзи

        # Подсчет суммы карт
        if value == '1':  # Туз
            ace += 1
        elif value in '0jqk':  # 10, валет, дама, король
            sum_values += 10
        else:
            sum_values += int(value)

        text += f'{suit}{text_translation_value} | '

    # Добавляем тузы после основных карт
    for _ in range(ace):
        sum_values += 11 if sum_values + 11 <= 21 else 1

    return text.strip(), sum_values


def new_give_card(cards_player):
    while True:
        suits = ['♠', '♣', '♥', '♦']
        values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'j', 'q', 'k']  # 0 = 10

        suit = choice(suits)
        value = choice(values)

        cards = f'{suit}{value}'
        if not cards_player:
            return cards

        if not (cards in cards_player):
            return cards


async def give_player_cards(user_id: int, money: int) -> str:
    text_card_player, bet = await requests.get_or_create_blackjack(user_id, money)

    # Создаём список карт (если пустой — делаем новый)
    cards_player = sorted(text_card_player.split(':')) if text_card_player else []

    # Исправленный блок добавления карт
    n = 2 if not cards_player else 1
    for _ in range(n):
        card = new_give_card(cards_player)  # Возвращает **ОДНУ** карту
        cards_player.append(card)

    text, sum_cards_player = sum_card(cards_player)  # Передаём список карт

    # Создаём ответ
    result = f'Рука: {text}\nЗначение карт: {sum_cards_player}'
    cards = ':'.join(cards_player)  # Сохраняем строку карт

    await requests.update_blackjack(user_id, cards)  # Обновляем в БД
    return result


async def pass_player_card(user_id: int) -> str:
    text_card_player, bet = await requests.get_or_create_blackjack(user_id)

    if not text_card_player:
        await requests.remove_blackjack(user_id)
        return 'У вас нет карт!'

    await requests.remove_money(user_id, bet)
    await requests.remove_blackjack(user_id)
    return 'Вы скинули карты!'


async def dealer_walk(user_id: int) -> str:
    text_card_player, bet = await requests.get_or_create_blackjack(user_id)

    if not text_card_player:
        await requests.remove_blackjack(user_id)
        return "У вас нет карт!"

    # Получаем карты игрока
    cards_player = text_card_player.split(":")
    cards_dealer = []

    # Логика дилера (добирает, пока < 17)
    sum_card_dealer = 0
    while sum_card_dealer < 17:
        card = new_give_card(cards_dealer + cards_player)
        cards_dealer.append(card)
        text_cards_dealer, sum_card_dealer = sum_card(cards_dealer)

    # Карты игрока
    text_cards_player, sum_card_player = sum_card(cards_player)

    # Определяем победителя
    if sum_card_player > 21:
        win_or_loss = "Дилер"
        coins = -bet
    elif sum_card_dealer > 21 or sum_card_player > sum_card_dealer:
        win_or_loss = "Игрок"
        coins = bet
    elif sum_card_player == sum_card_dealer:
        win_or_loss = "Ничья"
        coins = 0
    else:
        win_or_loss = "Дилер"
        coins = -bet

    if coins != 0:
        await requests.change_balance(user_id, coins)

    # Формируем текст результата
    n = 16 + (max(len(cards_dealer), len(cards_player)) * 8)
    win_text = f"\nВы {'выйграли' if coins > 0 else 'проиграли'} {html.bold(abs(bet))} монет" if coins != 0 else ""

    text = (
        f"Карты дилера: {text_cards_dealer}\nЗначение карт: {sum_card_dealer}\n"
        f"{'_' * n}\n"
        f"Карты игрока: {text_cards_player}\nЗначение карт: {sum_card_player}\n"
        f"{'_' * n}\n"
        f"Выйграл: {html.bold(win_or_loss)}{win_text}"
    )

    # Удаляем игру после завершения
    await requests.remove_blackjack(user_id)

    return text


