# ADR-001: Mock Mode

## Decision
Support `MOCK_MODE` as a runtime flag to switch between mocked provider behaviour and real provider calls.

## Why
- Enables fast iteration without external dependencies
- Makes demos reliable (no provider downtime)
- Reduces risk while still building real persistence and API shape

## Consequences
- Provider clients must support a mock implementation
- Real integration will be added later behind the same interface