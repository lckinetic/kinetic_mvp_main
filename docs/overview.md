# Kinetic MVP – Overview

## Goal
Build a working MVP that demonstrates:
- On/off-ramp flows (Banxa), starting with on-ramp
- A minimal backend that persists order state
- Mock mode for safe demos and fast iteration

## What’s in scope (MVP)
- FastAPI backend
- Postgres persistence (Docker)
- API endpoints for:
  - Health check
  - Onramp order creation + retrieval
  - Webhook ingestion (next)

## What’s explicitly out of scope (for MVP)
- Production-grade auth / RBAC
- Full UI polish (Postman is primary UI)
- Full provider coverage / edge-case completeness
