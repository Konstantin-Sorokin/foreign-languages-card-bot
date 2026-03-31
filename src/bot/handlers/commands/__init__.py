from aiogram import Router

from bot.handlers.commands.base_commands import router as base_commands_router

router = Router()

router.include_routers(
    base_commands_router,
)

__all__ = [
    "router",
]
