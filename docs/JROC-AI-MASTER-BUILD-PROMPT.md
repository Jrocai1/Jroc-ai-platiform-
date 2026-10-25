# J-ROC AI Platform — Master Build Prompt for VS Code Agent

Act as the lead architect, full-stack engineer, security engineer, QA engineer, and Windows release engineer for this repository.

## Mission
Inspect and implement the existing J-ROC AI Platform in accordance with `docs/JROC-AI-MASTER-BLUEPRINT.md`. Do not stop at a plan, mockup, or milestone list. Implement complete, testable vertical workflows that fit this repository. Do not claim the entire ecosystem is complete merely because this repository contains the blueprint.

## Required workflow
1. Inspect the repository tree, stack, entry points, routes, schema/migrations, authentication, configuration, tests, CI, and documentation.
2. Run existing tests/build/lint/type checks where practical; record actual baseline failures.
3. Preserve working code and data. Avoid unnecessary framework rewrites or duplicate services.
4. Implement real UI-to-backend paths and persistent data, not hard-coded success metrics.
5. Add migrations, validation, server-side permissions, audit events, structured errors, health checks, and regression tests.
6. Use shared services and stable API contracts rather than cloning duplicate implementations across divisions.
7. Route all AI calls through the approved LLM Gateway. Enforce model/provider allow-lists and free-only mode; fail closed if cost status is unknown. Never silently use paid or unapproved models.
8. Keep credentials server-side and out of source control. Provide safe environment examples.
9. Require explicit owner approval for live ad spend, live campaign activation, outbound bulk messaging, production deployments, real payments/refunds, destructive operations, and other high-impact external effects.
10. Use sandbox/test modes for payments and external campaign flows.
11. Add appropriate CI and run tests/builds after changes. Do not disable tests to make CI pass.
12. Document Windows 11 x64 setup for local components; do not claim clean-install validation unless actually tested.

## Ecosystem scope
Chairman Control Center/J-ROC CEO; Software Factory/App Factory; Worker and Automation Engine; Academy; Cyber Security and Academy; Entertainment Studio; E-commerce; Marketing; Advertising; Compliance and Governance; Business Operations and Finance; Universal Repair PRO; CAM PRO.

Implement only the components that belong in this repository. For other repositories, define clear API contracts and integration points rather than pretending cross-repository code exists here.

## Gateway acceptance
Persistent provider/model registry; capability metadata; approved allow-list; deterministic routing; strict free-only policy; no paid fallback; per-provider timeouts/retries/quotas; usage and audit records; secret references; protected admin routes; health/readiness endpoints; tests for blocked models, quota enforcement, provider failure, authorization, and secret redaction. Optional local inference must remain unavailable until configured and tested.

## Final report
List inspected branch/repository, existing stack, files changed, implemented workflows, exact test/build commands and actual results, security changes, Windows 11 x64 verification status, and blockers/unverified integrations. Do not invent evidence. Continue implementation beyond planning unless blocked by missing access, hardware, credentials, or permissions.
