from aiogram import Router

from . import menu
from .games import blackjack, slots


def setup_router_callback() -> Router:
    router = Router()

    router.include_routers(menu.router)
    router.include_routers(slots.router)
    router.include_routers(blackjack.router)
    return router