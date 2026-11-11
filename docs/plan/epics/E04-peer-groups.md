# E4. Peer group service

**Goal:** a justified, reproducible peer set of five to ten companies for any company in scope, with relative statistics.
**Depends on:** E1 (filing text, universe), E3 (metrics). An embedding provider for business similarity.
**Milestone:** M3.

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E4-01 | S6 | Industry candidates | Candidates by four-digit industry code, widening to three and two digits until at least 15 are found. The level used is recorded. |
| F-E4-02 | S6 | Size filter | Revenue and market value within a configured band of the subject. Any widening of the band is logged. |
| F-E4-03 | S6 | Business similarity | Embedding of the business-description section; cosine ranking. Model and version recorded. |
| F-E4-04 | S6 | Selection | Composite ranking selects five to ten peers with deterministic tie-breaks. Fewer than five returns an explicit insufficient-peers result. |
| F-E4-05 | S6 | Analyst override | Peers can be added or removed with a reason. Overrides persist and are marked in outputs. |
| F-E4-06 | S6 | Peer statistics | Median, quartiles, percentile rank and z-score for valuation, growth, profitability and leverage metrics, with a stated winsorization rule and the count behind each statistic. |
| F-E4-07 | S6 | Relative valuation table | Premium or discount to peer median, and percentile against the company's own five-year history. |
| F-E4-08 | S6 | Versioning | Peer sets are dated. Changes are logged. A past peer set can be reproduced. |
| F-E4-09 | S6 | Justification record | For each peer: industry match level, size ratio and similarity score, in a form the memo can cite. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E4-01 | G | F-E4-01, F-E4-03, F-E4-04 | Each pair in the known-peers dataset appears in the other's top ten within the universe. |
| T-E4-02 | U | F-E4-04 | The subject is never in its own peer set, there are no duplicates, and the count is five to ten or the insufficient-peers result is returned. |
| T-E4-03 | U | F-E4-02 | Selected peers respect the size band; a widened band is logged with the reason. |
| T-E4-04 | U | F-E4-04 | Identical inputs give an identical peer set in identical order. |
| T-E4-05 | U | F-E4-05 | An override survives recomputation and is flagged in the output. |
| T-E4-06 | U | F-E4-06 | Percentile rank is correct with ties and small samples; winsorization is applied before z-scores. |
| T-E4-07 | U | F-E4-06, F-E4-07 | A peer missing a metric is excluded from that statistic and the count shown reflects it. |
| T-E4-08 | I | F-E4-08 | A peer set as of a past date uses only data known then. |
| T-E4-09 | U | F-E4-03 | When the embedding provider fails, selection falls back to industry and size and flags the fallback. |
| T-E4-10 | U | F-E4-09 | Every selected peer has a justification record with all three fields populated. |
| T-E4-11 | M | F-E4-04, F-E4-05 | Investor reviews peer sets for ten companies and records any overrides. |

## Known limits

- Industry codes from filings are coarse. Peer quality depends on text similarity and on the size of the universe.
- Private and foreign competitors are not candidates.
