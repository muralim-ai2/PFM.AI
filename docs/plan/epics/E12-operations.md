# E12. Operations

**Goal:** the system runs on a schedule without supervision, recovers from failure, keeps its data safe, and reports what it costs.
**Depends on:** the runtime decision (open question Q1).
**Milestone:** M7 (cost tracking earlier, at M5).

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E12-01 | S16 | Scheduler | Daily jobs (prices, filings, monitors), weekly (screen, proposals), quarterly (re-underwriting, outcome review). Dependency-aware. Catches up after downtime. |
| F-E12-02 | S15 | Runtime and packaging | Container image for the services, co-located with the broker gateway. Environment documented for the chosen host. |
| F-E12-03 | S16 | Backups | Nightly encrypted snapshot of the database and series files to storage off the machine, with retention. |
| F-E12-04 | S16 | Observability | Job durations, failures and data freshness recorded, with alerts. |
| F-E12-05 | S10 | Cost tracking | Model cost per call, memo, run and month; data subscriptions recorded; budget alerts. |
| F-E12-06 | S16 | Security | Secrets outside the repo, least-privilege keys, read-only broker session for monitoring, dependency audit, software bill of materials. |
| F-E12-07 | S16 | Runbooks | Ingest failure, reconciliation break, broker outage, bad-data rollback, key rotation. |
| F-E12-08 | S16 | Disaster-recovery drill | Restore to a clean machine from backup following the runbook. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E12-01 | I | F-E12-01 | Missed runs catch up in order. A failed dependency skips its dependents and records why. |
| T-E12-02 | CI | F-E12-02 | The image builds in the pipeline and its smoke test passes. |
| T-E12-03 | I | F-E12-03, F-E12-08 | Backup then restore into an empty directory gives matching row counts and file hashes. |
| T-E12-04 | U | F-E12-04 | Prices older than two trading days raise a freshness alert. |
| T-E12-05 | U | F-E12-05 | The cost ledger equals the sum of traced call costs; an alert fires at the budget threshold. |
| T-E12-06 | CI | F-E12-06 | Dependency audit reports no high-severity findings and the secret scan is clean. |
| T-E12-07 | M | F-E12-07, F-E12-08 | Investor carries out the disaster-recovery drill from the runbook. |
| T-E12-08 | CI | F-E12-07 | Each runbook file exists and has the required sections: trigger, diagnosis, steps, verification. |

## Known limits

- Availability depends on the host. A laptop that sleeps misses scheduled runs; the scheduler catches up but alerts are delayed.
