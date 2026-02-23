# Feature Template (MVP)

Use this template before implementing any new feature. Keep it short. Bullet points are fine.

## Feature name
- e.g. "Offramp - Create Order (mock)" / "Webhook signature validation"

## Problem / user goal
- What problem does this solve for the MVP?

## MVP impact (1–2 sentences)
- How does this strengthen the core value proposition:
  "Pre-built, configurable workflow templates for corporate crypto ops onboarding"?

## Scope (in)
- List what is included in this feature

## Scope (out)
- List what is explicitly excluded (to prevent scope creep)

## API changes
- Endpoints added/changed:
  - METHOD /path
- Request/response changes:
- Backwards compatibility concerns:

## Data model changes
- Tables/fields added/changed:
- Uniqueness / indexes:
- Migration approach:
  - MVP local: rebuild DB ok? yes/no
  - Future: migrations needed? yes/no

## Business logic changes
- Service(s) touched:
- Key logic rules (state transitions, validation:

## Idempotency & retries
- Does this feature need idempotency? yes/no
- If yes:
  - Key source (header / payload hash / client_reference)
  - Uniqueness enforced where (DB / app)

## Error handling
- Expected error cases:
- What should the API return (status codes + messages)?

## Security & secrets
- Any new env vars needed?
- Any sensitive data stored/logged?

## Tests (minimum)
- Happy path:
- Negative cases:
- Idempotency / duplicate behaviour:
- Restart persistence check:

## Docs & Postman updates
- docs file(s) to update:
- Postman request(s) to add/update:

## Done definition
- List the objective checks that prove it's done (3–8 bullets)

