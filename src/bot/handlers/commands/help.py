from aiogram import Router, types
from aiogram.filters import Command

from bot.texts.messages import HELP_MESSAGE
from bot.utils.constants import HELP_COMMAND

router = Router(name=__name__)


@router.message(Command(HELP_COMMAND))
async def cmd_help(
    message: types.Message,
) -> None:
    """Show help information about the bot."""

    await message.answer(HELP_MESSAGE)
