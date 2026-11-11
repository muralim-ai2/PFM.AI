# E8. Backtesting and benchmarking

**Goal:** an honest test of the screen, valuation and signal layers on point-in-time data, with cash-account rules and real costs at the actual account size, compared against simple benchmarks.
**Depends on:** E1 (point-in-time data, benchmarks), E5 (models).
**Milestone:** M6.

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E8-01 | S12 | Daily event-driven engine | Decisions at the close of day t use `as_of(t)`. Fills at the next session at a configured price. |
| F-E8-02 | S12 | Point-in-time inputs | Fundamentals available only after filing acceptance plus a configured lag. Universe membership by date. Delistings handled by a stated policy. |
| F-E8-03 | S12 | Cash-account rules | Next-day settlement, no margin, no shorting, fractional-share policy, minimum order size. |
| F-E8-04 | S12 | Cost model | Broker commission schedule from dated config, spread and slippage by traded value, dividends credited. |
| F-E8-05 | S12 | Shared strategy interface | The strategy and portfolio code used in backtests is the code used in paper and live trading. |
| F-E8-06 | S12 | Benchmarks | Equity benchmark total return, the 30/70 blend, and an equal-weight universe portfolio. |
| F-E8-07 | S12 | Metrics and tearsheet | Annualized return, volatility, Sharpe, Sortino, maximum drawdown, Calmar, turnover, hit rate, exposure, average holding period, and a by-year table, each against benchmarks. |
| F-E8-08 | S13 | Validation methods | Walk-forward evaluation, purged and embargoed cross-validation for any fitted parameter, parameter-sensitivity maps, deflated Sharpe ratio, and a log of how many variants were tried. |
| F-E8-09 | S13 | Bias detectors | Look-ahead canary, survivorship coverage report, and trial counter shown on every tearsheet. |
| F-E8-10 | S13 | Small-account analysis | Results at USD 5,000 with real costs beside frictionless results, and the cost level at which the edge disappears. |
| F-E8-11 | S12 | Run manifest | Code revision, config, data snapshot id and seed stored per run. Reruns are identical. |
| F-E8-12 | S13 | Strategy rubric scoring | The backtest-validity dimension of the rubric scored by the deterministic judge from the run manifest and detectors. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E8-01 | G | F-E8-01, F-E8-06 | Buy-and-hold of the equity benchmark reproduces its total return within 5 basis points a year. |
| T-E8-02 | U | F-E8-01, F-E8-04 | Each day, equity equals cash plus positions, and the change in equity equals profit and loss less costs plus dividends. |
| T-E8-03 | P | F-E8-03 | For generated strategies, settled cash is never negative and no position is ever short. |
| T-E8-04 | U | F-E8-03 | Sale proceeds cannot fund a purchase before settlement. |
| T-E8-05 | EV | F-E8-09 | A strategy that reads the next day's return is flagged by the look-ahead detector; a clean strategy is not. |
| T-E8-06 | U | F-E8-02 | Fundamentals used on day t have knowledge time no later than t minus the lag. |
| T-E8-07 | U | F-E8-04 | A hand-calculated trade, including commission minimum and slippage, matches the engine. |
| T-E8-08 | U | F-E8-02 | A delisted holding is closed by the stated policy and listed in the report. |
| T-E8-09 | U | F-E8-07 | Every metric equals a reference library's value on a fixed return series. |
| T-E8-10 | U | F-E8-08 | Walk-forward folds do not overlap, and purge and embargo windows have the configured sizes. |
| T-E8-11 | U | F-E8-08 | Deflated Sharpe ratio equals a reference implementation on known inputs. |
| T-E8-12 | I | F-E8-11 | The same manifest yields an identical equity-curve hash. |
| T-E8-13 | I | F-E8-05 | One strategy object runs unchanged in the backtest engine and against the simulated broker. |
| T-E8-14 | U | F-E8-10 | At zero cost the small-account result equals the frictionless result; the break-even cost is found by search and verified by rerun. |
| T-E8-15 | U | F-E8-12 | A manifest with look-ahead flagged or no out-of-sample period scores zero on the corresponding sub-dimension. |
| T-E8-16 | U | F-E8-09 | The tearsheet shows the share of the universe with delisting data and the number of variants tried. |
| T-E8-17 | M | F-E8-07, F-E8-10 | Investor reviews tearsheets for the core and tactical strategies against benchmarks, including the small-account analysis. |

## Known limits

- Without a paid survivorship-free price source, results overstate returns. The tearsheet states the coverage.
- Fundamental history through the SEC's structured data begins around 2009, which bounds the test period.
- A passing backtest is evidence about the past, not a forecast.
