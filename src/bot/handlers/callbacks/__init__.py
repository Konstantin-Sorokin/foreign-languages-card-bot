from aiogram import Router

from bot.handlers.callbacks.card_reveal import router as card_reveal_router
from bot.handlers.callbacks.confirm_add_card import router as confirm_router
from bot.handlers.callbacks.evaluation import router as evaluation_router
from bot.handlers.callbacks.learning import router as learning_router

router = Router()

router.include_routers(
    learning_router,
    card_reveal_router,
    evaluation_router,
    confirm_router,
)

__all__ = [
    "router",
]
