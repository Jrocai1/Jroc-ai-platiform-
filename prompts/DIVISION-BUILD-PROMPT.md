# Reusable J-ROC AI Division Build Prompt

**Division:** [ENTER DIVISION]  
**Repository:** [OWNER/REPOSITORY]  
**Architecture:** `docs/JROC-AI-MASTER-BLUEPRINT.md`

Inspect the repository before editing. Identify the existing stack, current functionality, schema/migrations, tests, and blockers. Preserve working code and user data.

Implement a complete vertical workflow for this division:
- UI connected to real backend APIs.
- Persistent records and migrations.
- Server-side authentication and authorization.
- Input validation and useful loading, empty, success, and failure states.
- Audit events for important operations.
- Idempotent external actions and safe retry behavior.
- Automated tests for the critical workflow, permissions, persistence, and failures.
- Build/CI integration and setup/troubleshooting documentation.

Reuse shared identity/RBAC, LLM Gateway, worker engine, project state, secret references, integration hub, policy/approval engine, audit, and observability. Do not build a disconnected dashboard or hard-code live metrics.

Use only explicitly approved LLM providers/models. In free-only mode, fail closed if cost is unknown; never silently use paid models. Require explicit approval for live spend, campaign activation, bulk outbound messages, production deployments, real payments/refunds, and destructive actions.

Run tests/build and report exact evidence. Use statuses: NOT STARTED, IN PROGRESS, BLOCKED, IMPLEMENTED — NOT VERIFIED, VERIFIED IN TEST, DEPLOYED — VERIFIED. Continue implementation as far as access permits; document precise blockers instead of faking connectivity.
