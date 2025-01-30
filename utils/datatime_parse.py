from datetime import timedelta, datetime
import re


def definition_of_time(time_string: str | None) -> datetime | None:
    if not time_string:
        return None

    match_ = re.match(r'(\d+)([a-z])', time_string.lower().strip())
    current_datetime = datetime.utcnow()

    if match_:
        value, unit = int(match_.group(1)), match_.group(2)

        match unit:
            case 'h': time_delta = timedelta(hours=value)
            case 'd': time_delta = timedelta(days=value)
            case 'w': time_delta = timedelta(weeks=value)
            case _: return None
    else:
        return None

    new_datetime = (current_datetime + time_delta).replace(second=0, microsecond=0)
    return new_datetime


def x2_payday() -> int:
    today = datetime.now()
    day_week = today.weekday()

    print(day_week)
    coins = 1
    if day_week in [5, 6]:
        coins *= 2
    return coins


def time_until(target_date: str) -> str:
    target_datetime = datetime.strptime(target_date, '%Y-%m-%d %H:%M:%S')
    now = datetime.utcnow()

    delta = target_datetime - now

    years = delta.days // 365
    months = (delta.days % 365) // 30
    weeks = ((delta.days % 365) % 30) // 7
    days = ((delta.days % 365) % 30) % 7
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60

    if years > 0:
        return f'{years} год(а/лет)'
    if months > 0:
        return f'{months} месяц(а/ев)'
    if weeks > 0:
        return f'{weeks} неделя(и)'
    if days > 0:
        return f'{days} день(дней)'
    if hours > 0:
        return f'{hours} час(а/ов)'
    if minutes > 0:
        return f'{minutes} минут(ы)'