from tortoise.expressions import F

from db import User, Blackjack, HorseRace
from typing import Optional, Tuple


async def create_user(user_id: int) -> bool:
    """Создаёт пользователя, если он не существует."""
    if await User.get_or_none(id=user_id):
        return False

    await User.create(id=user_id, status="PLAYER", balance=1000)
    return True


async def profile(user_id: int) -> Optional[Tuple[str, int]]:
    """Возвращает статус и баланс пользователя."""
    user = await User.filter(id=user_id).values_list("status", "balance")
    return user[0]


async def get_or_create_blackjack(user_id: int, money: int = 0) -> Tuple[str, int]:
    """Возвращает текущую игру в блэкджек или создаёт новую."""
    user = await Blackjack.get_or_none(id=user_id)
    if user:
        return user.cards, user.bet

    await Blackjack.create(id=user_id, cards="", bet=money)
    return "", money


async def update_blackjack(user_id: int, cards: str) -> None:
    """Обновляет карты пользователя в блэкджеке."""
    if user := await Blackjack.get_or_none(id=user_id):
        user.cards = cards
        await user.save()


async def remove_blackjack(user_id: int) -> None:
    """Удаляет запись блэкджека пользователя, если она существует."""
    if user := await Blackjack.get_or_none(id=user_id):
        await user.delete()


async def get_or_create_horse_race(user_id: int, horse_num: int = 0, money: int = 0) -> Tuple[int, int]:
    """Возвращает текущую ставку на лошадь или создаёт новую."""
    race = await HorseRace.get_or_none(id=user_id)
    if race:
        return race.horse_number, race.bet

    await HorseRace.create(id=user_id, horse_number=horse_num, bet=money)
    return horse_num, money


async def remove_horse_race(user_id: int) -> None:
    """Удаляет ставку пользователя на лошадь, если она есть."""
    if race := await HorseRace.get_or_none(id=user_id):
        await race.delete()


async def get_balance(user_id: int) -> int:
    """Возвращает баланс пользователя, если он существует, иначе 0."""
    user = await User.get_or_none(id=user_id)
    return user.balance if user else 0


async def change_balance(user_id: int, amount: int) -> None:
    """Изменяет баланс пользователя. Если amount < 0 — снимает деньги, но не даёт уйти в минус."""
    await User.filter(id=user_id).update(balance=F('balance') + amount)
    await User.filter(id=user_id, balance__lt=0).update(balance=0)  # Если баланс стал < 0, вернуть 0
