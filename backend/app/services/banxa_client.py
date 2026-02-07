from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import uuid


@dataclass(frozen=True)
class BanxaCreateOrderResult:
    order_id: str
    checkout_url: str
    status: str
    created_at: datetime


class BanxaClient:
    """
    MVP client. In MOCK_MODE it returns fake order IDs and a sandbox-like checkout URL.
    Later we swap the NotImplementedError for real Banxa API calls.
    """
    def __init__(self, mock_mode: bool):
        self.mock_mode = mock_mode

    def create_onramp_order(
        self,
        *,
        fiat_amount: float,
        fiat_currency: str,
        crypto_currency: str,
        wallet_address: str,
        blockchain: str,
        user_email: str,
    ) -> BanxaCreateOrderResult:
        if self.mock_mode:
            oid = f"banxa_mock_{uuid.uuid4().hex[:12]}"
            url = f"https://checkout.sandbox.banxa.com/?order_id={oid}"
            return BanxaCreateOrderResult(
                order_id=oid,
                checkout_url=url,
                status="pending",
                created_at=datetime.now(timezone.utc),
            )

        raise NotImplementedError("Real Banxa calls not implemented yet. Set MOCK_MODE=true.")
