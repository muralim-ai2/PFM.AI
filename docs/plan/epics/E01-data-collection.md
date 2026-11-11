# E1. Data collection

**Goal:** a point-in-time store of filings, facts, filing text, prices, corporate actions and macro data for the universe, with measured quality.
**Depends on:** E0. SEC contact email, FRED key, price-source decision (ADR-006).
**Milestone:** M1.

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E1-01 | S1 | Security master | Company record with CIK, name, SIC code, fiscal year-end month, status. Ticker history with valid-from and valid-to. Ticker resolves to exactly one CIK for any date. |
| F-E1-02 | S1 | Universe management | Named universes (`pilot-25`, `core-150`, `sp500`) with dated membership. Exclusion flags for financial-sector SIC codes and foreign filers. Source of each membership list recorded. |
| F-E1-03 | S1 | Filing index ingest | From the EDGAR submissions API: accession, form, period of report, acceptance timestamp, primary document. Forms 10-K, 10-Q, their amendments, and 8-K items 2.02 and 4.02. Amendments linked to originals. Incremental after first load. |
| F-E1-04 | S1 | XBRL fact ingest | From the companyfacts API: every fact with start, end, unit, accession, form, fiscal year and period. `us-gaap` and `dei` taxonomies. Raw payload archived unchanged with a content hash. |
| F-E1-05 | S2 | Filing text sections | Primary documents downloaded. Business, risk factors, management discussion and notes extracted as text with section boundaries. Missing sections reported, never guessed. |
| F-E1-06 | S2 | Daily prices | Provider protocol with a primary and a fallback adapter. Open, high, low, close, volume, unadjusted, stored in Parquet. Fifteen years of history where available. Delisted names included if the provider supplies them. |
| F-E1-07 | S2 | Corporate actions | Splits, cash dividends with ex-date, symbol changes. Adjustment factors and a total-return series derived and stored. |
| F-E1-08 | S2 | Macro and rates | FRED series for risk-free rates, inflation, credit spread, unemployment. Observation date and vintage kept for revised series. |
| F-E1-09 | S2 | Benchmarks | Total-return series for the equity benchmark, a bond proxy, and the 30/70 blend. |
| F-E1-10 | S1 | Point-in-time store | Every record has `knowledge_time` and `ingested_at`. `as_of(t)` is the only read path for analysis and backtests. Filings become knowable on the next trading day after acceptance if accepted after the close. |
| F-E1-11 | S2 | Data-quality framework | Declarative checks: completeness, freshness, range, uniqueness, referential integrity, cross-source reconciliation. Results stored with severity. A critical failure blocks that company downstream. |
| F-E1-12 | S1 | Incremental, idempotent, compliant jobs | Re-running any ingest produces no changes. Jobs resume after interruption. SEC requests carry the declared User-Agent and stay under the published rate limit. |
| F-E1-13 | S2 | Debenture sleeve input | Validated CSV of fixed-income holdings: issuer, face value, coupon, maturity, market value, as-of date. Feeds total portfolio value and the 30/70 calculation. |
| F-E1-14 | S2 | Data snapshots | An immutable snapshot id freezes a consistent view of all stores for reproducible runs. |
| F-E1-15 | S8 | Optional feeds decision | Written assessment of estimates, transcripts and news feeds: what each would add, cost, licence. Go or no-go recorded at M4. No implementation in this plan unless approved. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E1-01 | C | F-E1-03 | Recorded submissions responses for three companies parse into filing rows whose count and fields match the fixture. |
| T-E1-02 | U | F-E1-01 | A company that changed ticker resolves by date to the same CIK under the old and new symbol. |
| T-E1-03 | I | F-E1-03, F-E1-12 | Second ingest run inserts zero rows. Adding one new filing to the fixture inserts only that filing. |
| T-E1-04 | U | F-E1-03 | An amended annual report is linked to the original for the same period. |
| T-E1-05 | C | F-E1-04 | Recorded companyfacts response: row count equals the number of fact entries in the payload; all units retained. |
| T-E1-06 | U | F-E1-04 | Stored payload hash matches on re-read. A modified payload is detected. |
| T-E1-07 | U | F-E1-05 | Section extractor finds the three target sections in five fixture filings of different years and layouts, and returns an explicit not-found result on a filing without them. |
| T-E1-08 | G | F-E1-07 | Around a known stock split the adjusted series is continuous, and the adjustment factor equals the split ratio. |
| T-E1-09 | G | F-E1-07, F-E1-09 | Computed calendar-year total return of the equity benchmark matches the fund's published figure within 10 basis points. |
| T-E1-10 | DQ | F-E1-06, F-E1-11 | Gaps longer than five trading days, non-positive prices, and primary-versus-fallback close differences above 0.5% are flagged. |
| T-E1-11 | P | F-E1-10 | For generated dates, `as_of(d)` never returns a row with `knowledge_time` later than `d`. |
| T-E1-12 | I | F-E1-10 | A fact from a filing accepted after the close on day D is invisible as of D and visible on the next trading day. |
| T-E1-13 | I | F-E1-12 | A simulated run of 1,000 SEC requests never exceeds the rate limit, and every request carries the User-Agent. |
| T-E1-14 | I | F-E1-12 | Ingest interrupted midway and restarted completes with no duplicates and no missing rows. |
| T-E1-15 | DQ | F-E1-02, F-E1-11 | For `pilot-25`: at least 99% of companies have three fiscal years of facts and ten years of prices. Exceptions are listed by company and cause. |
| T-E1-16 | U | F-E1-08 | FRED parser handles missing-value markers and keeps the vintage date. |
| T-E1-17 | U | F-E1-13 | Invalid debenture rows are rejected with line-numbered messages. Valid file yields total value and equity share. |
| T-E1-18 | U | F-E1-14 | Writing to a closed snapshot fails. Reading the same snapshot twice returns identical data. |
| T-E1-19 | U | F-E1-02 | A financial-sector company and a foreign filer are flagged out of scope with the reason. |
| T-E1-20 | C | F-E1-06 | Both price adapters pass the shared provider contract suite on recorded responses. |
| T-E1-21 | M | F-E1-11, F-E1-15 | Investor reviews the `pilot-25` data-quality report at M1 and the optional-feeds assessment at M4. |

## Known limits

- Free price sources rarely include delisted companies. Until a paid source is approved, backtests carry survivorship bias and say so.
- Custom company-specific XBRL tags are not in the companyfacts API. They are handled in E2 through per-filing data where material.
