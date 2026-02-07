import logging

SENSITIVE_KEYS = {"BANXA_API_KEY", "BANXA_API_SECRET", "BANXA_WEBHOOK_SECRET"}


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def safe_settings_log(data: dict) -> dict:
    masked = {}
    for k, v in data.items():
        if k in SENSITIVE_KEYS and v:
            masked[k] = "***"
        else:
            masked[k] = v
    return masked
