# Onramp API (MVP)

## Purpose
Create an on-ramp order and return a provider checkout URL. Persist the order in Postgres.

## Endpoints

### POST `/onramp/orders`
Creates a new onramp order.

**Request body**
```json
{
  "fiat_amount": 100,
  "fiat_currency": "GBP",
  "crypto_currency": "USDC",
  "wallet_address": "0xabc123",
  "blockchain": "ethereum",
  "user_email": "test@example.com"
}


**Response**
```json
{
  "order_id": "banxa_mock_....",
  "checkout_url": "https://checkout.sandbox.banxa.com/?order_id=...",
  "order_status": "pending",
  "fiat_amount": 100,
  "fiat_currency": "GBP",
  "crypto_currency": "USDC",
  "wallet_address": "0xabc123",
  "blockchain": "ethereum",
  "created_at": "2026-02-07T..."
}