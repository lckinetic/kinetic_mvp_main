from __future__ import annotations

from typing import Any, Dict
from sqlmodel import Session

from app.core.config import Settings
from app.services.banxa_client import BanxaClient
from app.workflows.registry import register

from app.services.onramp_service import create_onramp_order
from app.services.offramp_service import create_offramp_order
from app.services.order_lifecycle import apply_order_status_update
from app.services.workflow_steps import step_start, step_complete, step_fail
from app.domain.catalog import (
    SUPPORTED_FIAT_CURRENCIES,
    SUPPORTED_CRYPTO_CURRENCIES,
    SUPPORTED_BLOCKCHAINS,
)


def _maybe_fail(input_data: Dict[str, Any], step_name: str) -> str | None:
    """
    Demo helper: if simulate_failure_step == step_name, return the message to fail with.
    """
    target = str(input_data.get("simulate_failure_step", "")).strip()
    if target and target == step_name:
        msg = str(input_data.get("simulate_failure_message", "Simulated failure")).strip()
        return msg or "Simulated failure"
    return None


@register(
    name="treasury_demo",
    version="1.0",
    display_name="Treasury Rebalance (Demo)",
    description="Mock flow: Onramp → Complete → Offramp → Complete",
    category="treasury",
    business_summary="Convert fiat to stablecoins and back again using a pre-defined treasury workflow (demo).",
    business_steps=[
        "Buy stablecoins using a fiat onramp",
        "Confirm completion (provider status update)",
        "Sell stablecoins back to fiat (offramp)",
        "Confirm payout completion",
    ],
    step_outline=["onramp.create", "onramp.complete", "offramp.create", "offramp.complete"],
    step_labels={
        "onramp.create": "Buy stablecoins (create onramp order)",
        "onramp.complete": "Confirm purchase completed",
        "offramp.create": "Sell stablecoins (create offramp order)",
        "offramp.complete": "Confirm payout completed",
    },
    input_schema=[
        {
            "name": "fiat_amount",
            "label": "Fiat amount",
            "type": "number",
            "required": True,
            "default": 1000,
            "example": 1000,
            "min": 10,
            "step": 1,
            "help_text": "How much fiat to onramp (demo value).",
        },
        {
            "name": "fiat_currency",
            "label": "Fiat currency",
            "type": "select",
            "required": True,
            "default": "GBP",
            "options": SUPPORTED_FIAT_CURRENCIES,
            "help_text": "Fiat currency used for both onramp and offramp.",
        },
        {
            "name": "crypto_currency",
            "label": "Crypto currency",
            "type": "select",
            "required": True,
            "default": "USDC",
            "options": SUPPORTED_CRYPTO_CURRENCIES,
            "help_text": "Asset to buy onramp / sell offramp.",
        },
        {
            "name": "wallet_address",
            "label": "Destination wallet (onramp)",
            "type": "string",
            "required": True,
            "example": "0xDEMO",
            "placeholder": "0x…",
            "help_text": "Where purchased crypto is delivered (demo).",
        },
        {
            "name": "blockchain",
            "label": "Blockchain",
            "type": "select",
            "required": True,
            "default": "ethereum",
            "options": SUPPORTED_BLOCKCHAINS,
            "help_text": "Network used for the onramp transfer.",
        },
        {
            "name": "user_email",
            "label": "User email",
            "type": "email",
            "required": True,
            "example": "demo@example.com",
            "placeholder": "name@company.com",
            "help_text": "Used for provider checkout / KYC (demo).",
        },
        {
            "name": "crypto_amount",
            "label": "Crypto amount (offramp)",
            "type": "number",
            "required": True,
            "default": 100,
            "example": 100,
            "min": 1,
            "step": 0.01,
            "help_text": "Amount of crypto to sell for fiat (demo).",
        },
        {
            "name": "destination_reference",
            "label": "Offramp destination reference",
            "type": "string",
            "required": True,
            "example": "demo-bank-001",
            "placeholder": "e.g. bank account / payout ref",
            "help_text": "Identifier for payout destination (demo).",
        },
        {
            "name": "onramp_client_reference",
            "label": "Onramp client reference",
            "type": "string",
            "required": False,
            "example": "treasury-demo-on-001",
            "help_text": "Optional idempotency key for onramp create.",
        },
        {
            "name": "offramp_client_reference",
            "label": "Offramp client reference",
            "type": "string",
            "required": False,
            "example": "treasury-demo-off-001",
            "help_text": "Optional idempotency key for offramp create.",
        },

        # ✅ Upgrade 2: simulate failures (optional)
        {
            "name": "simulate_failure_step",
            "label": "Simulate failure at step (optional)",
            "type": "select",
            "required": False,
            "default": "",
            "options": ["", "onramp.create", "onramp.complete", "offramp.create", "offramp.complete"],
            "help_text": "For demo purposes: forces the workflow to fail at the selected step.",
        },
        {
            "name": "simulate_failure_message",
            "label": "Failure message (optional)",
            "type": "string",
            "required": False,
            "default": "Simulated failure",
            "help_text": "Custom message used when simulation is triggered.",
        },
    ],
)
def treasury_demo(
    *,
    db: Session,
    settings: Settings,
    banxa: BanxaClient,
    input: Dict[str, Any],
) -> Dict[str, Any]:
    run_id = int(input["run_id"])
    seq = 1
    steps_out = []

    # Inputs (safe defaults for demos)
    fiat_amount = float(input.get("fiat_amount", 1000))
    fiat_currency = str(input["fiat_currency"])
    crypto_currency = str(input["crypto_currency"])
    wallet_address = str(input.get("wallet_address", "0xDEMO_WALLET_ADDRESS"))
    blockchain = str(input["blockchain"])
    user_email = str(input.get("user_email", "demo@example.com"))

    destination_reference = str(input.get("destination_reference", "demo-bank-ref-001"))
    crypto_amount = float(input.get("crypto_amount", 100))

    run_id_str = str(input.get("run_id", "")).strip()
    onramp_ref = input.get("onramp_client_reference") or (f"treasury_demo_on_{run_id_str}" if run_id_str else None)
    offramp_ref = input.get("offramp_client_reference") or (f"treasury_demo_off_{run_id_str}" if run_id_str else None)

    # 1) onramp.create
    s = step_start(db=db, run_id=run_id, seq=seq, step_name="onramp.create", data={"client_reference": onramp_ref})
    try:
        msg = _maybe_fail(input, "onramp.create")
        if msg:
            step_fail(db=db, step_id=s.id, error=msg)
            raise RuntimeError(msg)

        onramp_order = create_onramp_order(
            db=db,
            banxa=banxa,
            fiat_amount=fiat_amount,
            fiat_currency=fiat_currency,
            crypto_currency=crypto_currency,
            wallet_address=wallet_address,
            blockchain=blockchain,
            user_email=user_email,
            client_reference=onramp_ref,
        )
        step_complete(db=db, step_id=s.id, data={"order_id": onramp_order.order_id})
        steps_out.append({"step": "onramp.create", "order_id": onramp_order.order_id})
    except Exception as e:
        step_fail(db=db, step_id=s.id, error=f"{type(e).__name__}: {e}")
        raise
    seq += 1

    # 2) onramp.complete (simulate)
    s = step_start(db=db, run_id=run_id, seq=seq, step_name="onramp.complete", data={"order_id": onramp_order.order_id})
    try:
        msg = _maybe_fail(input, "onramp.complete")
        if msg:
            step_fail(db=db, step_id=s.id, error=msg)
            raise RuntimeError(msg)

        updated = apply_order_status_update(
            db=db,
            provider="banxa",
            direction="onramp",
            order_id=onramp_order.order_id,
            raw_status="success",
        )
        step_complete(db=db, step_id=s.id, data={"status": updated.order_status if updated else None})
        steps_out.append({"step": "onramp.complete", "status": "completed"})
    except Exception as e:
        step_fail(db=db, step_id=s.id, error=f"{type(e).__name__}: {e}")
        raise
    seq += 1

    # 3) offramp.create
    s = step_start(db=db, run_id=run_id, seq=seq, step_name="offramp.create", data={"client_reference": offramp_ref})
    try:
        msg = _maybe_fail(input, "offramp.create")
        if msg:
            step_fail(db=db, step_id=s.id, error=msg)
            raise RuntimeError(msg)

        offramp_order = create_offramp_order(
            db=db,
            banxa=banxa,
            crypto_amount=crypto_amount,
            crypto_currency=crypto_currency,
            fiat_currency=fiat_currency,
            destination_reference=destination_reference,
            user_email=user_email,
            client_reference=offramp_ref,
        )
        step_complete(db=db, step_id=s.id, data={"order_id": offramp_order.order_id})
        steps_out.append({"step": "offramp.create", "order_id": offramp_order.order_id})
    except Exception as e:
        step_fail(db=db, step_id=s.id, error=f"{type(e).__name__}: {e}")
        raise
    seq += 1

    # 4) offramp.complete (simulate)
    s = step_start(db=db, run_id=run_id, seq=seq, step_name="offramp.complete", data={"order_id": offramp_order.order_id})
    try:
        msg = _maybe_fail(input, "offramp.complete")
        if msg:
            step_fail(db=db, step_id=s.id, error=msg)
            raise RuntimeError(msg)

        updated = apply_order_status_update(
            db=db,
            provider="banxa",
            direction="offramp",
            order_id=offramp_order.order_id,
            raw_status="success",
        )
        step_complete(db=db, step_id=s.id, data={"status": updated.order_status if updated else None})
        steps_out.append({"step": "offramp.complete", "status": "completed"})
    except Exception as e:
        step_fail(db=db, step_id=s.id, error=f"{type(e).__name__}: {e}")
        raise

    return {
        "template": "treasury_demo",
        "steps": steps_out,
        "result": {
            "run_id": run_id,
            "onramp_order_id": onramp_order.order_id,
            "offramp_order_id": offramp_order.order_id,
            "fiat_currency": fiat_currency,
            "crypto_currency": crypto_currency,
        },
    }