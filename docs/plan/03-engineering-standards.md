# 3. Engineering standards

These apply from Sprint 0. A feature that does not meet them is not done.

## 3.1 Code

| Topic | Standard |
|---|---|
| Language | Python 3.12, `src/` layout, one package `pfm` |
| Dependencies | `uv` with a committed lockfile; no unpinned installs |
| Style | `ruff` for lint and format; line length 100 |
| Types | `mypy --strict` on `src/`; no untyped public functions |
| Structure | domain / services / adapters / interfaces, enforced with `import-linter` |
| Interfaces | `typing.Protocol` for data providers, LLM providers, broker, storage |
| Domain models | Frozen dataclasses or pydantic models; no dict-passing across service boundaries |
| Money and reported values | `Decimal`; float only for ratios, returns and statistics |
| Time | Timezone-aware UTC internally; trading calendar from `exchange_calendars` |
| Errors | Typed exception hierarchy; no bare `except`; fail closed on anything touching orders |
| Config | `pydantic-settings`; all tunables in versioned YAML; no constants buried in code |
| Secrets | Environment only; `.env.example` committed, `.env` ignored; never logged |
| Logging | Structured JSON with `run_id`; no print statements in library code |
| Database | Alembic migrations, forward and backward tested; no schema changes outside migrations |
| Functions | Small and single-purpose; pure where possible; side effects at the edges |
| Comments | Explain why, not what; public functions have docstrings with units |

## 3.2 Testing

| Topic | Standard |
|---|---|
| Framework | `pytest`, `hypothesis` for property tests, recorded HTTP cassettes for vendors |
| Order of work | Test specs in this plan come first; tests are written with the feature in the same PR |
| Coverage | 90% line coverage on `domain` and `services`, 80% overall, enforced in CI |
| Determinism | No network, clock or randomness in unit tests; seeds fixed and recorded |
| Golden data | Hand-verified reference values stored with source and verifier; changes need review |
| Live tests | Marked `live`; run nightly or on demand with a cost cap; never block a PR |
| Naming | Test ids from this plan appear in the test name or marker, e.g. `test_T_E2_03_...` |

## 3.3 Workflow

| Topic | Standard |
|---|---|
| Branching | Trunk-based. Short-lived branches `feat/E2-05-period-engine`; PR into `main` |
| Commits | Conventional Commits; one logical change each |
| Pull requests | Under about 400 changed lines where possible; description lists feature and test ids |
| Review | Every PR reviewed before merge; milestone PRs reviewed by the investor |
| CI on PR | format, lint, types, import contracts, unit and integration tests, coverage, secret scan, dependency audit |
| CI nightly | Live contract tests, data-quality run on the pilot universe, judge anchor re-score |
| Releases | Tag per milestone `m1`, `m2`, ...; changelog generated from commits |
| Decisions | Architecture decision records in `docs/adr/`; one per significant choice |

## 3.4 Definition of ready

A feature can start when:

1. Its acceptance checks and test ids exist in the epic file.
2. Inputs it depends on are done or stubbed behind a protocol.
3. Any account, key or paid subscription it needs is available.
4. Open questions that affect it are answered.

## 3.5 Definition of done

A feature is done when:

1. All its listed tests pass in CI, and no existing test was weakened to get there.
2. Coverage and type gates hold.
3. Its acceptance checks are demonstrated on real data where the check calls for real data.
4. Migrations, config and docs are updated.
5. Outputs carry versions and lineage as the architecture requires.
6. Known limits are written down in the epic file, not left implicit.

## 3.6 Rules specific to this system

- A number shown to the investor comes from a registered formula or a source record. An LLM never types one.
- No look-ahead: any read used for a decision goes through `as_of`.
- The same strategy code runs in backtest, paper and live.
- No order leaves the system without a matching approval record.
- A tolerance or threshold is never loosened to make a check pass. The cause is found or the exception is recorded with a reason.
