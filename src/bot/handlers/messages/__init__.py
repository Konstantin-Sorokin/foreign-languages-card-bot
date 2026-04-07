from aiogram import Router

from bot.handlers.messages.add_card import router as add_card_router
from bot.handlers.messages.learning_choice import router as select_learning_router

router = Router()

router.include_routers(
    select_learning_router,
    add_card_router,
)

__all__ = [
    "router",
]
