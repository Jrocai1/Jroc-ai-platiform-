# J-ROC AI — Repair and Verify Prompt

Do not regenerate the project from scratch. Preserve existing features and data.

1. Inspect source, dependencies, routes, schemas/migrations, auth, configuration, tests, CI, and docs.
2. Run current checks and capture actual failures.
3. Reproduce problems and identify root causes before edits.
4. Fix broken imports/routes, schema mismatches, permission gaps, unsafe config, dead controls, persistence bugs, and UI/API mismatches.
5. Add regression tests for defects fixed.
6. Verify displayed status comes from real backend data; label unavailable providers and mock hardware clearly.
7. Verify LLM routing is allow-listed and free-only mode has no paid fallback.
8. Verify secrets remain server-side and high-impact external actions require approval.
9. Re-run checks and report exact commands/results; never invent passing tests.
10. Update docs with verified behavior and remaining blockers.

Do not delete user data or execute live spend, real payments, destructive changes, or production deployment without explicit approval. Report implemented, verified, blocked, and unverified work.
