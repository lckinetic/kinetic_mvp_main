# Architecture (MVP)

## High-level
- Backend: FastAPI (Python)
- DB: Postgres (Docker, local)
- ORM: SQLModel
- Config: `.env` loaded at startup

## Repo layout (key parts)
- `backend/app/main.py` – FastAPI app + startup
- `backend/app/api/` – API routes
- `backend/app/services/` – business logic + provider clients
- `backend/app/db/` – SQLModel models + engine
- `infra/docker-compose.yml` – local Postgres

## Runtime modes
- `MOCK_MODE=true`: provider calls are mocked (demo-safe)
- `MOCK_MODE=false`: real provider calls (later)

## Current endpoints
- `GET /health`
- `POST /onramp/orders` (in progress)
- `GET /onramp/orders/{order_id}` (in progress)
