# Architecture Principles (Kinetic MVP)

These are guardrails to keep the MVP clean while moving fast (especially without a full-time CTO).

## 1) Keep layers clean
- API layer (`backend/app/api`): request/response, validation, dependency injection
- Service layer (`backend/app/services`): business logic, orchestration
- Provider clients (`backend/app/services/*client.py`): integration details only
- DB layer (`backend/app/db`): models, engine, session

Rule: API routes should not contain provider logic or raw SQL beyond simple queries.

## 2) Internal canonical statuses
We store internal status values only:
- pending | processing | completed | failed | cancelled

Provider-specific statuses must be normalised in one place.
Never persist unknown provider status strings into the Order table.

## 3) Idempotency is enforced at DB level
- Webhooks: unique idempotency_key in WebhookEvent
- Order creation: unique (provider, direction, client_reference) when client_reference is present

Rule: idempotency must survive restarts.

## 4) Audit trail first
- Store raw webhook payloads as received
- Mark processed state
- Do not delete events in MVP

Rule: prefer "store then process" over "process only".

## 5) MOCK_MODE is a first-class runtime mode
- MOCK_MODE=true: deterministic, demo-safe behaviour, no external dependencies
- MOCK_MODE=false: real integration paths (incrementally implemented)

Rule: MVP must be demoable without external providers.

## 6) Minimal UI: Postman is the UI
Until UI work begins, Postman collection is part of the product.
It must be version-controlled under `/postman`.

## 7) Documentation lives with code
- docs/ is the source of truth
- Each new endpoint must update:
  - docs/api/*
  - postman/*
  - relevant README notes

## 8) Prefer small, reversible changes
- Avoid big refactors during MVP unless blocking
- Add guardrails (allowed status set, terminal protection) early
- Reset local DB is acceptable during MVP; migrations later

