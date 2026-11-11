# 9. Traceability

Generated from the epic files. Every feature has at least one automated test, except decision-only deliverables verified at the milestone review (F-E1-15). Every test names the features it covers.

Totals: 148 features, 195 tests.

## 9.1 Counts by epic

| Epic | Features | Tests | Sprints |
|---|---|---|---|
| E0. Foundations and engineering platform | 10 | 12 | S0 |
| E1. Data collection | 15 | 21 | S1, S2, S8 |
| E2. Financial statements service | 15 | 20 | S3, S4 |
| E3. Fundamental analysis service | 12 | 15 | S5, S6 |
| E4. Peer group service | 9 | 11 | S6 |
| E5. Valuation and models service | 15 | 20 | S7, S8 |
| E6. Agent teams | 12 | 14 | S9, S10 |
| E7. Evaluation and reflection | 12 | 20 | S10, S11, S16 |
| E8. Backtesting and benchmarking | 12 | 17 | S12, S13 |
| E9. Portfolio construction and risk | 10 | 13 | S13, S14 |
| E10. Execution and approvals | 10 | 14 | S15 |
| E11. Reporting, dashboard and TradingView | 8 | 10 | S8, S11, S16 |
| E12. Operations | 8 | 8 | S10, S15, S16 |

## 9.2 Counts by test type

| Type | Tests |
|---|---|
| U | 117 |
| I | 21 |
| P | 12 |
| M | 11 |
| G | 8 |
| EV | 8 |
| CI | 7 |
| C | 6 |
| DQ | 4 |
| E2E | 1 |

## 9.3 Feature to tests

| Feature | Name | Sprint | Milestone | Tests |
|---|---|---|---|---|
| F-E0-01 | Repository layout | S0 | M0 | T-E0-01 |
| F-E0-02 | Tooling | S0 | M0 | T-E0-02 |
| F-E0-03 | CI pipeline | S0 | M0 | T-E0-02, T-E0-05 |
| F-E0-04 | Configuration and secrets | S0 | M0 | T-E0-03, T-E0-05 |
| F-E0-05 | Database migrations | S0 | M0 | T-E0-04 |
| F-E0-06 | Logging and run ledger | S0 | M0 | T-E0-06, T-E0-09 |
| F-E0-07 | Errors, retries and rate limiting | S0 | M0 | T-E0-07, T-E0-08 |
| F-E0-08 | Decision records | S0 | M0 | T-E0-10, T-E0-12 |
| F-E0-09 | Prototype disposition | S0 | M0 | T-E0-10, T-E0-12 |
| F-E0-10 | Fixture and golden-data policy | S0 | M0 | T-E0-11 |
| F-E1-01 | Security master | S1 | M1 | T-E1-02 |
| F-E1-02 | Universe management | S1 | M1 | T-E1-15, T-E1-19 |
| F-E1-03 | Filing index ingest | S1 | M1 | T-E1-01, T-E1-03, T-E1-04 |
| F-E1-04 | XBRL fact ingest | S1 | M1 | T-E1-05, T-E1-06 |
| F-E1-05 | Filing text sections | S2 | M1 | T-E1-07 |
| F-E1-06 | Daily prices | S2 | M1 | T-E1-10, T-E1-20 |
| F-E1-07 | Corporate actions | S2 | M1 | T-E1-08, T-E1-09 |
| F-E1-08 | Macro and rates | S2 | M1 | T-E1-16 |
| F-E1-09 | Benchmarks | S2 | M1 | T-E1-09 |
| F-E1-10 | Point-in-time store | S1 | M1 | T-E1-11, T-E1-12 |
| F-E1-11 | Data-quality framework | S2 | M1 | T-E1-10, T-E1-15, T-E1-21 |
| F-E1-12 | Incremental, idempotent, compliant jobs | S1 | M1 | T-E1-03, T-E1-13, T-E1-14 |
| F-E1-13 | Debenture sleeve input | S2 | M1 | T-E1-17 |
| F-E1-14 | Data snapshots | S2 | M1 | T-E1-18 |
| F-E1-15 | Optional feeds decision | S8 | M4 | T-E1-21 |
| F-E2-01 | Standard chart of accounts | S3 | M2 | T-E2-01 |
| F-E2-02 | Tag mapping engine | S3 | M2 | T-E2-01, T-E2-06, T-E2-07 |
| F-E2-03 | Assisted mapping for custom tags | S4 | M2 | T-E2-15 |
| F-E2-04 | Fiscal calendar | S3 | M2 | T-E2-05 |
| F-E2-05 | Period engine | S3 | M2 | T-E2-02, T-E2-03, T-E2-04 |
| F-E2-06 | Audit status labelling | S3 | M2 | T-E2-03 |
| F-E2-07 | Restatements | S4 | M2 | T-E2-08, T-E2-17 |
| F-E2-08 | Statement assembly | S4 | M2 | T-E2-01, T-E2-02, T-E2-17, T-E2-18 |
| F-E2-09 | Integrity checks | S3 | M2 | T-E2-09, T-E2-10, T-E2-14 |
| F-E2-10 | Lineage | S4 | M2 | T-E2-11 |
| F-E2-11 | Unit and split normalization | S3 | M2 | T-E2-12 |
| F-E2-12 | Export | S4 | M2 | T-E2-13, T-E2-20 |
| F-E2-13 | Coverage and exception report | S4 | M2 | T-E2-07, T-E2-14 |
| F-E2-14 | Reconciliation pack | S4 | M2 | T-E2-19, T-E2-20 |
| F-E2-15 | Out-of-scope handling | S3 | M2 | T-E2-16 |
| F-E3-01 | Metric registry | S5 | M3 | T-E3-03, T-E3-09, T-E3-10 |
| F-E3-02 | Growth | S5 | M3 | T-E3-01, T-E3-04 |
| F-E3-03 | Margins | S5 | M3 | T-E3-01, T-E3-10 |
| F-E3-04 | Returns | S5 | M3 | T-E3-01, T-E3-02, T-E3-08 |
| F-E3-05 | Efficiency | S5 | M3 | T-E3-01 |
| F-E3-06 | Leverage and liquidity | S5 | M3 | T-E3-01, T-E3-07 |
| F-E3-07 | Cash-flow quality | S5 | M3 | T-E3-01 |
| F-E3-08 | Earnings-quality scores | S6 | M3 | T-E3-05, T-E3-06 |
| F-E3-09 | Capital allocation | S6 | M3 | T-E3-01 |
| F-E3-10 | Trend and stability | S6 | M3 | T-E3-14 |
| F-E3-11 | Fundamental summary object | S5 | M3 | T-E3-12, T-E3-13, T-E3-15 |
| F-E3-12 | Red-flag rules | S6 | M3 | T-E3-11 |
| F-E4-01 | Industry candidates | S6 | M3 | T-E4-01 |
| F-E4-02 | Size filter | S6 | M3 | T-E4-03 |
| F-E4-03 | Business similarity | S6 | M3 | T-E4-01, T-E4-09 |
| F-E4-04 | Selection | S6 | M3 | T-E4-01, T-E4-02, T-E4-04, T-E4-11 |
| F-E4-05 | Analyst override | S6 | M3 | T-E4-05, T-E4-11 |
| F-E4-06 | Peer statistics | S6 | M3 | T-E4-06, T-E4-07 |
| F-E4-07 | Relative valuation table | S6 | M3 | T-E4-07 |
| F-E4-08 | Versioning | S6 | M3 | T-E4-08 |
| F-E4-09 | Justification record | S6 | M3 | T-E4-10 |
| F-E5-01 | Eligibility filters | S7 | M4 | T-E5-01 |
| F-E5-02 | Factor scores | S7 | M4 | T-E5-02, T-E5-03 |
| F-E5-03 | Screen output | S7 | M4 | T-E5-02, T-E5-17 |
| F-E5-04 | Cost of capital | S7 | M4 | T-E5-04, T-E5-05 |
| F-E5-05 | Discounted cash-flow engine | S7 | M4 | T-E5-06, T-E5-07, T-E5-08 |
| F-E5-06 | Scenario engine | S7 | M4 | T-E5-09, T-E5-20 |
| F-E5-07 | Sensitivity tables | S7 | M4 | T-E5-18 |
| F-E5-08 | Reverse discounted cash flow | S8 | M4 | T-E5-10 |
| F-E5-09 | Multiples valuation | S8 | M4 | T-E5-11 |
| F-E5-10 | Valuation synthesis | S8 | M4 | T-E5-12, T-E5-17, T-E5-20 |
| F-E5-11 | Trend and momentum | S8 | M4 | T-E5-13, T-E5-14 |
| F-E5-12 | Earnings signals | S8 | M4 | T-E5-13, T-E5-15 |
| F-E5-13 | Risk-state filter | S8 | M4 | T-E5-13, T-E5-19 |
| F-E5-14 | Signal combiner | S8 | M4 | T-E5-13, T-E5-19 |
| F-E5-15 | Model registry | S7 | M4 | T-E5-16 |
| F-E6-01 | Provider abstraction | S9 | M5 | T-E6-01, T-E6-02 |
| F-E6-02 | Team configuration | S9 | M5 | T-E6-03 |
| F-E6-03 | Read-only agent tools | S9 | M5 | T-E6-04 |
| F-E6-04 | Memo schema | S9 | M5 | T-E6-11, T-E6-14 |
| F-E6-05 | Workflow | S9 | M5 | T-E6-05, T-E6-11 |
| F-E6-06 | Structured-output robustness | S9 | M5 | T-E6-06 |
| F-E6-07 | Budgets and limits | S9 | M5 | T-E6-07 |
| F-E6-08 | Trace store | S9 | M5 | T-E6-08 |
| F-E6-09 | Prompt management | S9 | M5 | T-E6-12 |
| F-E6-10 | Untrusted-text handling | S10 | M5 | T-E6-09 |
| F-E6-11 | Response cache | S10 | M5 | T-E6-13 |
| F-E6-12 | Narrative rendering | S10 | M5 | T-E6-10 |
| F-E7-01 | Rubric as versioned config | S10 | M5 | T-E7-01 |
| F-E7-02 | Deterministic judge | S10 | M5 | T-E7-02, T-E7-03, T-E7-04 |
| F-E7-03 | LLM judge | S11 | M5 | T-E7-05, T-E7-06, T-E7-07, T-E7-09, T-E7-19 |
| F-E7-04 | Concurrence gate | S10 | M5 | T-E7-08, T-E7-09 |
| F-E7-05 | Defect library and judge mutation testing | S10 | M5 | T-E7-04, T-E7-05 |
| F-E7-06 | Human gold set and calibration | S11 | M5 | T-E7-10, T-E7-20 |
| F-E7-07 | Judge drift monitoring | S11 | M5 | T-E7-15 |
| F-E7-08 | Targeted reflection loop | S11 | M5 | T-E7-11, T-E7-12 |
| F-E7-09 | Cross-run lessons | S11 | M5 | T-E7-17 |
| F-E7-10 | Outcome reflection | S16 | M7 | T-E7-16 |
| F-E7-11 | Team benchmark harness | S11 | M5 | T-E7-13, T-E7-14, T-E7-20 |
| F-E7-12 | Score store and scorecard data | S10 | M5 | T-E7-18 |
| F-E8-01 | Daily event-driven engine | S12 | M6 | T-E8-01, T-E8-02 |
| F-E8-02 | Point-in-time inputs | S12 | M6 | T-E8-06, T-E8-08 |
| F-E8-03 | Cash-account rules | S12 | M6 | T-E8-03, T-E8-04 |
| F-E8-04 | Cost model | S12 | M6 | T-E8-02, T-E8-07 |
| F-E8-05 | Shared strategy interface | S12 | M6 | T-E8-13 |
| F-E8-06 | Benchmarks | S12 | M6 | T-E8-01 |
| F-E8-07 | Metrics and tearsheet | S12 | M6 | T-E8-09, T-E8-17 |
| F-E8-08 | Validation methods | S13 | M6 | T-E8-10, T-E8-11 |
| F-E8-09 | Bias detectors | S13 | M6 | T-E8-05, T-E8-16 |
| F-E8-10 | Small-account analysis | S13 | M6 | T-E8-14, T-E8-17 |
| F-E8-11 | Run manifest | S12 | M6 | T-E8-12 |
| F-E8-12 | Strategy rubric scoring | S13 | M6 | T-E8-15 |
| F-E9-01 | Mandate configuration | S13 | M6 | T-E9-01, T-E9-03 |
| F-E9-02 | Core construction | S13 | M6 | T-E9-01, T-E9-02, T-E9-03 |
| F-E9-03 | Tactical construction | S13 | M6 | T-E9-01, T-E9-12 |
| F-E9-04 | Exit rules | S13 | M6 | T-E9-04 |
| F-E9-05 | Pre-trade checks | S14 | M6 | T-E9-05 |
| F-E9-06 | Risk monitor | S14 | M6 | T-E9-06, T-E9-13 |
| F-E9-07 | Allocation monitor | S14 | M6 | T-E9-07 |
| F-E9-08 | Order proposal generator | S14 | M6 | T-E9-08, T-E9-11 |
| F-E9-09 | Ledger | S14 | M6 | T-E9-09, T-E9-10 |
| F-E9-10 | What-if view | S14 | M6 | T-E9-11 |
| F-E10-01 | Broker protocol | S15 | M7 | T-E10-01 |
| F-E10-02 | Connectivity | S15 | M7 | T-E10-05 |
| F-E10-03 | Contract resolution | S15 | M7 | T-E10-11, T-E10-12 |
| F-E10-04 | Approval workflow | S15 | M7 | T-E10-04, T-E10-13 |
| F-E10-05 | Order management | S15 | M7 | T-E10-02, T-E10-03, T-E10-05, T-E10-09, T-E10-11 |
| F-E10-06 | Reconciliation | S15 | M7 | T-E10-06, T-E10-11 |
| F-E10-07 | Safety controls | S15 | M7 | T-E10-07, T-E10-08, T-E10-14 |
| F-E10-08 | Audit log | S15 | M7 | T-E10-10 |
| F-E10-09 | Execution quotes | S15 | M7 | T-E10-09 |
| F-E10-10 | Go-live checklist | S15 | M7 | T-E10-13, T-E10-14 |
| F-E11-01 | Stock memo renderer | S11 | M5 | T-E11-01, T-E11-02, T-E11-10 |
| F-E11-02 | Evaluation scorecard view | S11 | M5 | T-E11-03 |
| F-E11-03 | Charts from own data | S8 | M4 | T-E11-09 |
| F-E11-04 | Weekly portfolio report | S16 | M7 | T-E11-04, T-E11-10 |
| F-E11-05 | Dashboard | S16 | M7 | T-E11-05, T-E11-10 |
| F-E11-06 | TradingView export | S16 | M7 | T-E11-06 |
| F-E11-07 | TradingView alert receiver | S16 | M7 | T-E11-07 |
| F-E11-08 | Notifications | S16 | M7 | T-E11-08 |
| F-E12-01 | Scheduler | S16 | M7 | T-E12-01 |
| F-E12-02 | Runtime and packaging | S15 | M7 | T-E12-02 |
| F-E12-03 | Backups | S16 | M7 | T-E12-03 |
| F-E12-04 | Observability | S16 | M7 | T-E12-04 |
| F-E12-05 | Cost tracking | S10 | M5 | T-E12-05 |
| F-E12-06 | Security | S16 | M7 | T-E12-06 |
| F-E12-07 | Runbooks | S16 | M7 | T-E12-07, T-E12-08 |
| F-E12-08 | Disaster-recovery drill | S16 | M7 | T-E12-03, T-E12-07 |
