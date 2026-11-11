# 6. Milestones and review gates

Each milestone ends with a review. Work on the next milestone starts only after a go decision,
recorded in `docs/reviews/Mx.md` with date, decision and any conditions.

| Milestone | Sprints | Epics | Outcome |
|---|---|---|---|
| M0 Foundations | S0 | E0 | Clean repository, pipeline, standards, decisions |
| M1 Data platform | S1-S2 | E1 | Point-in-time data for the pilot universe with a quality report |
| M2 Financial statements | S3-S4 | E2 | Three audited years plus interim periods, reconciled and exportable |
| M3 Fundamentals and peers | S5-S6 | E3, E4 | Metrics, quality scores and justified peer sets |
| M4 Valuation and models | S7-S8 | E5 | Screen, long-term valuation, medium-term signals |
| M5 Agents and evaluation | S9-S11 | E6, E7 | Memos that pass two judges; calibrated rubric; team benchmark |
| M6 Backtest and portfolio | S12-S14 | E8, E9 | Tested strategies and mandate-compliant proposals |
| M7 Execution and operations | S15-S16 | E10, E11, E12 | Paper trading with approvals, reports, dashboard, scheduled runs |
| M8 Paper period and go-live review | 12 weeks | none new | Decision on live trading |

## M0 Foundations

- **You provide:** answers to open questions Q1 to Q10; approval of the decision records.
- **You check:** the pipeline blocks a bad pull request; the decision records match what was agreed; the prototype disposition note.
- **Exit:** all E0 tests pass; decision records accepted; sign-up list for M1 complete.

## M1 Data platform

- **Sign-ups first:** SEC contact email, FRED key.
- **You check:** the `pilot-25` data-quality report (coverage, gaps, cross-source differences); the price-source comparison and recommendation; one company traced from raw payload to stored fact.
- **Demo:** ingest a company you name from scratch; rerun to show no changes; query as of a past date.
- **Exit:** all E1 tests for S1 and S2 pass; coverage thresholds met or exceptions accepted by you; price source decided.

## M2 Financial statements

- **You check:** the reconciliation pack for five companies you choose, against the filings; the Excel workbook; audited and unaudited labels; the exception report.
- **Demo:** statements for a company you name, with click-through from a cell to the filing.
- **Exit:** all E2 tests pass; golden statements match; thresholds in T-E2-14 met; your sign-off on the reconciliation pack.

## M3 Fundamentals and peers

- **Sign-ups first:** embedding provider chosen.
- **You check:** metric definitions in the registry; the fundamental summary for five companies; peer sets for ten companies, with your overrides.
- **Exit:** all E3 and E4 tests pass; golden metrics match; your review recorded.

## M4 Valuation and models

- **Start now:** the IBKR account application, since approval time is not published.
- **You check:** valuations for five companies including assumptions and sensitivities; the screen shortlist and reasons for exclusion; signal charts; the optional-feeds assessment and your go or no-go on paid feeds.
- **Exit:** all E5 tests pass; textbook examples reproduced; reproducibility test passes.

## M5 Agents and evaluation

- **Sign-ups first:** model API account with a spend limit; keys for any other providers.
- **Your time:** grading 15 memos on the rubric (several hours).
- **You check:** the calibration report (agreement with your grades); the judge sensitivity report on the defect library; the saturation test result; the team benchmark report (attempts to pass by team shape, cost per passing memo); three rendered memos with scorecards.
- **Exit:** all E6 and E7 tests for S9 to S11 pass; thresholds in T-E7-04, T-E7-05, T-E7-09 and T-E7-10 met; a default team shape chosen from the benchmark.

## M6 Backtest and portfolio

- **You check:** tearsheets for the core and tactical strategies against the equity benchmark and the 30/70 blend; the small-account analysis; survivorship coverage; the number of variants tried; a proposed portfolio for USD 5,000 with every limit shown.
- **Decision:** whether the strategies justify paper trading, or need rework, or whether an index fund is the better answer for the equity sleeve.
- **Exit:** all E8 and E9 tests pass; your decision recorded.

## M7 Execution and operations

- **Sign-ups first:** IBKR account funded with paper trading enabled and market data as needed; TradingView paid plan with two-factor authentication; webhook endpoint; backup storage.
- **You check:** one paper order from proposal through approval to fill and reconciliation; the dashboard; a weekly report; a TradingView alert arriving as a review task; a restore from backup.
- **Exit:** all E10, E11 and E12 tests pass; the scheduler has run unattended for one week on paper.

## M8 Paper period and go-live review

- **Duration:** 12 weeks of scheduled paper trading.
- **You check each week:** the weekly report, any alerts, reconciliation status.
- **Go-live criteria:** no reconciliation break unresolved; no safety-control breach; every traded memo passed the gate; costs within budget; paper results consistent with the backtest range; your sign-off on the checklist.
- **Outcome:** enable live trading at a reduced size, extend the paper period, or stop.
