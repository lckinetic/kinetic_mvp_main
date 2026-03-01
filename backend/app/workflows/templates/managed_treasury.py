from __future__ import annotations

from typing import Any, Dict
from sqlmodel import Session

from app.core.config import Settings
from app.workflows.registry import register
from app.services.workflow_steps import step_start, step_complete, step_fail


def _maybe_fail(input: Dict[str, Any], step_name: str) -> str | None:
    """
    Demo helper: if user sets simulate_failure_step == current step_name,
    we mark the step failed and raise an error to stop the workflow.
    """
    target = str(input.get("simulate_failure_step", "")).strip()
    if target and target == step_name:
        msg = str(input.get("simulate_failure_message", "Simulated failure")).strip()
        return msg or "Simulated failure"
    return None


@register(
    name="managed_treasury",
    version="1.0",
    display_name="Managed Crypto Treasury",
    description="Transfer assets to exchange, execute trade, withdraw back (demo).",
    category="treasury",
    input_schema=[
        {
            "name": "user_email",
            "label": "User email",
            "type": "email",
            "required": True,
            "example": "demo@example.com",
            "placeholder": "name@company.com",
        },
        {
            "name": "trade_symbol",
            "label": "Trading pair",
            "type": "string",
            "required": True,
            "default": "BTC-USD",
            "example": "BTC-USD",
            "help_text": "Symbol used for the demo trade.",
        },
        {
            "name": "trade_amount",
            "label": "Trade amount",
            "type": "number",
            "required": True,
            "default": 100,
            "example": 100,
            "min": 1,
            "step": 1,
            "help_text": "Amount used for the demo trade.",
        },
        # Upgrade 2: failure simulation controls
        {
            "name": "simulate_failure_step",
            "label": "Simulate failure at step (optional)",
            "type": "select",
            "required": False,
            "default": "",
            "options": [
                "",
                "wallet.create",
                "transfer.to_exchange",
                "trade.execute",
                "balance.check",
                "withdraw.to_wallet",
            ],
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
    business_summary="Invest treasury assets by transferring to an exchange, executing a trade, and returning funds to self-custody (demo).",
    business_steps=[
        "Create or access self-custodial wallet",
        "Transfer assets to exchange",
        "Execute simple trade",
        "Track updated balance",
        "Withdraw assets back to wallet",
    ],
    step_outline=[
        "wallet.create",
        "transfer.to_exchange",
        "trade.execute",
        "balance.check",
        "withdraw.to_wallet",
    ],
    step_labels={
        "wallet.create": "Create Wallet",
        "transfer.to_exchange": "Transfer to Exchange",
        "trade.execute": "Execute Trade",
        "balance.check": "Check Balance",
        "withdraw.to_wallet": "Withdraw to Wallet",
    },
)
def managed_treasury(
    *,
    db: Session,
    settings: Settings,
    adapters: Dict[str, Any],
    input: Dict[str, Any],
) -> Dict[str, Any]:
    run_id = int(input.get("run_id", 0))
    seq = 1
    steps_out = []

    user_email = input["user_email"]
    symbol = input.get("trade_symbol", "BTC-USD")
    amount = float(input.get("trade_amount", 100))

    privy = adapters["privy"]
    coinbase = adapters["coinbase"]

    # 1) wallet.create
    s = step_start(db=db, run_id=run_id, seq=seq, step_name="wallet.create")
    try:
        msg = _maybe_fail(input, "wallet.create")
        if msg:
            step_fail(db=db, step_id=s.id, error=msg)
            raise RuntimeError(msg)

        wallet = privy.create_wallet(user_email=user_email)
        step_complete(db=db, step_id=s.id, data={"wallet_id": wallet.wallet_id})
        steps_out.append({"step": "wallet.create", "wallet_id": wallet.wallet_id})
    except Exception as e:
        step_fail(db=db, step_id=s.id, error=str(e))
        raise
    seq += 1

    # 2) transfer.to_exchange (mock)
    s = step_start(db=db, run_id=run_id, seq=seq, step_name="transfer.to_exchange")
    try:
        msg = _maybe_fail(input, "transfer.to_exchange")
        if msg:
            step_fail(db=db, step_id=s.id, error=msg)
            raise RuntimeError(msg)

        # mock transfer result (feel free to replace with real adapter call later)
        transfer_id = f"mock_transfer_{run_id}"
        step_complete(db=db, step_id=s.id, data={"status": "transferred", "transfer_id": transfer_id})
        steps_out.append({"step": "transfer.to_exchange", "status": "completed", "transfer_id": transfer_id})
    except Exception as e:
        step_fail(db=db, step_id=s.id, error=str(e))
        raise
    seq += 1

    # 3) trade.execute
    s = step_start(db=db, run_id=run_id, seq=seq, step_name="trade.execute")
    try:
        msg = _maybe_fail(input, "trade.execute")
        if msg:
            step_fail(db=db, step_id=s.id, error=msg)
            raise RuntimeError(msg)

        trade = coinbase.place_trade(symbol=symbol, side="buy", amount=amount)
        step_complete(db=db, step_id=s.id, data={"trade_id": trade.trade_id, "symbol": symbol, "side": "buy", "amount": amount})
        steps_out.append({"step": "trade.execute", "trade_id": trade.trade_id})
    except Exception as e:
        step_fail(db=db, step_id=s.id, error=str(e))
        raise
    seq += 1

    # 4) balance.check (mock)
    s = step_start(db=db, run_id=run_id, seq=seq, step_name="balance.check")
    try:
        msg = _maybe_fail(input, "balance.check")
        if msg:
            step_fail(db=db, step_id=s.id, error=msg)
            raise RuntimeError(msg)

        # mock balance (replace with coinbase.get_balance() later)
        balance = 1000
        step_complete(db=db, step_id=s.id, data={"balance": balance})
        steps_out.append({"step": "balance.check", "balance": balance})
    except Exception as e:
        step_fail(db=db, step_id=s.id, error=str(e))
        raise
    seq += 1

    # 5) withdraw.to_wallet (mock)
    s = step_start(db=db, run_id=run_id, seq=seq, step_name="withdraw.to_wallet")
    try:
        msg = _maybe_fail(input, "withdraw.to_wallet")
        if msg:
            step_fail(db=db, step_id=s.id, error=msg)
            raise RuntimeError(msg)

        withdraw_id = f"mock_withdraw_{run_id}"
        step_complete(db=db, step_id=s.id, data={"status": "withdrawn", "withdraw_id": withdraw_id})
        steps_out.append({"step": "withdraw.to_wallet", "status": "completed", "withdraw_id": withdraw_id})
    except Exception as e:
        step_fail(db=db, step_id=s.id, error=str(e))
        raise

    return {
        "template": "managed_treasury",
        "steps": steps_out,
        "result": {
            "run_id": run_id,
            "wallet_id": wallet.wallet_id,
            "trade_id": trade.trade_id,
            "symbol": symbol,
            "amount": amount,
        },
    }