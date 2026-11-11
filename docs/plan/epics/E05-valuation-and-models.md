# E5. Valuation and models service

**Goal:** three model layers with versioned, reproducible outputs: a screen that narrows the universe, long-term valuation, and medium-term signals.
**Depends on:** E1, E2, E3, E4.
**Milestone:** M4.

## Features

### Layer 1: screen

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E5-01 | S7 | Eligibility filters | Data-quality pass, minimum market value, minimum traded value, minimum price, in-scope sector. Each exclusion carries a reason. |
| F-E5-02 | S7 | Factor scores | Quality, value and safety factors as sector-neutral percentile ranks, combined with configured weights. |
| F-E5-03 | S7 | Screen output | Ranked shortlist of about 40 names with the factor breakdown per name. |

### Layer 2: long-term valuation

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E5-04 | S7 | Cost of capital | Risk-free rate from the macro store, beta from five-year monthly regression with adjustment and bounds, equity risk premium from dated config, cost of debt, tax rate, market-value weights. Result bounded and flagged when a bound applies. |
| F-E5-05 | S7 | Discounted cash-flow engine | Free cash flow to the firm from driver assumptions over an explicit period, fade to terminal, terminal value by perpetual growth and by exit multiple, mid-year convention, bridge from enterprise to equity value, diluted share count. |
| F-E5-06 | S7 | Scenario engine | Bear, base and bull assumption sets with probabilities and expected value. Each assumption carries a rationale and the figures it rests on. |
| F-E5-07 | S7 | Sensitivity tables | Discount rate against terminal growth, and growth against margin. |
| F-E5-08 | S8 | Reverse discounted cash flow | Solves for the growth or margin implied by the current price. |
| F-E5-09 | S8 | Multiples valuation | Enterprise-value and price multiples against peer median and the company's own five-year history, giving an implied value range. |
| F-E5-10 | S8 | Valuation synthesis | Combined value range, margin of safety against price, verdict thresholds from the mandate config, and a disagreement flag when methods diverge beyond a threshold. |

### Layer 3: medium-term signals

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E5-11 | S8 | Trend and momentum | 200-day trend, twelve-minus-one and six-minus-one month momentum, strength relative to sector. |
| F-E5-12 | S8 | Earnings signals | Standardized unexpected earnings from a seasonal random-walk model, and a post-announcement window dated from the earnings filing's acceptance time. |
| F-E5-13 | S8 | Risk-state filter | Volatility regime, market trend filter, drawdown state. |
| F-E5-14 | S8 | Signal combiner | Entry and exit rules with holding-period bounds of 4 to 26 weeks. Outputs carry as-of timestamps. |

### Shared

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E5-15 | S7 | Model registry | Every model has a version and parameters in config. Outputs store model version and data snapshot id. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E5-01 | U | F-E5-01 | Each filter excludes its engineered case and records the reason. |
| T-E5-02 | U | F-E5-02, F-E5-03 | Ranks are uniform within a sector; composite weights sum to one; shortlist size follows config. |
| T-E5-03 | P | F-E5-02 | Improving one factor input never lowers the composite score. |
| T-E5-04 | U | F-E5-04 | Cost of capital reproduces a hand-worked example; values outside bounds are clipped and flagged. |
| T-E5-05 | U | F-E5-04 | Beta equals a reference regression on fixed data; insufficient history falls back to the sector value with a flag. |
| T-E5-06 | G | F-E5-05 | The engine reproduces a published textbook valuation within 0.1%. |
| T-E5-07 | P | F-E5-05 | Value rises with growth when return exceeds cost of capital, rises with margin, falls with discount rate. Terminal growth at or above the discount rate is rejected. Zero-growth case equals the closed-form perpetuity. |
| T-E5-08 | U | F-E5-05 | Equity value equals enterprise value less net debt and minorities, divided by diluted shares. |
| T-E5-09 | U | F-E5-06 | Scenario probabilities sum to one, values are ordered, expected value is correct, and an assumption without rationale or basis is rejected. |
| T-E5-10 | U | F-E5-08 | The implied growth, fed back into the engine, returns the current price within 0.1%. |
| T-E5-11 | U | F-E5-09 | Negative earnings give a not-applicable multiple, which peer medians exclude. |
| T-E5-12 | U | F-E5-10 | Disagreement flag fires above the threshold; margin of safety and verdict follow the configured rules. |
| T-E5-13 | P | F-E5-11, F-E5-12, F-E5-13, F-E5-14 | Signals at time t are unchanged when any data after t is altered. |
| T-E5-14 | U | F-E5-11 | Twelve-minus-one momentum skips the latest month and equals a reference calculation. |
| T-E5-15 | U | F-E5-12 | The earnings-surprise measure equals the known value on a synthetic series; a filing accepted after the close dates the signal to the next trading day. |
| T-E5-16 | I | F-E5-15 | Rerunning with the same snapshot id gives byte-identical outputs. |
| T-E5-17 | I | F-E5-03, F-E5-10 | Screen and valuation run end to end for `pilot-25`; no value per share is zero or negative without a flag. |
| T-E5-18 | U | F-E5-07 | Sensitivity grid centre equals the base case; rows and columns are monotonic. |
| T-E5-19 | U | F-E5-13, F-E5-14 | Each entry and exit rule triggers on its engineered series; holding-period bounds are enforced. |
| T-E5-20 | M | F-E5-06, F-E5-10 | Investor reviews valuations for five companies, including assumptions and sensitivities. |

## Known limits

- Estimate-revision signals need a paid feed and are not in this epic.
- The valuation engine is for operating companies; it is not applied to excluded sectors.
