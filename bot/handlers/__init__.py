from aiogram import Router

from . import start, profile
from .games import slots, blackjack, horse_race


def setup_router_handler() -> Router:
    router = Router()

    router.include_routers(slots.router)
    router.include_routers(blackjack.router)
    router.include_routers(horse_race.router)

    router.include_routers(profile.router)
    router.include_routers(start.router)
    return router