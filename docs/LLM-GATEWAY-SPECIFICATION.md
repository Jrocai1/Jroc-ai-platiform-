# J-ROC AI LLM Gateway Specification

## Mission
Provide one secure backend interface for approved AI models used across J-ROC AI. A model selector alone is not a gateway.

## Requirements
- Provider adapters with normalized requests, responses, errors, capabilities, health, and usage.
- Persistent provider/model registry with enablement, explicit approval, capabilities, context limits, quota/rate metadata, pricing status, verification timestamp, and source.
- Deterministic routing constrained by explicit allow-lists.
- Strict free-only mode: reject unknown, unverified, or nonzero-cost routes unless explicitly approved by policy. No silent paid fallback.
- Server-side secret references; never expose provider credentials to the client or commit them.
- Timeouts, bounded retries, provider rate limits, quota enforcement, safe error normalization, and health/readiness.
- Usage records with timestamp, actor/division, provider/model, status, latency, usage units where available, cost status, and correlation ID.
- Protected admin operations and audit records for policy/provider/model changes.
- Optional local inference (e.g. Ollama) must show unavailable until configured and tested.
- OpenAI-compatible shapes only where supported; document modality/tool-calling limitations.

## Suggested API
- `GET /v1/models`
- `POST /v1/chat/completions`
- `POST /v1/embeddings` when supported
- `GET /health`, `GET /ready`
- Protected admin routes for providers, models, policies, usage, and audit.
Adapt to existing conventions and avoid duplicate route trees.

## Registry model
Provider: id, name, adapter type, base URL, enabled, health, secret reference, timestamps.
Model: id, provider id/model id, display name, enabled, approved, capabilities, context limit, quota/rate metadata, cost status, pricing metadata, verified timestamp/source.
Policy: allowed providers/models, free-only flag, fallback policy, per-request/daily limits, allowed divisions, enabled.
Usage: request ID, time, actor/division, provider/model, status, latency, usage units, cost status, safe error category.

Use the repository's existing database and migrations.

## Routing
1. Authenticate caller and resolve permissions.
2. Validate request and required capabilities.
3. Load applicable policy and eligible models.
4. Filter by explicit allow-list, health, quota, capability, and cost policy.
5. In free-only mode, reject models whose current cost status is not explicitly verified for the intended use.
6. Select deterministically using configured priority.
7. Apply timeout and bounded retries only for retryable failures.
8. Do not retry non-idempotent side effects without guaranteed idempotency.
9. Record safe usage/audit metadata and return normalized response or actionable error.
10. If no eligible model remains, return a clear error; do not widen the allow-list.

## Security
Admin changes require RBAC and audit logging. Validate requests, limit sizes, redact secrets, restrict access to prompts/completions, define retention, and never let model output bypass policy checks. Do not log full prompts by default when sensitive data may be present.

## Required tests
Approved-model filtering; disallowed model rejection; free-only rejection for unknown/paid cost; no paid fallback; quota enforcement; timeout/malformed response handling; secret redaction; admin authorization; usage/audit creation; local inference unavailable until configured.

## Candidate adapters
Investigate Google AI services, OpenRouter, Hugging Face inference, Groq, Cerebras, Cloudflare Workers AI, and local Ollama. This is not a claim that any provider/model is currently free or available. Verify terms, quotas, regions, and capabilities before enabling; keep unreviewed models disabled.

## Definition of done
Persistence, routing, policy enforcement, authorization, usage/audit, failure handling, and automated tests work together.
