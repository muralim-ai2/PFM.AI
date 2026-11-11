# E3. Fundamental analysis service

**Goal:** a complete, versioned set of fundamental metrics and quality scores computed from the standardized statements, each with a documented formula and hand-verified reference values.
**Depends on:** E2.
**Milestone:** M3.

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E3-01 | S5 | Metric registry | Each metric has id, formula, inputs, unit, period basis (annual, quarterly, trailing), version and null policy. Metrics are computed only through the registry. |
| F-E3-02 | S5 | Growth | Year-on-year, same-quarter prior-year, three-year compound and trailing growth for revenue, operating profit, net income, earnings per share and free cash flow. |
| F-E3-03 | S5 | Margins | Gross, operating, EBITDA, net and free-cash-flow margins, plus incremental margins. |
| F-E3-04 | S5 | Returns | Return on invested capital with a written definition of invested capital, return on equity, on assets, on capital employed. DuPont three-step and five-step breakdowns. |
| F-E3-05 | S5 | Efficiency | Days sales, inventory and payables outstanding, cash conversion cycle, asset turnover, capex to sales, capex to depreciation. |
| F-E3-06 | S5 | Leverage and liquidity | Net debt, net debt to EBITDA, interest cover, current and quick ratios, Altman Z-score with the variant chosen by industry. |
| F-E3-07 | S5 | Cash-flow quality | Free cash flow, cash conversion, operating cash flow to net income, stock-based compensation share, working-capital contribution. |
| F-E3-08 | S6 | Earnings-quality scores | Accruals ratio, Piotroski F-score with all nine signals itemized, Beneish M-score with all eight variables itemized. |
| F-E3-09 | S6 | Capital allocation | Buybacks, dividends, payout ratio, net change in share count, acquisition spend, reinvestment rate. |
| F-E3-10 | S6 | Trend and stability | Three-year slopes, margin volatility, and flags for deteriorating margins or rising leverage. |
| F-E3-11 | S5 | Fundamental summary object | One typed object per company and date holding all metrics with data-quality caveats, consumed by peers, models and agents. |
| F-E3-12 | S6 | Red-flag rules | Declarative rules such as receivables growing much faster than revenue. Each firing cites the figures behind it. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E3-01 | G | F-E3-02, F-E3-03, F-E3-04, F-E3-05, F-E3-06, F-E3-07, F-E3-09 | Every metric for three golden companies over three years equals the hand-calculated spreadsheet value to a relative tolerance of 1e-6. |
| T-E3-02 | P | F-E3-04 | The product of DuPont components equals return on equity for generated inputs. |
| T-E3-03 | U | F-E3-01 | Zero or negative denominators yield null with a reason code, never infinity or not-a-number. |
| T-E3-04 | U | F-E3-02 | Trailing figures equal the sum of the last four quarters, including a derived fourth quarter. |
| T-E3-05 | U | F-E3-08 | A synthetic company built to score nine and one built to score zero do so; flipping one signal changes the score by exactly one. |
| T-E3-06 | U | F-E3-08 | The Beneish calculation reproduces a published worked example within tolerance. |
| T-E3-07 | U | F-E3-06 | The Altman calculation reproduces a textbook example, and the variant follows the industry code. |
| T-E3-08 | U | F-E3-04 | Invested capital follows the written definition on an engineered balance sheet, including the treatment of excess cash. |
| T-E3-09 | U | F-E3-01 | Changing a formula without raising its version fails a registry consistency test. |
| T-E3-10 | P | F-E3-01, F-E3-03 | Multiplying every statement value by a constant leaves all ratios unchanged. |
| T-E3-11 | U | F-E3-12 | Each red-flag rule fires on its engineered fixture, cites figure ids, and stays silent on a clean fixture. |
| T-E3-12 | I | F-E3-11 | Metrics as of a past date use only filings known on that date. |
| T-E3-13 | DQ | F-E3-11 | For `pilot-25`, metric coverage is at least 95%. Values more than five standard deviations from a company's own history are listed for review. |
| T-E3-14 | U | F-E3-10 | Slope and volatility match a reference calculation; flags fire at the configured thresholds. |
| T-E3-15 | M | F-E3-11 | Investor reviews the fundamental summary for five companies against their own reading of the filings. |

## Known limits

- Metrics that need segment or footnote data (for example debt maturity ladders) are included only where tagged in the main statements.
