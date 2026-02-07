from __future__ import annotations

from datetime import datetime, timezone
from sqlmodel import Session, select

from app.db.models import Order
from app.services.banxa_client import BanxaClient


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def create_onramp_order(
    *,
    db: Session,
    banxa: BanxaClient,
    fiat_amount: float,
    fiat_currency: str,
    crypto_currency: str,
    wallet_address: str,
    blockchain: str,
    user_email: str,
) -> Order:
    result = banxa.create_onramp_order(
        fiat_amount=fiat_amount,
        fiat_currency=fiat_currency,
        crypto_currency=crypto_currency,
        wallet_address=wallet_address,
        blockchain=blockchain,
        user_email=user_email,
    )

    order = Order(
        provider="banxa",
        direction="onramp",
        order_id=result.order_id,
        order_status=result.status,
        user_email=user_email,
        fiat_amount=fiat_amount,
        fiat_currency=fiat_currency,
        crypto_currency=crypto_currency,
        wallet_address=wallet_address,
        blockchain=blockchain,
        checkout_url=result.checkout_url,
        created_at=result.created_at,
        updated_at=utcnow(),
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_onramp_order_by_order_id(db: Session, order_id: str) -> Order | None:
    stmt = select(Order).where(Order.direction == "onramp", Order.order_id == order_id)
    return db.exec(stmt).first()
