from __future__ import annotations

from dataclasses import dataclass
import uuid


@dataclass
class PrivyWallet:
    wallet_id: str
    address: str


class PrivyClient:
    """
    Mock Privy adapter (MVP version).
    Later this will wrap real Privy API calls.
    """

    def __init__(self, *, mock_mode: bool = True):
        self.mock_mode = mock_mode

    def create_wallet(self, *, user_email: str) -> PrivyWallet:
        """
        Create a mock self-custodial wallet for a user.
        In real implementation this would call Privy API.
        """
        wallet_id = f"privy_wallet_{uuid.uuid4().hex[:12]}"
        address = f"0x{uuid.uuid4().hex[:40]}"

        return PrivyWallet(
            wallet_id=wallet_id,
            address=address,
        )