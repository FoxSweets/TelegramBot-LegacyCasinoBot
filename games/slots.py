import random

from aiogram import html
from db import requests

SLOT = ['🍋', '🍇', '🌶', '🍀', '🌷', '🍁', '🥝', '🍓', '🍪', '🍰']
WEIGHTS = [1, 2, 2, 8, 8, 8, 8, 18, 18, 27]

WIN_COINS = {
    '🍋': 1000,
    '🍇': 500,
    '🌶': 500,
    '🍀': 200,
    '🌷': 200,
    '🍁': 200,
    '🥝': 200,
    '🍓': 100,
    '🍪': 100,
    '🍰': 50
}


async def game_slots(count: int, grid: list[str] = None, stop_columns: list[str] = None) -> any:
    if grid is None:
        grid = [random.choices(SLOT, weights=WEIGHTS, k=1)[0] for _ in range(9)]
        stop_columns = [False, False, False]

    text = "━━━━━━━━\n"
    for i in range(0, 9, 3):
        text += f"{grid[i]}  |  {grid[i + 1]}  |  {grid[i + 2]}\n"
    text += "━━━━━━━━"

    if (count + 1) % 6 == 0:
        stop_columns[(count // 6) % 3] = True

    if not stop_columns[0]:
        grid[6], grid[3], grid[0] = grid[3], grid[0], random.choices(SLOT, weights=WEIGHTS, k=1)[0]
    if not stop_columns[1]:
        grid[7], grid[4], grid[1] = grid[4], grid[1], random.choices(SLOT, weights=WEIGHTS, k=1)[0]
    if not stop_columns[2]:
        grid[8], grid[5], grid[2] = grid[5], grid[2], random.choices(SLOT, weights=WEIGHTS, k=1)[0]

    return text, grid, stop_columns


async def result_slots(user_id: int, grid: list[str]) -> str:
    coins = 0

    for i in range(0, 9, 3):
        if grid[i] == grid[i + 1] == grid[i + 2]:
            coins += WIN_COINS[grid[i]]

    for i in range(3):
        if grid[i] == grid[i + 3] == grid[i + 6]:
            coins += WIN_COINS[grid[i]]

    if grid[0] == grid[4] == grid[8]:  # Главная диагональ
        coins += WIN_COINS[grid[4]]
    if grid[2] == grid[4] == grid[6]:  # Побочная диагональ
        coins += WIN_COINS[grid[4]]

    if coins > 0:
        await requests.change_balance(user_id, coins)
        return f'\nРезультат: {html.bold("WIN")}🤑\nПолучено {coins}💵 монет!'
    await requests.change_balance(user_id, -20)
    return f'\nРезультат: {html.bold("LOSE")}😈'
