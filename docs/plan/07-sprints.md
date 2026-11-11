# 7. Sprint plan

A sprint is one reviewable increment. Nominal length is one week; that is a planning assumption,
not a measured velocity. Building is unlikely to be the constraint. Verifying data against filings
and your milestone reviews are.

Rules for every sprint:

1. Work starts only on features that meet the definition of ready.
2. Each feature lands in its own pull request with the tests listed for it.
3. The sprint closes when its listed tests pass in the pipeline and the exit criteria hold.
4. A test is never weakened to close a sprint. An unmet threshold is reported with its cause.

Feature and test definitions are in the epic files. The lists below are generated from them.


## S0. Foundations  (M0)

**Goal:** A clean repository with pipeline, standards and accepted decisions.

| Feature | Epic | Name |
|---|---|---|
| F-E0-01 | E0 | Repository layout |
| F-E0-02 | E0 | Tooling |
| F-E0-03 | E0 | CI pipeline |
| F-E0-04 | E0 | Configuration and secrets |
| F-E0-05 | E0 | Database migrations |
| F-E0-06 | E0 | Logging and run ledger |
| F-E0-07 | E0 | Errors, retries and rate limiting |
| F-E0-08 | E0 | Decision records |
| F-E0-09 | E0 | Prototype disposition |
| F-E0-10 | E0 | Fixture and golden-data policy |

**Tests that must pass (11):** T-E0-01, T-E0-02, T-E0-03, T-E0-04, T-E0-05, T-E0-06, T-E0-07, T-E0-08, T-E0-09, T-E0-11, T-E0-12

**Manual acceptance at the milestone review:** T-E0-10

**Demo:** A pull request with a type error is blocked; a clean one passes; migrations run up and down.

**Exit criteria:**

- Open questions Q1-Q10 answered
- Decision records ADR-001 to ADR-009 accepted
- Prototype tagged and removed from the new layout

## S1. Reference data, filings, facts  (M1)

**Goal:** Security master, universes, filing index and XBRL facts in a point-in-time store.

| Feature | Epic | Name |
|---|---|---|
| F-E1-01 | E1 | Security master |
| F-E1-02 | E1 | Universe management |
| F-E1-03 | E1 | Filing index ingest |
| F-E1-04 | E1 | XBRL fact ingest |
| F-E1-10 | E1 | Point-in-time store |
| F-E1-12 | E1 | Incremental, idempotent, compliant jobs |

**Tests that must pass (11):** T-E1-01, T-E1-02, T-E1-03, T-E1-04, T-E1-05, T-E1-06, T-E1-11, T-E1-12, T-E1-13, T-E1-14, T-E1-19

**Demo:** Ingest a company you name; rerun shows no changes; query its facts as of a past date.

**Exit criteria:**

- `pilot-25` defined and loaded
- Ingest is idempotent and resumable
- SEC access rules respected

## S2. Prices, text, macro, data quality  (M1)

**Goal:** Prices, corporate actions, macro, benchmarks, filing text, debenture input, snapshots and the data-quality framework.

| Feature | Epic | Name |
|---|---|---|
| F-E1-05 | E1 | Filing text sections |
| F-E1-06 | E1 | Daily prices |
| F-E1-07 | E1 | Corporate actions |
| F-E1-08 | E1 | Macro and rates |
| F-E1-09 | E1 | Benchmarks |
| F-E1-11 | E1 | Data-quality framework |
| F-E1-13 | E1 | Debenture sleeve input |
| F-E1-14 | E1 | Data snapshots |

**Tests that must pass (9):** T-E1-07, T-E1-08, T-E1-09, T-E1-10, T-E1-15, T-E1-16, T-E1-17, T-E1-18, T-E1-20

**Demo:** Data-quality report for `pilot-25`; price-source comparison with a recommendation.

**Exit criteria:**

- Coverage thresholds in T-E1-15 met or exceptions accepted
- Price source decided (ADR-006)
- M1 evidence pack delivered

## S3. Statements core  (M2)

**Goal:** Standard chart of accounts, tag mapping, fiscal calendar, period engine and integrity checks.

| Feature | Epic | Name |
|---|---|---|
| F-E2-01 | E2 | Standard chart of accounts |
| F-E2-02 | E2 | Tag mapping engine |
| F-E2-04 | E2 | Fiscal calendar |
| F-E2-05 | E2 | Period engine |
| F-E2-06 | E2 | Audit status labelling |
| F-E2-09 | E2 | Integrity checks |
| F-E2-11 | E2 | Unit and split normalization |
| F-E2-15 | E2 | Out-of-scope handling |

**Tests that must pass (8):** T-E2-03, T-E2-04, T-E2-05, T-E2-06, T-E2-09, T-E2-10, T-E2-12, T-E2-16

**Demo:** Annual and quarterly statements for the golden companies with every integrity check shown.

**Exit criteria:**

- Golden annual and quarterly values entered by hand from filings
- Integrity checks pass on golden companies
- Excluded sectors return an explicit result

## S4. Statements completion  (M2)

**Goal:** Restatements, assembly with trailing and comparative periods, lineage, export, exception report and reconciliation pack.

| Feature | Epic | Name |
|---|---|---|
| F-E2-03 | E2 | Assisted mapping for custom tags |
| F-E2-07 | E2 | Restatements |
| F-E2-08 | E2 | Statement assembly |
| F-E2-10 | E2 | Lineage |
| F-E2-12 | E2 | Export |
| F-E2-13 | E2 | Coverage and exception report |
| F-E2-14 | E2 | Reconciliation pack |

**Tests that must pass (11):** T-E2-01, T-E2-02, T-E2-07, T-E2-08, T-E2-11, T-E2-13, T-E2-14, T-E2-15, T-E2-17, T-E2-18, T-E2-19

**Manual acceptance at the milestone review:** T-E2-20

**Demo:** Excel workbook and reconciliation pack for five companies you choose.

**Exit criteria:**

- Thresholds in T-E2-14 met on `pilot-25`
- Every exported cell has lineage
- M2 evidence pack delivered

## S5. Metric registry and core metrics  (M3)

**Goal:** Registry plus growth, margin, return, efficiency, leverage and cash-flow metrics, delivered as one summary object.

| Feature | Epic | Name |
|---|---|---|
| F-E3-01 | E3 | Metric registry |
| F-E3-02 | E3 | Growth |
| F-E3-03 | E3 | Margins |
| F-E3-04 | E3 | Returns |
| F-E3-05 | E3 | Efficiency |
| F-E3-06 | E3 | Leverage and liquidity |
| F-E3-07 | E3 | Cash-flow quality |
| F-E3-11 | E3 | Fundamental summary object |

**Tests that must pass (9):** T-E3-02, T-E3-03, T-E3-04, T-E3-07, T-E3-08, T-E3-09, T-E3-10, T-E3-12, T-E3-13

**Manual acceptance at the milestone review:** T-E3-15

**Demo:** Fundamental summary for the golden companies beside the hand-calculated spreadsheet.

**Exit criteria:**

- Golden metrics match
- Null policy applied everywhere
- Metric definitions reviewed

## S6. Quality scores and peer groups  (M3)

**Goal:** Earnings-quality scores, capital allocation, trends, red flags, and the full peer service.

| Feature | Epic | Name |
|---|---|---|
| F-E3-08 | E3 | Earnings-quality scores |
| F-E3-09 | E3 | Capital allocation |
| F-E3-10 | E3 | Trend and stability |
| F-E3-12 | E3 | Red-flag rules |
| F-E4-01 | E4 | Industry candidates |
| F-E4-02 | E4 | Size filter |
| F-E4-03 | E4 | Business similarity |
| F-E4-04 | E4 | Selection |
| F-E4-05 | E4 | Analyst override |
| F-E4-06 | E4 | Peer statistics |
| F-E4-07 | E4 | Relative valuation table |
| F-E4-08 | E4 | Versioning |
| F-E4-09 | E4 | Justification record |

**Tests that must pass (15):** T-E3-01, T-E3-05, T-E3-06, T-E3-11, T-E3-14, T-E4-01, T-E4-02, T-E4-03, T-E4-04, T-E4-05, T-E4-06, T-E4-07, T-E4-08, T-E4-09, T-E4-10

**Manual acceptance at the milestone review:** T-E4-11

**Demo:** Peer sets and relative tables for ten companies; red flags with cited figures.

**Exit criteria:**

- Known peer pairs found
- Overrides persist
- M3 evidence pack delivered

## S7. Screen and discounted cash flow  (M4)

**Goal:** Eligibility and factor screen, cost of capital, valuation engine, scenarios, sensitivities and the model registry.

| Feature | Epic | Name |
|---|---|---|
| F-E5-01 | E5 | Eligibility filters |
| F-E5-02 | E5 | Factor scores |
| F-E5-03 | E5 | Screen output |
| F-E5-04 | E5 | Cost of capital |
| F-E5-05 | E5 | Discounted cash-flow engine |
| F-E5-06 | E5 | Scenario engine |
| F-E5-07 | E5 | Sensitivity tables |
| F-E5-15 | E5 | Model registry |

**Tests that must pass (11):** T-E5-01, T-E5-02, T-E5-03, T-E5-04, T-E5-05, T-E5-06, T-E5-07, T-E5-08, T-E5-09, T-E5-16, T-E5-18

**Demo:** Valuation of a company you name, with scenarios and sensitivity tables; the ranked shortlist.

**Exit criteria:**

- Textbook valuation reproduced
- Property tests pass
- Outputs reproducible from a snapshot id

## S8. Relative valuation and medium-term signals  (M4)

**Goal:** Reverse valuation, multiples, synthesis, trend, momentum, earnings and risk-state signals, charts, and the optional-feeds assessment.

| Feature | Epic | Name |
|---|---|---|
| F-E1-15 | E1 | Optional feeds decision |
| F-E5-08 | E5 | Reverse discounted cash flow |
| F-E5-09 | E5 | Multiples valuation |
| F-E5-10 | E5 | Valuation synthesis |
| F-E5-11 | E5 | Trend and momentum |
| F-E5-12 | E5 | Earnings signals |
| F-E5-13 | E5 | Risk-state filter |
| F-E5-14 | E5 | Signal combiner |
| F-E11-03 | E11 | Charts from own data |

**Tests that must pass (9):** T-E5-10, T-E5-11, T-E5-12, T-E5-13, T-E5-14, T-E5-15, T-E5-17, T-E5-19, T-E11-09

**Manual acceptance at the milestone review:** T-E1-21, T-E5-20

**Demo:** Valuation synthesis and signal charts for the shortlist.

**Exit criteria:**

- No-look-ahead perturbation test passes
- Optional-feeds decision recorded
- M4 evidence pack delivered

## S9. Agent platform  (M5)

**Goal:** Provider adapters, team configuration, read-only tools, memo schema, workflow, budgets, traces and prompt versioning.

| Feature | Epic | Name |
|---|---|---|
| F-E6-01 | E6 | Provider abstraction |
| F-E6-02 | E6 | Team configuration |
| F-E6-03 | E6 | Read-only agent tools |
| F-E6-04 | E6 | Memo schema |
| F-E6-05 | E6 | Workflow |
| F-E6-06 | E6 | Structured-output robustness |
| F-E6-07 | E6 | Budgets and limits |
| F-E6-08 | E6 | Trace store |
| F-E6-09 | E6 | Prompt management |

**Tests that must pass (11):** T-E6-01, T-E6-02, T-E6-03, T-E6-04, T-E6-05, T-E6-06, T-E6-07, T-E6-08, T-E6-11, T-E6-12, T-E6-14

**Demo:** A memo produced from recorded responses, then one live memo for a single company inside a set budget.

**Exit criteria:**

- All adapters pass the contract suite
- Numbers outside tool results are rejected
- Every call traced with cost

## S10. Evaluation core  (M5)

**Goal:** Rubric, deterministic judge, concurrence gate, defect library, score store; untrusted-text handling, cache, narrative rendering and cost tracking.

| Feature | Epic | Name |
|---|---|---|
| F-E6-10 | E6 | Untrusted-text handling |
| F-E6-11 | E6 | Response cache |
| F-E6-12 | E6 | Narrative rendering |
| F-E7-01 | E7 | Rubric as versioned config |
| F-E7-02 | E7 | Deterministic judge |
| F-E7-04 | E7 | Concurrence gate |
| F-E7-05 | E7 | Defect library and judge mutation testing |
| F-E7-12 | E7 | Score store and scorecard data |
| F-E12-05 | E12 | Cost tracking |

**Tests that must pass (10):** T-E6-09, T-E6-10, T-E6-13, T-E7-01, T-E7-02, T-E7-03, T-E7-04, T-E7-08, T-E7-18, T-E12-05

**Demo:** Mutation-test report showing which injected defects the deterministic judge catches.

**Exit criteria:**

- Threshold in T-E7-04 met
- Gate truth table passes
- Coverage statement for the deterministic judge written

## S11. LLM judge, calibration, reflection, benchmark  (M5)

**Goal:** Blind LLM judge, calibration against your grades, drift monitoring, targeted reflection, lessons, the team benchmark, and memo and scorecard rendering.

| Feature | Epic | Name |
|---|---|---|
| F-E7-03 | E7 | LLM judge |
| F-E7-06 | E7 | Human gold set and calibration |
| F-E7-07 | E7 | Judge drift monitoring |
| F-E7-08 | E7 | Targeted reflection loop |
| F-E7-09 | E7 | Cross-run lessons |
| F-E7-11 | E7 | Team benchmark harness |
| F-E11-01 | E11 | Stock memo renderer |
| F-E11-02 | E11 | Evaluation scorecard view |

**Tests that must pass (15):** T-E7-05, T-E7-06, T-E7-07, T-E7-09, T-E7-10, T-E7-11, T-E7-12, T-E7-13, T-E7-14, T-E7-15, T-E7-17, T-E7-19, T-E11-01, T-E11-02, T-E11-03

**Manual acceptance at the milestone review:** T-E7-20

**Demo:** Calibration report, saturation test result, and the benchmark of team shapes.

**Exit criteria:**

- Thresholds in T-E7-05, T-E7-09 and T-E7-10 met
- Default team shape chosen from benchmark results
- M5 evidence pack delivered

## S12. Backtest engine  (M6)

**Goal:** Event-driven engine on point-in-time data with cash-account rules, costs, benchmarks, metrics and run manifests.

| Feature | Epic | Name |
|---|---|---|
| F-E8-01 | E8 | Daily event-driven engine |
| F-E8-02 | E8 | Point-in-time inputs |
| F-E8-03 | E8 | Cash-account rules |
| F-E8-04 | E8 | Cost model |
| F-E8-05 | E8 | Shared strategy interface |
| F-E8-06 | E8 | Benchmarks |
| F-E8-07 | E8 | Metrics and tearsheet |
| F-E8-11 | E8 | Run manifest |

**Tests that must pass (10):** T-E8-01, T-E8-02, T-E8-03, T-E8-04, T-E8-06, T-E8-07, T-E8-08, T-E8-09, T-E8-12, T-E8-13

**Demo:** Buy-and-hold reproduction of the benchmark; first tearsheet for the core strategy.

**Exit criteria:**

- Benchmark reproduced within tolerance
- Accounting identity holds daily
- Reruns identical

## S13. Backtest validation and portfolio construction  (M6)

**Goal:** Walk-forward and cross-validation, bias detectors, small-account analysis, strategy scoring; mandate config, core and tactical construction, exit rules.

| Feature | Epic | Name |
|---|---|---|
| F-E8-08 | E8 | Validation methods |
| F-E8-09 | E8 | Bias detectors |
| F-E8-10 | E8 | Small-account analysis |
| F-E8-12 | E8 | Strategy rubric scoring |
| F-E9-01 | E9 | Mandate configuration |
| F-E9-02 | E9 | Core construction |
| F-E9-03 | E9 | Tactical construction |
| F-E9-04 | E9 | Exit rules |

**Tests that must pass (11):** T-E8-05, T-E8-10, T-E8-11, T-E8-14, T-E8-15, T-E8-16, T-E9-01, T-E9-02, T-E9-03, T-E9-04, T-E9-12

**Manual acceptance at the milestone review:** T-E8-17

**Demo:** Validated tearsheets for both strategies; a constructed portfolio for USD 5,000.

**Exit criteria:**

- Look-ahead canary caught
- Survivorship coverage and trial count on every tearsheet
- Constraint property tests pass

## S14. Risk controls and proposals  (M6)

**Goal:** Pre-trade checks, risk and allocation monitors, order proposals tied to the gate, ledger and what-if view.

| Feature | Epic | Name |
|---|---|---|
| F-E9-05 | E9 | Pre-trade checks |
| F-E9-06 | E9 | Risk monitor |
| F-E9-07 | E9 | Allocation monitor |
| F-E9-08 | E9 | Order proposal generator |
| F-E9-09 | E9 | Ledger |
| F-E9-10 | E9 | What-if view |

**Tests that must pass (8):** T-E9-05, T-E9-06, T-E9-07, T-E9-08, T-E9-09, T-E9-10, T-E9-11, T-E9-13

**Demo:** Order proposals for the constructed portfolio in the what-if view, with each limit shown.

**Exit criteria:**

- No buy proposal without a passing memo
- Ledger property tests pass
- M6 evidence pack delivered and decision recorded

## S15. Execution on paper  (M7)

**Goal:** Broker protocol and adapters, connectivity, approvals, order management, reconciliation, safety controls, audit log, runtime packaging.

| Feature | Epic | Name |
|---|---|---|
| F-E10-01 | E10 | Broker protocol |
| F-E10-02 | E10 | Connectivity |
| F-E10-03 | E10 | Contract resolution |
| F-E10-04 | E10 | Approval workflow |
| F-E10-05 | E10 | Order management |
| F-E10-06 | E10 | Reconciliation |
| F-E10-07 | E10 | Safety controls |
| F-E10-08 | E10 | Audit log |
| F-E10-09 | E10 | Execution quotes |
| F-E10-10 | E10 | Go-live checklist |
| F-E12-02 | E12 | Runtime and packaging |

**Tests that must pass (14):** T-E10-01, T-E10-02, T-E10-03, T-E10-04, T-E10-05, T-E10-06, T-E10-07, T-E10-08, T-E10-09, T-E10-10, T-E10-11, T-E10-12, T-E10-14, T-E12-02

**Manual acceptance at the milestone review:** T-E10-13

**Demo:** One paper order from proposal through approval to fill and reconciliation.

**Exit criteria:**

- Live adapter refuses to connect with the flag off
- Failure-injection test passes
- Go-live checklist written

## S16. Reporting, TradingView and operations  (M7)

**Goal:** Weekly report, dashboard, TradingView export and alert receiver, notifications, scheduler, backups, observability, security, runbooks, outcome reflection.

| Feature | Epic | Name |
|---|---|---|
| F-E7-10 | E7 | Outcome reflection |
| F-E11-04 | E11 | Weekly portfolio report |
| F-E11-05 | E11 | Dashboard |
| F-E11-06 | E11 | TradingView export |
| F-E11-07 | E11 | TradingView alert receiver |
| F-E11-08 | E11 | Notifications |
| F-E12-01 | E12 | Scheduler |
| F-E12-03 | E12 | Backups |
| F-E12-04 | E12 | Observability |
| F-E12-06 | E12 | Security |
| F-E12-07 | E12 | Runbooks |
| F-E12-08 | E12 | Disaster-recovery drill |

**Tests that must pass (11):** T-E7-16, T-E11-04, T-E11-05, T-E11-06, T-E11-07, T-E11-08, T-E12-01, T-E12-03, T-E12-04, T-E12-06, T-E12-08

**Manual acceptance at the milestone review:** T-E11-10, T-E12-07

**Demo:** A week of unattended scheduled runs on paper; a TradingView alert arriving as a review task; a restore from backup.

**Exit criteria:**

- Scheduler ran unattended for one week
- Restore verified
- M7 evidence pack delivered
