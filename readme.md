---

## 6. Database Strategy

- ORM: **SQLModel**
- Migrations: **None for MVP**
  - Tables are created on startup using:
    ```python
    SQLModel.metadata.create_all(engine)
    ```
- One `orders` table for both on-ramp and off-ramp (simpler MVP)
- One `webhook_events` table for idempotency and audit

---

## 7. AI Agent Team (Internal Dev Team)

AI agents are treated as **specialised team roles**.

They generate:
- code
- tickets
- tests
- reviews
- checklists

They do **not** run in production.

---

### 7.1 Orchestrator Agent

**Responsibility**
- Coordinate all other agents
- Merge outputs into a single “Execution Pack”

**Typical Output**
- Decisions required
- Sprint tickets
- File changes
- Test plan
- Risks

---

### 7.2 Tech Lead Agent (CTO Replacement)

**Responsibility**
- Simplify architecture
- Enforce MVP scope
- Prevent overengineering

**Rules**
- One FastAPI service only
- No AWS services
- Prefer clarity over flexibility

---

### 7.3 Repo Lead Dev Agent

**Responsibility**
- Own repo structure and conventions
- Review AI-generated code for consistency
- Block architectural drift

**Rules**
- Everything must run locally
- Clear run instructions required

---

### 7.4 Pair Programmer Agent

**Responsibility**
- Take a single ticket → produce working code

**Required Output**
- Files to create/edit
- Code snippets
- Commands to run
- Tests
- One curl/Postman example

---

### 7.5 QA / Test Engineer Agent

**Responsibility**
- Protect demo stability
- Catch edge cases early

**Focus Areas**
- Webhook idempotency
- Order state transitions
- Replay handling
- Regression smoke tests

---

### 7.6 AppSec-Lite Agent

**Responsibility**
- MVP-level security hygiene

**Focus Areas**
- `.env` secrets handling
- No secrets in logs
- Webhook signature verification
- Basic input validation

---

## 8. Definition of Done (For Any Ticket)

A ticket is **not done** unless it includes:

- ✅ Working code
- ✅ Local run instructions
- ✅ Tests or test steps
- ✅ One happy-path example (curl/Postman)
- ✅ No new unnecessary abstractions

---

## 9. Development Workflow

1. PM / Orchestrator defines ticket
2. Tech Lead confirms scope
3. Pair Programmer writes code
4. Repo Lead Dev reviews structure
5. QA Agent validates behaviour
6. You merge and move on

---

## 10. How to Run Locally (MVP)

```bash
docker compose -f infra/docker-compose.yml up -d
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000


### Smoke check

curl http://localhost:8000/health