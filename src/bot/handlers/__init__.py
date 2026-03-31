from aiogram import Router

from bot.handlers.callbacks import router as callbacks_router
from bot.handlers.commands import router as commands_router
from bot.handlers.messages import router as messages_router

router = Router()

router.include_routers(commands_router, messages_router, callbacks_router)

__all__ = [
    "router",
]
