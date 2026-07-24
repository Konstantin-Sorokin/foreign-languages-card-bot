from aiogram import Router

from bot.handlers.learning.irregular_verb import router as irregular_verb_router
from bot.handlers.learning.menu import router as menu_router
from bot.handlers.learning.translation_card import router as translation_card_router

router = Router()

router.include_router(menu_router)
router.include_router(irregular_verb_router)
router.include_router(translation_card_router)

__all__ = [
    "router",
]
