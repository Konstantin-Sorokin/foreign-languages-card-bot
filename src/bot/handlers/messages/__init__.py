from aiogram import Router

from bot.handlers.messages.learning_choice import router as select_learning_router

router = Router()

router.include_routers(
    select_learning_router,
)

__all__ = [
    "router",
]
