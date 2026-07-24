from aiogram import Router

from bot.handlers.commands.help import router as help_router
from bot.handlers.commands.start import router as start_router

router = Router()

router.include_router(start_router)
router.include_router(help_router)

__all__ = [
    "router",
]
