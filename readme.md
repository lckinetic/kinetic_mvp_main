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