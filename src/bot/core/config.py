import logging
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        """Convert string log level to logging module constant."""
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int = 0


class RabbitConfig(BaseModel):
    url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )
    token: str

    proxy_url: str | None = None
    api_url: str

    redis: RedisConfig
    rabbit: RabbitConfig

    logging: LoggingConfig = LoggingConfig()


settings = Settings()
