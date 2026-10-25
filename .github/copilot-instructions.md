# J-ROC AI Platform — Coding Agent Instructions

- Read `docs/JROC-AI-MASTER-BLUEPRINT.md` before significant architecture changes.
- Inspect existing code/tests before editing; preserve working behavior and data.
- Implement real UI/backend workflows and persistent storage, not hard-coded demo metrics.
- Follow the existing stack unless a justified change is documented.
- Add migrations, validation, server-side authorization, error states, audit events, and tests.
- Keep credentials out of source, client bundles, logs, and commits.
- Route AI calls through the J-ROC AI LLM Gateway and its explicit provider/model allow-list.
- In free-only mode, reject unknown pricing/quota status; never silently use paid or unapproved models.
- Verify provider availability, capabilities, current terms, and quotas.
- Require explicit approval for live ad spend, campaign activation, bulk messaging, production deploys, real payments/refunds, and destructive actions.
- Use sandbox modes for payment and campaign testing.
- Never claim tests, integrations, devices, models, deployments, or compliance are verified without evidence.
- Run relevant lint/type-check/test/build commands and report actual results.
- Document setup and troubleshooting. State whether Windows 11 x64 behavior was actually tested.
- Distinguish implemented, tested, blocked, and unverified work.
