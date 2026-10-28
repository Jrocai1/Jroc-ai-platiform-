# J-ROC AI Factory

J-ROC AI Factory is an authenticated Python orchestration foundation for compliant software-asset intake, approval, audit logging, and controlled mission execution.

## Included

- Authenticated WebSocket server
- Strict Pydantic request and event schemas
- Compliant asset-intake policy gate
- Human approval before deployment
- SQLite-backed append-only, hash-chained audit events
- Mission state broadcasting over WebSockets
- Sample authenticated client
- Automated intake tests

## Compliance model

Assets are accepted only when their legal basis is identified as one of the supported categories:

- J-ROC AI owned
- Expressly authorized
- Compatible open-source software
- Verified public domain

The intake gate rejects or holds assets when access-control bypass, license-enforcement removal, embedded secrets, missing attribution, missing authorization evidence, or unsupported licensing conditions are detected.

Passing an automated check does not release an asset. Accepted assets enter `PENDING_APPROVAL` and require human approval before mission deployment.

## Requirements

- Python 3.11 or later
- `websockets`
- `pydantic`

The package declares its dependencies in `pyproject.toml`.

## Installation

Create and activate a Python virtual environment, then install the package:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

On Windows PowerShell, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Configuration

Set a strong shared authentication token before starting the service. The server refuses tokens shorter than 16 characters.

Linux/macOS example:

```bash
export JROC_AUTH_TOKEN="replace-with-a-long-random-secret"
```

Windows PowerShell example:

```powershell
$env:JROC_AUTH_TOKEN = "replace-with-a-long-random-secret"
```

Optional environment variables are documented in `.env.example`:

- `JROC_HOST`
- `JROC_PORT`
- `JROC_DB`
- `JROC_AUTH_TIMEOUT_SECONDS`

## Start the server

```bash
python -m jroc_factory.server
```

The default local endpoint is `ws://127.0.0.1:8765`.

## Run the sample client

In another terminal with the same `JROC_AUTH_TOKEN` configured:

```bash
python -m jroc_factory.client
```

The sample client authenticates and submits a sample MIT-licensed asset-intake request.

## Supported WebSocket actions

- `AUTH`
- `SUBMIT_ASSET`
- `APPROVE_ASSET`
- `DEPLOY_SALVAGE_MISSION`
- `GET_STATE`

Unknown fields are rejected by the request schemas.

## Asset states

The included intake workflow uses these key states:

- `REJECTED`
- `PENDING_APPROVAL`
- `APPROVED`

Only `APPROVED` assets can be used to create a deployment mission.

## Audit ledger

The service records asset-intake decisions, approvals, and mission updates in SQLite. Audit events are chained with SHA-256 hashes so later events reference the preceding audit hash.

This provides a tamper-evident local audit structure. It should not be treated as an externally anchored or independently immutable ledger.

## Tests

Run:

```bash
pytest
```

The included tests cover:

- Compatible open-source intake
- Rejection of access-control bypass requests
- Ownership/authorization evidence requirements

## Security notes

- Keep `JROC_AUTH_TOKEN` out of source control.
- Keep `.env` files and SQLite databases out of Git.
- Use encrypted transport when exposing the WebSocket service outside a trusted local environment.
- Do not treat public availability, abandonment, bankruptcy, or product discontinuation as permission to reuse proprietary code.
- Preserve upstream copyright, license, attribution, and provenance information.
- Review licensing and authorization before integration or resale.

## Project layout

```text
jroc_factory/
  __init__.py
  audit.py
  auth.py
  client.py
  intake.py
  schemas.py
  server.py
tests/
  test_intake.py
.env.example
.gitignore
pyproject.toml
README.md
```

## J-ROC AI Factory principle

Discovery is not authorization. Intake is not approval. Approval is not ownership.

Every asset should remain traceable to its provenance, authorization basis, license obligations, review decision, and audit history.
