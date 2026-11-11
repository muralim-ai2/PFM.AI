# E0. Foundations and engineering platform

**Goal:** a clean repository, pipeline and conventions, so every later feature lands with tests, types and traceability.
**Depends on:** answers to the open questions in `01-scope-and-decisions.md`.
**Milestone:** M0.

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E0-01 | S0 | Repository layout | `src/pfm/{domain,services,adapters,interfaces}` with mirrored `tests/`. Import contracts fail the build when a layer rule is broken. |
| F-E0-02 | S0 | Tooling | `uv` lockfile, `ruff`, `mypy --strict`, `pre-commit` hooks. One command sets up a fresh clone. |
| F-E0-03 | S0 | CI pipeline | PR workflow runs format, lint, types, import contracts, tests, coverage gate, secret scan, dependency audit. Nightly workflow exists for live tests. |
| F-E0-04 | S0 | Configuration and secrets | Typed settings load from environment and YAML. Missing required values stop startup with a clear message. `.env.example` lists every variable. |
| F-E0-05 | S0 | Database migrations | Alembic set up for SQLite. Initial migration creates reference and operations tables. Upgrade and downgrade both work. |
| F-E0-06 | S0 | Logging and run ledger | JSON logs carry `run_id`. Every job writes a `job_run` row with status, duration and counts. |
| F-E0-07 | S0 | Errors, retries and rate limiting | Typed exception hierarchy. Shared retry helper with backoff that honours `Retry-After`. Token-bucket rate limiter. |
| F-E0-08 | S0 | Decision records | ADR template and ADR-001 to ADR-009 written and accepted. |
| F-E0-09 | S0 | Prototype disposition | Current `main` tagged `spike-v0`. Prototype code removed from the new layout. A short note lists which ideas were kept and why. |
| F-E0-10 | S0 | Fixture and golden-data policy | Cassette recording with secret scrubbing. Golden data folder with a provenance file per dataset. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E0-01 | CI | F-E0-01 | A deliberate import from `domain` into `adapters` makes the import-contract step fail. |
| T-E0-02 | CI | F-E0-02, F-E0-03 | A PR with an untyped function, a lint error or a failing test is blocked. Verified once per gate and recorded. |
| T-E0-03 | U | F-E0-04 | Missing required setting raises a configuration error that names the variable. |
| T-E0-04 | I | F-E0-05 | Upgrade, downgrade, upgrade on an empty and on a seeded database leaves an identical schema and data. |
| T-E0-05 | CI | F-E0-03, F-E0-04 | A planted fake key in a test branch is caught by the secret scan. |
| T-E0-06 | U | F-E0-06 | Each log line has `run_id`. A regex scan of captured logs finds no secret-shaped strings. |
| T-E0-07 | U | F-E0-07 | Response sequence 429 then 200 causes one retry and waits the `Retry-After` interval. |
| T-E0-08 | P | F-E0-07 | For generated request bursts the limiter never exceeds the configured rate. |
| T-E0-09 | U | F-E0-06 | A job that raises still writes a `job_run` row with status failed and the error type. |
| T-E0-10 | M | F-E0-08, F-E0-09 | Investor reviews the decision records and the prototype disposition note. |
| T-E0-11 | U | F-E0-10 | Recording a cassette with a key in the request stores a scrubbed placeholder. |
| T-E0-12 | CI | F-E0-08, F-E0-09 | Repository check: each decision record exists with status accepted, the tag `spike-v0` exists, and no prototype module path remains. |

## Known limits

- None of the product features exist at the end of this epic. It delivers no investment output.
