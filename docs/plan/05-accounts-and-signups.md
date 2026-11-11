# 5. Accounts, keys and subscriptions

What must exist before each milestone can start. Prices and terms were checked on 2026-11-10 from the
vendor pages linked below. Items marked (unverified) could not be confirmed from an official page and
must be confirmed at sign-up.

## 5.1 By milestone

| Needed before | Item | Action for the investor | Cost | Notes |
|---|---|---|---|---|
| M0 | GitHub repository | Already exists | Free | Branch protection on `main` to be switched on in S0 |
| M1 | SEC EDGAR access | Provide a contact email for the request header | Free | No key or account. Header format and request rate to be taken from the SEC developer FAQ (unverified here) |
| M1 | FRED API key | Create an account and request a key | Free (unverified) | Key is required |
| M1 | Price data source | Decide after the S2 comparison (ADR-006) | USD 0-30 a month | See 5.3 |
| M3 | Embedding provider | Choose a hosted API or a local open-source model | Low or zero | Used for peer similarity |
| M5 | Model API access | Create an Anthropic Console account, add credit, set a spend limit | Usage-based | Credit minimum and limit controls to be confirmed in the Console (unverified) |
| M5 | Other model providers (optional) | Keys for any other family used as judge or as small workers | Usage-based | Needed only if a different judge family or open models are wanted |
| M7 | Interactive Brokers account | Open an individual cash account; fund it | USD 500 minimum equity for market data | Approval time not published (unverified). Start the application during M4 |
| M7 | IBKR paper trading | Enable in the account; a free trial exists without a funded account | Free | API access in the trial is not confirmed (unverified) |
| M7 | IBKR market data | Subscribe as needed | See 5.2 | Requires USD 500 equity |
| M7 | TradingView paid plan | Subscribe; enable two-factor authentication | From USD 12.95 a month on annual billing | Webhooks need two-factor authentication; the minimum plan for webhooks is not stated on the official page (unverified) |
| M7 | Public HTTPS endpoint for webhooks | Choose with the runtime decision | Low or zero | Tunnel or small host |
| M7 | Off-machine backup storage | Choose a storage bucket or drive | Low | |
| M8 | Live trading enablement | Sign the go-live checklist | n/a | |

## 5.2 Interactive Brokers details

| Topic | Finding | Source |
|---|---|---|
| Commission, IBKR Pro fixed | USD 0.005 a share, minimum USD 1.00, maximum 1% of trade value | commissions page |
| Commission, IBKR Pro tiered | USD 0.0035 a share at the lowest volume tier, minimum USD 0.35 an order | commissions page |
| Fractional shares | Commission is the greater of 1% of trade value or USD 0.01. API order types not confirmed (unverified) | commissions page |
| Market data, non-professional | Snapshot bundle USD 10 a month, waived above USD 5 commissions. Streaming add-on USD 4.50, waived above USD 15 commissions. Some real-time feeds free | market data page |
| Delayed data | Delayed US equity data is no longer offered through the account; some free real-time feeds exist | market data page |
| API on IBKR Lite | Not stated on the API page (unverified). Assume IBKR Pro is required until confirmed | API page |

At USD 5,000, a USD 1.00 minimum commission on a USD 400 position is 0.25% each way. The
small-account analysis in E8 measures what that does to returns.

## 5.3 Price data options

| Source | Free tier | Paid | Delisted companies | Status |
|---|---|---|---|---|
| IBKR historical data | With account and subscription | See 5.2 | Limited | Candidate primary once the account exists |
| Tiingo | 50 requests an hour, 500 symbols a month | USD 30 a month | Not stated (unverified) | Candidate |
| EODHD | 20 calls a day | USD 19.99 a month | Not stated (unverified) | Candidate |
| Norgate Data | n/a | Not fetched (unverified) | Usually cited as survivorship-free (unverified) | To assess if budget allows |
| Sharadar via Nasdaq Data Link | n/a | Not fetched (unverified) | Usually cited as survivorship-free (unverified) | To assess if budget allows |
| Stooq | n/a | n/a | n/a | Excluded: the site disallows automated access |

S2 includes a comparison on `pilot-25` and a written recommendation.

## 5.4 Sources

- https://www.interactivebrokers.com/en/pricing/commissions-stocks.php
- https://www.interactivebrokers.com/en/pricing/market-data-pricing.php
- https://www.interactivebrokers.com/en/trading/free-trial.php
- https://www.interactivebrokers.com/en/trading/ib-api.php
- https://www.tradingview.com/pricing/
- https://www.tradingview.com/support/solutions/43000529348-about-webhooks/
- https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- https://fred.stlouisfed.org/docs/api/api_key.html
- https://www.tiingo.com/about/pricing
- https://eodhd.com/pricing
