from fastapi import FastAPI
import logging

from app.core.config import get_settings
from app.core.logging import configure_logging, safe_settings_log
from app.db.engine import get_engine, create_db_and_tables

# IMPORTANT: import models so SQLModel knows about tables before create_all()
from app.db import models  # noqa: F401

from app.api.health import router as health_router
from app.api.onramp import router as onramp_router

logger = logging.getLogger("kinetic")


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title="Kinetic MVP API", version="0.1.0")

    @app.on_event("startup")
    def startup():
        engine = get_engine(settings)
        create_db_and_tables(engine)
        logger.info(
            "Startup complete. %s",
            safe_settings_log(
                {
                    "MOCK_MODE": settings.mock_mode,
                    "BANXA_ENV": settings.banxa_env,
                    "DATABASE_URL": settings.database_url,
                    "BANXA_API_KEY": settings.banxa_api_key,
                    "BANXA_API_SECRET": settings.banxa_api_secret,
                    "BANXA_WEBHOOK_SECRET": settings.banxa_webhook_secret,
                }
            ),
        )

    app.include_router(health_router)
    app.include_router(onramp_router)
    return app


app = create_app()
