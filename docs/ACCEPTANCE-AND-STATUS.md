# Acceptance and Status Rules

## Status definitions
- **NOT STARTED:** no implementation evidence.
- **IN PROGRESS:** implementation underway; acceptance incomplete.
- **BLOCKED:** a named dependency, permission, credential, device, or technical issue prevents progress.
- **IMPLEMENTED — NOT VERIFIED:** code exists, required verification is incomplete.
- **VERIFIED IN TEST:** specified checks passed in a reproducible test environment.
- **DEPLOYED — VERIFIED:** deployment and post-deployment checks confirmed.

## Minimum acceptance
- UI invokes a real API/local service.
- Backend validates inputs and enforces authentication/authorization.
- Data persists and can be retrieved after restart.
- Success/failure states are truthful and visible.
- Sensitive actions generate audit records.
- Critical logic has automated tests.
- No secrets are exposed or committed.
- Configuration and recovery are documented.
- Relevant commands have actually run.

## Integration evidence
Record status (not configured/configured/connected/verified in test), test date/environment, tested capabilities, limitations, blockers, and pricing/quota source/date.

## Prohibited claims/actions
Do not call a mockup a working system; infer connectivity from a settings field; claim tests or deployment without evidence; claim services are free forever; claim compliance certification from a checklist; or execute live spend, bulk messages, real payments, or destructive actions without approval.
