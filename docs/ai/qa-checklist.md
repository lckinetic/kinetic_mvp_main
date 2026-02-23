# QA Checklist (MVP)

Use this checklist before marking a feature "Done".

## API behaviour
- [ ] Endpoint appears in Swagger: /docs
- [ ] Postman request exists and passes
- [ ] Correct status codes returned for happy path
- [ ] Errors are clear and consistent (400/404/409/500 as appropriate)

## Persistence & restart safety
- [ ] Data is persisted in Postgres (not in-memory)
- [ ] Restart uvicorn and re-check critical GETs still work
- [ ] If DB schema changed, confirm local DB rebuild steps are documented

## Idempotency & duplicates
- [ ] Webhook duplicate (same idempotency key) returns duplicate_ignored (or equivalent) and does not change state
- [ ] Order creation duplicate (same client_reference) returns the existing order (same order_id)
- [ ] Terminal state protection: completed/failed/cancelled cannot be overwritten

## Lifecycle correctness
- [ ] Status updates only accept allowed statuses
- [ ] Unknown provider statuses do not corrupt internal status
- [ ] updated_at changes when status changes
- [ ] completed_at is set only for terminal transitions

## Security & secrets hygiene
- [ ] No secrets printed in logs
- [ ] .env contains required keys and is in .gitignore
- [ ] Signature validation behaviour matches MOCK_MODE expectation

## Observability / debugging
- [ ] Webhook events can be inspected (e.g. GET /webhooks/banxa/events)
- [ ] Request failures are diagnosable via logs + stored webhook payload

## Documentation
- [ ] docs/ reflects reality (API + behaviour)
- [ ] Postman collection committed under /postman
- [ ] Any new env vars documented (where + example)

