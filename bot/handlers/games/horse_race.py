import asyncio

from aiogram import Router, Bot, html
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from db import requests
from games import horse_race

router = Router()


@router.message(Command("horse_race"))
async def _start_horse(message: Message, command: CommandObject):
    user_id = message.from_user.id
    args = command.args.split() if command.args else []

    if not args:
        await message.reply("Ошибка! Укажите номер лошади и (необязательно) ставку.\nПример: `/horse_race 3 100`")
        return

    try:
        horse_number = int(args[0])
        if horse_number not in range(1, 5):  # Лошадей 4, поэтому номер должен быть от 1 до 4
            raise ValueError("Некорректный номер лошади")

        bet = int(args[1]) if len(args) > 1 else 100
        if bet <= 0:
            raise ValueError("Ставка должна быть больше 0")
    except ValueError:
        await message.reply("Ошибка! Укажите корректные числа (номер лошади от 1 до 4, ставка > 0).")
        return

    balance = await requests.get_balance(user_id)
    if balance < bet:
        await message.reply(f"Недостаточно средств! Ваш баланс: {balance} монет.")
        return

    await requests.get_or_create_horse_race(user_id, horse_number, bet)
    await message.reply(f"Вы выбрали лошадь №{horse_number} с ставкой {bet} монет.")

    horses = {i: 1 for i in range(1, 5)}
    rounds = 10

    msg = await message.answer("Запуск гонки...")
    while True:
        horses, text = await horse_race.race(horses, rounds)
        await msg.edit_text(text)
        await asyncio.sleep(0.2)

        for k, v in horses.items():
            if v >= rounds:
                stored_horse, stored_bet = await requests.get_or_create_horse_race(user_id, horse_number, bet)

                if stored_horse == k:
                    await requests.change_balance(user_id, stored_bet)
                    result_text = f"Поздравляем! 🎉 Ваша лошадь №{k} победила!\nВы выиграли {stored_bet} монет к поставленной ставки!"
                else:
                    await requests.change_balance(user_id, stored_bet)
                    result_text = f"Увы! Победила лошадь №{k}. 😞 Вы проиграли {stored_bet} монет."

                await requests.remove_horse_race(user_id)
                await msg.edit_text(result_text)
                return
