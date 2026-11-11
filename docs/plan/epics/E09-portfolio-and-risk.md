# E9. Portfolio construction and risk

**Goal:** turn approved memos and signals into order proposals that always sit inside the mandate, with an internal ledger and monitors for allocation and risk.
**Depends on:** E5 (models), E7 (gate), E8 (shared strategy interface).
**Milestone:** M6.

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E9-01 | S13 | Mandate configuration | Total portfolio, equity target with band, core and tactical sleeve split, position and sector caps, maximum names, minimum position value, and prohibitions on margin, shorting and derivatives. |
| F-E9-02 | S13 | Core construction | Selects from the shortlist names whose margin of safety meets the threshold. Capped equal weight or inverse volatility. Sector caps and a turnover budget. |
| F-E9-03 | S13 | Tactical construction | Sizes medium-term entries to a volatility target within caps. Holds cash when no signal qualifies. |
| F-E9-04 | S13 | Exit rules | Thesis-breaker hit, price above value range, trend break or stop for tactical positions, time stop. |
| F-E9-05 | S14 | Pre-trade checks | Limits, settled cash, share of traded volume, duplicate order, price collar, restricted list. Each block carries a reason code. |
| F-E9-06 | S14 | Risk monitor | Drawdown circuit breaker that blocks new buys, concentration, beta, correlation clusters, historical value-at-risk as information. |
| F-E9-07 | S14 | Allocation monitor | Equity share against the debenture sleeve, with a rebalance proposal when outside the band. |
| F-E9-08 | S14 | Order proposal generator | Target against current holdings gives orders with rationale and links to memo and evaluation score. Only memos that passed the gate can produce a buy. |
| F-E9-09 | S14 | Ledger | Positions, settled and unsettled cash, tax lots, realized and unrealized profit and loss, wash-sale flag as information. |
| F-E9-10 | S14 | What-if view | Portfolio before and after a set of proposed orders, with every limit shown. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E9-01 | P | F-E9-01, F-E9-02, F-E9-03 | For generated shortlists and prices, no position exceeds its cap, no sector exceeds its cap, weights are non-negative and sum to at most 100%. |
| T-E9-02 | U | F-E9-02 | Constraints that cannot all be met produce an infeasibility report; none is silently relaxed. |
| T-E9-03 | U | F-E9-01, F-E9-02 | USD 5,000 across eight names respects the minimum position value and leaves non-negative cash under the fractional-share policy. |
| T-E9-04 | U | F-E9-04 | Each exit rule produces a sell proposal with its reason on an engineered scenario. |
| T-E9-05 | U | F-E9-05 | Each pre-trade check blocks its engineered violation with the right reason code and passes a clean order. |
| T-E9-06 | U | F-E9-06 | At a 15% sleeve drawdown new buys are blocked and sells are allowed. |
| T-E9-07 | U | F-E9-07 | An allocation of 36/64 yields a proposal that returns it to the band. |
| T-E9-08 | U | F-E9-08 | A memo without a passing evaluation cannot generate a buy proposal. |
| T-E9-09 | P | F-E9-09 | For generated sequences of fills, cash plus positions stay consistent and lot accounting follows the stated method. |
| T-E9-10 | U | F-E9-09 | A sale at a loss followed by a repurchase within 30 days is flagged. |
| T-E9-11 | I | F-E9-08, F-E9-10 | Proposals applied in the what-if view reconcile to the target portfolio totals. |
| T-E9-12 | U | F-E9-03 | With no qualifying signal the tactical sleeve is entirely cash. |
| T-E9-13 | U | F-E9-06 | Concentration, beta and value-at-risk equal reference calculations on a fixed portfolio. |

## Known limits

- With USD 5,000 the number of positions is limited by minimum order economics; the small-account analysis in E8 informs the configured maximum.
- Tax handling is informational only.
