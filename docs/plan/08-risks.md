# 8. Risk register

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | The strategies do not beat an index fund after costs at USD 5,000 | High | High | Small-account analysis and benchmark comparison at M6, with an explicit decision point | Investor |
| R2 | Survivorship bias inflates backtests because free price data lacks delisted companies | High | High | Coverage reported on every tearsheet; paid source assessed at M1; results labelled | Build |
| R3 | Statement mapping errors on companies with unusual tagging | High | High | Golden statements, integrity checks, unmapped-tag report, reconciliation pack, investor sign-off | Build |
| R4 | LLM judge scores drift upward or miss defects | Medium | High | Deterministic judge must concur; mutation testing; saturation test; calibration; drift monitoring | Build |
| R5 | A fabricated or wrong number reaches a memo | Medium | High | Numbers only from tools; figure-id rendering; deterministic recomputation; critical sub-dimension | Build |
| R6 | Look-ahead in models or backtests | Medium | High | Single `as_of` read path; perturbation tests; canary strategy | Build |
| R7 | Model costs exceed budget, especially in benchmarks | Medium | Medium | Per-run caps, cost ledger, budget alerts, benchmark sized to budget | Investor and build |
| R8 | An order is sent in error | Low | High | Approval hash, live flag, account guard, daily caps, reconciliation halt, paper period | Build |
| R9 | Vendor terms or interfaces change (SEC, broker, price source, model provider) | Medium | Medium | Adapters behind protocols; nightly contract tests; no scraping | Build |
| R10 | Brokerage account approval or data subscription delays M7 | Medium | Medium | Start the application at M4; simulated broker keeps E10 work unblocked | Investor |
| R11 | Small open models fail structured output or tool use | Medium | Medium | Repair retries; benchmark measures failure rate; hybrid team shape | Build |
| R12 | Overfitting from trying many strategy variants | Medium | High | Trial counter, deflated Sharpe ratio, walk-forward, parameters fixed before the out-of-sample period | Build |
| R13 | The host machine is unavailable when jobs are due | Medium | Low | Catch-up scheduler, freshness alerts, runtime decision at M0 | Investor |
| R14 | Investor review time becomes the bottleneck | Medium | Medium | Evidence packs sized for review; milestone gates keep rework small | Investor |
| R15 | Scope growth (estimates, news, more asset types) delays core delivery | Medium | Medium | Deferred items listed; changes go through a decision record | Investor |
| R16 | Securities rules or tax consequences are overlooked | Low | Medium | System is for the investor's own account only; tax flags informational; professional advice is outside this plan | Investor |
