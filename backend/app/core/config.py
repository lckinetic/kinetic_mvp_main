from __future__ import annotations
from dataclasses import dataclass
import os
from dotenv import load_dotenv


def _bool(v: str | None, default: bool = False) -> bool:
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    database_url: str
    mock_mode: bool

    banxa_api_key: str
    banxa_api_secret: str
    banxa_env: str
    banxa_webhook_secret: str

    log_level: str


def get_settings() -> Settings:
    # Loads backend/.env when you run from backend/
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required (see backend/.env.example).")

    return Settings(
        database_url=database_url,
        mock_mode=_bool(os.getenv("MOCK_MODE"), default=True),

        banxa_api_key=os.getenv("BANXA_API_KEY", ""),
        banxa_api_secret=os.getenv("BANXA_API_SECRET", ""),
        banxa_env=os.getenv("BANXA_ENV", "sandbox"),
        banxa_webhook_secret=os.getenv("BANXA_WEBHOOK_SECRET", ""),

        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )