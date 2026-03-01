from __future__ import annotations

from typing import Any, Dict, Optional
import inspect

from fastapi import HTTPException
from sqlmodel import Session

from app.core.config import Settings, get_settings
from app.db.models import WorkflowRun, utcnow

from app.workflows.registry import get_template
from app.workflows.validation import validate_template_input

# Adapters
from app.services.banxa_client import BanxaClient
from app.adapters.privy.client import PrivyClient
from app.adapters.coinbase.client import CoinbaseClient


def _build_adapters(settings: Settings) -> Dict[str, Any]:
    """
    Central place to construct all adapter clients.
    For MVP these are mock-only; later you can wire real creds from settings.
    """
    return {
        "banxa": BanxaClient(mock_mode=settings.mock_mode),
        "privy": PrivyClient(mock_mode=settings.mock_mode),
        "coinbase": CoinbaseClient(mock_mode=settings.mock_mode),
    }


def _call_template_function(
    fn,
    *,
    db: Session,
    settings: Settings,
    input_data: Dict[str, Any],
):
    """
    Call a template function safely, supporting both:
      - legacy: fn(db=..., settings=..., banxa=..., input=...)
      - new:    fn(db=..., settings=..., adapters={...}, input=...)
    """
    adapters = _build_adapters(settings)

    sig = inspect.signature(fn)
    kwargs: Dict[str, Any] = {
        "db": db,
        "settings": settings,
        "input": input_data,
    }

    # legacy support
    if "banxa" in sig.parameters:
        kwargs["banxa"] = adapters["banxa"]

    # new support
    if "adapters" in sig.parameters:
        kwargs["adapters"] = adapters

    return fn(**kwargs)


def run_template(
    *,
    db: Session,
    template_name: str,
    input_data: Dict[str, Any],
    settings: Optional[Settings] = None,
) -> WorkflowRun:
    try:
        t = get_template(template_name)
    except KeyError:
        raise HTTPException(status_code=404, detail="Template not found")

    settings = settings or get_settings()

    run = WorkflowRun(
        template_name=template_name,
        status="running",
        input=input_data or {},
        output={},
        updated_at=utcnow(),
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    run_input = dict(run.input or {})
    run_input["run_id"] = run.id
    run.input = run_input
    db.add(run)
    db.commit()
    db.refresh(run)

    try:
        schema = t.get("input_schema", [])
        validated_input = validate_template_input(run_input, schema)
        validated_input["run_id"] = run.id

        fn = t["function"]
        output = _call_template_function(
            fn,
            db=db,
            settings=settings,
            input_data=validated_input,
        )

        run.status = "completed"
        run.output = output or {}
        run.updated_at = utcnow()

    except HTTPException as e:
        run.status = "failed"
        run.error = str(e.detail)
        run.updated_at = utcnow()
        db.add(run)
        db.commit()
        db.refresh(run)
        raise

    except Exception as e:
        run.status = "failed"
        run.error = f"{type(e).__name__}: {e}"
        run.updated_at = utcnow()

    db.add(run)
    db.commit()
    db.refresh(run)
    return run