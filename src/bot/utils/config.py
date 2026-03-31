from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            PROJECT_ROOT / ".env.template",
            PROJECT_ROOT / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )
    token: str
    proxy_url: str


settings = Settings()
