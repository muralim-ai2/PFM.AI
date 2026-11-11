# E11. Reporting, dashboard and TradingView

**Goal:** the investor can read every output, see why it was produced, approve orders, and use TradingView for charts and alerts without scraping it.
**Depends on:** E2 to E10 for content. A TradingView paid plan for webhooks.
**Milestone:** M5 (memo and scorecard), M4 (charts), M7 (the rest).

The statements workbook is specified in E2 (F-E2-12).

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E11-01 | S11 | Stock memo renderer | HTML and PDF containing statements, analysis, peers, valuation, scenarios, risks, evaluation scorecard and lineage links. Numbers rendered from figure ids. |
| F-E11-02 | S11 | Evaluation scorecard view | Dimensions and sub-dimensions with both judges' scores, evidence and attempt history. |
| F-E11-03 | S8 | Charts from own data | Price with indicators, signal markers and valuation bands, drawn from stored data. |
| F-E11-04 | S16 | Weekly portfolio report | Holdings, performance against benchmarks, allocation drift, risk, upcoming events, proposals. |
| F-E11-05 | S16 | Dashboard | Local web app: data-quality status, company page, shortlist, portfolio, approvals queue, runs and costs. |
| F-E11-06 | S16 | TradingView export | Watchlist import file, and a Pine script that draws the system's levels and signals from pasted inputs. |
| F-E11-07 | S16 | TradingView alert receiver | Authenticated webhook endpoint. An alert creates a review task. There is no code path from an alert to an order. |
| F-E11-08 | S16 | Notifications | Email or push for approvals waiting, reconciliation breaks and thesis-breaker alerts, rate-limited. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E11-01 | U | F-E11-01 | All figure placeholders resolve; no number appears without a figure id; output matches a stored snapshot. |
| T-E11-02 | U | F-E11-01 | Rendered memo shows audited and unaudited labels and the as-of date. |
| T-E11-03 | U | F-E11-02 | Scorecard totals equal the score store for the same memo and attempt. |
| T-E11-04 | U | F-E11-04 | Performance figures equal the backtest metric functions run on the same ledger data. |
| T-E11-05 | E2E | F-E11-05 | Dashboard pages load, and an approval click creates an approval record. |
| T-E11-06 | U | F-E11-06 | The watchlist file is in the documented format; the generated Pine script contains the expected levels and declares its version. |
| T-E11-07 | U | F-E11-07 | A request without the secret is refused. A valid request creates a task. Static analysis shows the receiver imports nothing from execution. |
| T-E11-08 | U | F-E11-08 | Each engineered event sends one notification; repeated events inside the window are suppressed. |
| T-E11-09 | U | F-E11-03 | Chart data equals the stored series; signal markers fall on the signal dates. |
| T-E11-10 | M | F-E11-01, F-E11-04, F-E11-05 | Investor reviews a memo, a weekly report and the dashboard. |

## Known limits

- TradingView has no public data API for this use. Integration is one-way export plus inbound alerts.
- The webhook receiver needs a public HTTPS endpoint; the hosting choice is part of the runtime decision in E12.
