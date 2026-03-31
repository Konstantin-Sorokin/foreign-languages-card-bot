import asyncio
import logging

from bot.creator import create_bot, create_dispatcher
from bot.utils import COMMANDS


async def main():
    logging.basicConfig(level=logging.INFO)

    dp = create_dispatcher()
    bot = create_bot()
    await bot.set_my_commands(COMMANDS)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
