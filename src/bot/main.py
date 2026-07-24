import asyncio

from bot.core.logging import configure_logging
from bot.creator import (
    create_dispatcher,
    create_resources,
    setup_bot,
    shutdown_resources,
)


async def main():
    """Application entry point."""
    configure_logging()

    resources = await create_resources()

    await setup_bot(resources)

    dp = create_dispatcher(resources)
    asyncio.create_task(resources.notification_consumer.start())

    try:
        await dp.start_polling(resources.bot)
    finally:
        await shutdown_resources(resources)


if __name__ == "__main__":
    asyncio.run(main())
