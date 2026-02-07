# Kinetic MVP – Development & Agent Operating Guide

## 1. Purpose of This Repository

This repository contains the **local-first MVP implementation of Kinetic**.

The goal of this MVP is to:
- Demonstrate a **working end-to-end crypto flow**:
  - Fiat on-ramp → wallet → off-ramp
- Validate third-party integrations (starting with Banxa)
- Support demos for partners and investors
- Be built **without a full-time CTO**, using AI agents + light external dev help

This is **not** the final platform architecture.  
This is a **fast, reliable, demoable MVP**.

---

## 2. Core MVP Principles (Non-Negotiable)

1. **Local-first development**
   - No AWS hosting yet
   - Everything runs locally via Docker + FastAPI

2. **Deterministic runtime**
   - No LLMs or AI agents in production request handling
   - Runtime logic must be predictable and testable

3. **AI agents are the dev team, not the runtime**
   - Agents help write code, tests, tickets, reviews
   - Agents do *not* make runtime decisions

4. **Single backend service**
   - One FastAPI app
   - One Postgres database
   - No microservices, no queues, no platform engine (yet)

5. **Mock-first integrations**
   - `MOCK_MODE=true` enables simulated Banxa / wallet flows
   - Same code paths for mock and real APIs

---

## 3. MVP Scope (What We Are Building)

### In Scope (MVP)
- Banxa fiat on-ramp (sandbox first)
- Banxa fiat off-ramp
- Basic wallet abstraction (Privy or stub initially)
- Order lifecycle tracking
- Webhook handling with idempotency
- Minimal UI or API-only demo

### Out of Scope (MVP)
- Visual workflow builder
- Multi-provider routing
- Dynamic module registry
- Runtime AI orchestration
- DeFi strategies or complex treasury logic
- Production-grade IAM or compliance tooling

---

## 4. High-Level Architecture (MVP)

Client (UI / CLI / Postman)
        |
        v
FastAPI Endpoints
        |
        v
Service Layer (pure Python)
        |
        v
Integration Clients (Banxa / Wallet)
        |
        v
Mock APIs OR Real APIs

---

## 5. Repository Structure

```
kinetic-mvp/
├─ backend/
│  ├─ app/
│  │  ├─ api/
│  │  ├─ core/
│  │  ├─ db/
│  │  ├─ services/
│  │  └─ tests/
│  ├─ pyproject.toml
│  ├─ .env.example
│  └─ README.md
├─ infra/
│  └─ docker-compose.yml
└─ README.md
```

---

## 6. Database Strategy

- ORM: **SQLModel**
- Migrations: **None for MVP**
- Tables created on startup via `SQLModel.metadata.create_all(engine)`

---

## 7. AI Agent Team (Internal Dev Team)

Agents act as **build-time helpers**, not runtime logic.

Roles:
- Orchestrator
- Tech Lead (CTO replacement)
- Repo Lead Dev
- Pair Programmer
- QA / Test Engineer
- AppSec-lite

---

## 8. Definition of Done

- Working code
- Local run instructions
- Tests or test steps
- One happy-path example
- No unnecessary abstractions

---

## 9. How to Run Locally

```bash
docker compose -f infra/docker-compose.yml up -d
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```
test from another terminal
curl http://localhost:8000/health

---

## 10. Guiding Philosophy

> Proof beats elegance.  
> Working beats perfect.  
> Deterministic beats clever.


## activate environment
source .venv/bin/activate

# start postgresql
brew services start postgresql@15
brew services restart postgresql@15
psql -h 127.0.0.1 -p 5432 -U kinetic -d kinetic

\dt
\q

# validating the full startup chain
env → config → FastAPI → DB engine → tables → API endpoint

# Swagger UI
http://127.0.0.1:8000/docs

# Health check
http://127.0.0.1:8000/health

# Onramp
http://127.0.0.1:8000/onramp/create

# Onramp
http://127.0.0.1:8000/onramp/create