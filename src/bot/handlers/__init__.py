from aiogram import Router

from bot.handlers.add import router as add_router
from bot.handlers.commands import router as commands_router
from bot.handlers.learning import router as learning_router

router = Router()

router.include_router(commands_router)
router.include_router(learning_router)
router.include_router(add_router)


__all__ = [
    "router",
]
