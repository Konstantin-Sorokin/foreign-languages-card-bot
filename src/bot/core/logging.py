import logging

from bot.core.config import settings


def configure_logging() -> None:
    """Configure logging based on application settings."""
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.log_format,
    )
