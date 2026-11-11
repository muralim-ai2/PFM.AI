# PFM.AI delivery plan

Plan only. No product code is on this branch beyond what `main` already had, and that code is
treated as a discarded prototype (see `01-scope-and-decisions.md`, section 1.5).

## Read in this order

| File | Content |
|---|---|
| `01-scope-and-decisions.md` | Mandate, scope, exclusions, open questions for you, decisions to ratify |
| `02-architecture.md` | Layers, data flow, time model, entities |
| `03-engineering-standards.md` | Coding, testing and workflow standards; definitions of ready and done |
| `04-test-strategy.md` | Test types, reference datasets, guards for each failure mode |
| `05-accounts-and-signups.md` | What you need to sign up for, when, and what it costs |
| `06-milestones.md` | Nine review gates: what you provide, what you check, exit criteria |
| `07-sprints.md` | Seventeen sprints with features, tests, demo and exit criteria |
| `08-risks.md` | Risk register |
| `09-traceability.md` | Every feature mapped to sprint, milestone and tests |
| `epics/` | Thirteen epics: features with acceptance checks, and a test specification for each |

## Shape of the plan

| Milestone | Sprints | Delivers | You sign up for |
|---|---|---|---|
| M0 Foundations | S0 | Repository, pipeline, standards, decisions | nothing new |
| M1 Data platform | S1-S2 | Filings, facts, prices, macro, point-in-time store, quality report | SEC contact email, FRED key, price source |
| M2 Financial statements | S3-S4 | Three audited years plus interim periods, reconciled, exportable | nothing new |
| M3 Fundamentals and peers | S5-S6 | Metrics, quality scores, peer sets | embedding provider |
| M4 Valuation and models | S7-S8 | Screen, valuation, medium-term signals | start the IBKR application |
| M5 Agents and evaluation | S9-S11 | Memos, two concurring judges, calibration, team benchmark | model API account |
| M6 Backtest and portfolio | S12-S14 | Validated backtests, mandate-compliant proposals | nothing new |
| M7 Execution and operations | S15-S16 | Paper trading with approvals, reports, dashboard, schedule | IBKR funded with paper trading, TradingView paid plan |
| M8 Paper period | 12 weeks | Go-live decision | nothing new |

Totals: 13 epics, 148 features, 195 test specifications.

## Identifiers

- Features: `F-E<epic>-<nn>`. Tests: `T-E<epic>-<nn>`. Sprints: `S<n>`. Milestones: `M<n>`.
- Test ids appear in test names when the tests are written, so the pipeline report maps back to this plan.

## How to review this plan

1. Answer the open questions in `01-scope-and-decisions.md`, section 1.6.
2. Check the rubric and gate rules in `epics/E07-evaluation-and-reflection.md`.
3. Check the two services you named as essential: `epics/E02-financial-statements.md` and `epics/E05-valuation-and-models.md`, with `E03` and `E04`.
4. Check the milestone gates in `06-milestones.md`: are these the points at which you want to stop and inspect?
5. Mark anything missing or wrong on the pull request. The plan changes before any code is written.

## Maintaining the plan

The epic files are the source of truth. `07-sprints.md` feature and test lists and
`09-traceability.md` are generated from them and checked for consistency: every feature has a
sprint and at least one test, every test names existing features, and no id is used twice.
