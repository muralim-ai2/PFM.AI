# 1. Scope, mandate and decisions

## 1.1 Product statement

A personal fund-management system for one investor. It collects filings and market data, rebuilds
financial statements, analyses fundamentals and peers, values companies, proposes a portfolio that
fits a fixed mandate, and places approved orders at Interactive Brokers. Every investment memo is
scored by two independent judges before it can drive a trade.

## 1.2 Mandate (as understood; confirm in M0)

| Item | Value | Status |
|---|---|---|
| Risk profile | Risk-averse | stated |
| Asset split | 30% equities, 70% debentures | stated |
| Equity sleeve | USD 5,000 at start (implies about USD 16,700 total) | stated, total inferred |
| Debenture sleeve | Held outside the system; tracked for the 30/70 check only | assumed |
| Account | Cash account, no margin, no shorting, no derivatives | stated (no margin); rest assumed |
| Horizons | Long term (1-5 years) core; medium term (1-6 months) tactical | stated |
| Instruments | US-listed common stock; ETFs for benchmarks only | assumed |
| Control | Human approves every order; paper trading before live | assumed |
| Broker and tools | Interactive Brokers, TradingView, Python, a database | stated |

## 1.3 In scope

1. Data collection: filings, XBRL facts, filing text, prices, corporate actions, macro, benchmarks.
2. Financial statements service: 3 audited fiscal years plus unaudited interim periods, standardized, reconciled, traceable.
3. Fundamental analysis service.
4. Peer group service.
5. Valuation and models service in layers: screen, long-term valuation, medium-term signals.
6. Agent teams that write investment memos, in selectable shapes (few frontier agents, or many small agents led by a frontier model).
7. Evaluation: two-level rubric, deterministic judge and LLM judge that must concur, reflection, team benchmark.
8. Backtesting and benchmarking on point-in-time data.
9. Portfolio construction and risk controls for the mandate.
10. Execution through IBKR with an approval workflow.
11. Reports, dashboard, TradingView integration.
12. Operations: scheduling, backups, monitoring, cost tracking.

## 1.4 Out of scope for v1

- Banks, insurers and REITs (different statement structure). Flagged and excluded, not half-supported.
- Foreign private issuers filing 20-F/40-F, and IFRS reporters.
- Intraday trading, Level 2 order-book data, options, shorting, margin.
- Scraping or screenshotting TradingView, broker screens or paywalled research sites.
- Automated trading without human approval.
- Tax filing output. Wash-sale flags are informational only.

## 1.5 Status of the code on `main`

`main` holds a prototype built in one pass and tested only on synthetic data. It is treated as a
throwaway spike. Sprint 0 tags it `spike-v0` and starts a clean layout. Nothing is carried over
unless it meets the standards in `03-engineering-standards.md` and has tests from this plan.

## 1.6 Open questions (answers needed at M0)

| # | Question | Why it matters | Default if unanswered |
|---|---|---|---|
| Q1 | Where does the system run: your laptop, a home server, or a small cloud VM? | IB Gateway must run next to it; scheduler and backups depend on it | Laptop for build, cloud VM from M7 |
| Q2 | US common stocks only, or ETFs as holdings too? | Universe, screen, valuation applicability | Stocks only |
| Q3 | Universe size for v1 | Data volume, LLM cost, run time | Pilot 25, then 150, then S&P 500 |
| Q4 | Taxable account or tax-advantaged? | Turnover budget, wash-sale handling, lot selection | Taxable, informational flags only |
| Q5 | Monthly budget for paid data | Survivorship-free prices and estimates cost money | USD 0-30 |
| Q6 | Monthly budget and providers for LLM calls | Team shapes, benchmark size, judge model family | Anthropic only, cap set at M5 |
| Q7 | How are debentures tracked: manual CSV, or do they sit at IBKR? | Allocation monitor design | Manual CSV |
| Q8 | Approval channel: command line, dashboard, phone notification | Execution workflow, hosting | Dashboard plus email |
| Q9 | Which model is "Astra", and which provider serves it? | Provider adapter work | Not included until identified |
| Q10 | Are estimates, transcripts and news needed in v1? | Paid feeds; medium-term signals improve with revisions data | Deferred; decision at M4 |

## 1.7 Architecture decision records to ratify in Sprint 0

| ADR | Decision | Proposed | Alternatives recorded |
|---|---|---|---|
| ADR-001 | Storage | SQLite for records, Parquet with DuckDB for prices and backtests | Postgres; FalkorDB for relationship queries (deferred) |
| ADR-002 | Time model | Bitemporal: every record has knowledge time and ingest time; all reads go through `as_of` | Latest-only tables |
| ADR-003 | Numbers | All numbers computed by code. LLMs never produce or alter a number | LLM arithmetic |
| ADR-004 | Memo acceptance | Deterministic judge and LLM judge must both pass; final score is the lower | LLM judge only |
| ADR-005 | Providers | Protocol interfaces for data, LLM and broker; adapters per vendor | Direct SDK calls in services |
| ADR-006 | Price source | Decided after M1 spike: IBKR historical, with one fallback | Single free source |
| ADR-007 | Agent orchestration | Own thin orchestrator over the provider protocol | Agent framework dependency |
| ADR-008 | Scheduling | Decided with Q1 | cron, APScheduler, hosted workflow |
| ADR-009 | Money and precision | `Decimal` for reported values and ledger; float only for ratios and statistics | Float everywhere |
