from aiogram import Router

from bot.handlers.callbacks.add_card import router as confirm_router
from bot.handlers.callbacks.learning_ivc import router as learning_ivc_router
from bot.handlers.callbacks.learning_tc import router as learning_tc_router

router = Router()

router.include_routers(
    learning_tc_router,
    learning_ivc_router,
    confirm_router,
)

__all__ = [
    "router",
]
