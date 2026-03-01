from __future__ import annotations

from dataclasses import dataclass
import uuid
from typing import Literal, Optional


Side = Literal["buy", "sell"]


@dataclass
class CoinbaseTrade:
    trade_id: str
    symbol: str
    side: Side
    amount: float
    status: str = "filled"
    price: Optional[float] = None


class CoinbaseClient:
    """
    Mock Coinbase adapter (MVP version).
    Later this will wrap real Coinbase Advanced Trade / Prime APIs.
    """

    def __init__(self, *, mock_mode: bool = True):
        self.mock_mode = mock_mode

    def place_trade(self, *, symbol: str, side: Side, amount: float) -> CoinbaseTrade:
        """
        Execute a mock trade.
        """
        trade_id = f"cb_trade_{uuid.uuid4().hex[:12]}"
        return CoinbaseTrade(
            trade_id=trade_id,
            symbol=symbol,
            side=side,
            amount=float(amount),
            status="filled",
            price=50000.0 if symbol.startswith("BTC") else None,  # optional demo price
        )

    def get_balance(self, *, asset: str = "USD") -> dict:
        """
        Optional helper if you later want balance.check to be real instead of hardcoded.
        """
        return {"asset": asset, "available": 1000.0}