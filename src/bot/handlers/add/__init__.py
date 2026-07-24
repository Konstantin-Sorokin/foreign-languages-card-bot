from aiogram import Router

from bot.handlers.add.card import router as card_router
from bot.handlers.add.menu import router as menu_router
from bot.handlers.add.pack import router as pack_router

router = Router()

router.include_router(menu_router)
router.include_router(card_router)
router.include_router(pack_router)

__all__ = [
    "router",
]
