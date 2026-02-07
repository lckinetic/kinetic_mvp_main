from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON, Index


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    provider: str = Field(default="banxa", index=True)
    direction: str = Field(index=True)  # "onramp" | "offramp"

    order_id: str = Field(index=True)  # provider order id
    order_status: str = Field(default="pending", index=True)

    user_email: str = Field(index=True)
    fiat_amount: float
    fiat_currency: str
    crypto_currency: str

    wallet_address: str
    blockchain: str

    checkout_url: Optional[str] = None
    transaction_hash: Optional[str] = None

    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    completed_at: Optional[datetime] = None


class WebhookEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    provider: str = Field(default="banxa", index=True)
    direction: str = Field(index=True)

    event_type: str = Field(index=True)
    order_id: Optional[str] = Field(default=None, index=True)

    payload: Dict[str, Any] = Field(sa_column=Column(JSON), default_factory=dict)

    processed: bool = Field(default=False, index=True)
    received_at: datetime = Field(default_factory=utcnow)

    idempotency_key: str = Field(index=True)


Index(
    "ix_webhook_events_provider_direction_key",
    WebhookEvent.provider,
    WebhookEvent.direction,
    WebhookEvent.idempotency_key,
    unique=True,
)
