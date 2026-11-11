# E2. Financial statements service

**Goal:** income statement, balance sheet and cash-flow statement for the last three audited fiscal years and every unaudited interim period since, standardized across companies, reconciled, and traceable to the filing.
**Depends on:** E1.
**Milestone:** M2.

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E2-01 | S3 | Standard chart of accounts | Versioned list of standard line items for the three statements for commercial and industrial companies, with definitions, sign convention and subtotals. |
| F-E2-02 | S3 | Tag mapping engine | Versioned rules from XBRL tag to standard line with priority, sign and aggregation. Company-level overrides. Any unmapped tag above 1% of revenue or total assets is reported. |
| F-E2-03 | S4 | Assisted mapping for custom tags | A model proposes a mapping for an unmapped tag with its reasoning. The proposal is inactive until an approval record exists. Reported values are never changed by this path. |
| F-E2-04 | S3 | Fiscal calendar | Fiscal year-end month, 52/53-week years, quarter assignment, and fiscal-year changes handled. |
| F-E2-05 | S3 | Period engine | Duration facts classified as quarter, half-year, nine-month or full-year. Standalone quarters derived from year-to-date figures for the income and cash-flow statements, including the fourth quarter. Derived values flagged. |
| F-E2-06 | S3 | Audit status labelling | Annual figures from the annual report labelled audited. Interim figures labelled unaudited. A derived fourth quarter labelled as derived from audited full-year less unaudited nine-month figures. |
| F-E2-07 | S4 | Restatements | First-reported and latest-restated values both kept. Restatement size computed. Non-reliance notices flagged on the company. |
| F-E2-08 | S4 | Statement assembly | Three fiscal years, all interim quarters since the last year-end with prior-year comparatives, trailing twelve months, per-share data, and common-size views. |
| F-E2-09 | S3 | Integrity checks | Balance-sheet equation, cash-flow reconciliation to change in cash, income-statement subtotals, net income equal across statements, closing cash equal across statements, sum of quarters equal to the year, share-count sanity. Each has a tolerance and a severity. |
| F-E2-10 | S4 | Lineage | Every cell links to accession number, tag, context and filing date, with a URL to the filing. |
| F-E2-11 | S3 | Unit and split normalization | Scale and currency normalized (USD only). Per-share values stored raw and split-adjusted. |
| F-E2-12 | S4 | Export | Excel workbook with annual and interim sheets for each statement, audited and unaudited labels, a checks sheet and a lineage sheet. Same content available as JSON. |
| F-E2-13 | S4 | Coverage and exception report | Per company: share of standard lines populated, checks passed and failed, unmapped material tags, restatements. |
| F-E2-14 | S4 | Reconciliation pack | For selected companies, a side-by-side of system values against as-filed values for key lines, ready for sign-off. |
| F-E2-15 | S3 | Out-of-scope handling | Financial-sector and foreign filers return an explicit out-of-scope result. No partial statements are produced. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E2-01 | G | F-E2-01, F-E2-02, F-E2-08 | Ten golden companies with varied fiscal year-ends: 20 key lines for three fiscal years equal values hand-keyed from the annual reports. |
| T-E2-02 | G | F-E2-05, F-E2-08 | Same companies: key lines for the latest three reported quarters equal values hand-keyed from the quarterly reports. |
| T-E2-03 | U | F-E2-05, F-E2-06 | Fourth quarter equals full year minus nine months, is flagged derived, and is not labelled audited. |
| T-E2-04 | U | F-E2-05 | Cash-flow quarters equal differences of consecutive year-to-date figures; the first quarter equals its year-to-date figure. |
| T-E2-05 | U | F-E2-04 | A 53-week year is classified as a full year. Quarters are assigned correctly for a January fiscal year-end. |
| T-E2-06 | U | F-E2-02 | Preferred tag wins when present, fallback is used when absent, and the sign rule is applied. |
| T-E2-07 | U | F-E2-02, F-E2-13 | An unmapped tag above the materiality threshold appears in the exception report. |
| T-E2-08 | I | F-E2-07 | A fixture with a revised prior-year figure stores both versions, leaves the first-reported view unchanged, and reports the restatement size. |
| T-E2-09 | P | F-E2-09 | Generated consistent statements pass all checks. Changing any single line beyond tolerance fails exactly the checks that depend on it. |
| T-E2-10 | U | F-E2-09 | Sum of four quarters equals the fiscal year within tolerance for every flow line. |
| T-E2-11 | U | F-E2-10 | Every exported cell has an accession number and tag, and its URL has the expected form. |
| T-E2-12 | U | F-E2-11 | After a stock split, historical per-share values are adjusted and raw values are retained. |
| T-E2-13 | I | F-E2-12 | The workbook opens, has the expected sheets, typed numeric cells, audit labels on every period column, and a checks sheet listing every check. |
| T-E2-14 | DQ | F-E2-09, F-E2-13 | For `pilot-25`: at least 95% of standard lines populated, 100% of periods pass the balance-sheet equation, at least 98% pass cash-flow reconciliation. Each failure is listed with its cause. |
| T-E2-15 | U | F-E2-03 | A mapping proposal without an approval record has no effect. Reported values are byte-identical before and after a mapping is activated. |
| T-E2-16 | U | F-E2-15 | A bank returns the out-of-scope result with a reason and no statement rows. |
| T-E2-17 | I | F-E2-07, F-E2-08 | Statements as of a date before a restatement return the originally reported values. |
| T-E2-18 | U | F-E2-08 | Trailing twelve months equals the sum of the last four quarters for flow lines and the latest value for balance lines. |
| T-E2-19 | U | F-E2-14 | Reconciliation pack lists each key line with system value, filed value and difference, and totals the mismatches. |
| T-E2-20 | M | F-E2-12, F-E2-14 | Investor checks the reconciliation pack and workbook for five companies against the filings and signs off. |

## Known limits

- Banks, insurers, REITs and foreign filers are excluded in v1.
- Segment data and footnote detail are not standardized in v1.
- Non-GAAP figures from earnings releases are not included.
