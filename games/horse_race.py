import random


async def race(horses: dict, rounds: int = 30) -> any:
    horse = random.randint(1, len(horses))
    horses[horse] += 1

    text = ''
    for i in range(1, len(horses) + 1):
        if horses[i] == rounds:
            text += "=" * (horses[i]) + "🐎" + "\n"
        else:
            text += "=" * (horses[i] - 1) + "🐎" + "=" * ((rounds - 1) - horses[i]) + "🏁" + "\n"

    return horses, text
