from aiogram import Router

from bot.handlers.messages.add_card import router as add_card_router
from bot.handlers.messages.card_type_selection import router as card_type_router

router = Router()

router.include_routers(
    card_type_router,
    add_card_router,
)

__all__ = [
    "router",
]