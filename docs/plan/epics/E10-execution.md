# E10. Execution and approvals

**Goal:** approved orders reach Interactive Brokers safely, first on paper, with reconciliation and an audit trail. Nothing is sent without approval.
**Depends on:** E9. An IBKR account with paper trading and API access; market data subscription as needed.
**Milestone:** M7.

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E10-01 | S15 | Broker protocol | One interface for account, positions, cash, quotes, place, cancel, status and executions. Adapters: simulated, IBKR paper, IBKR live. |
| F-E10-02 | S15 | Connectivity | Gateway session management, reconnect, pacing-limit handling, clock check. |
| F-E10-03 | S15 | Contract resolution | Ticker to broker contract id and primary exchange, with fractional eligibility. |
| F-E10-04 | S15 | Approval workflow | Proposals wait in a queue. Approve or reject singly or in batch. The approval stores approver, time and a hash of the order. Approvals expire. |
| F-E10-05 | S15 | Order management | Limit orders with a price collar, day orders, idempotent client order ids, an explicit state machine, partial fills, and a cancel policy. |
| F-E10-06 | S15 | Reconciliation | After each session and daily: broker positions and cash against the ledger. A break raises an alert and halts new orders. |
| F-E10-07 | S15 | Safety controls | Live trading flag off by default. Account-id guard separating paper from live. Daily caps on notional and order count. Kill switch. |
| F-E10-08 | S15 | Audit log | Append-only, hash-chained record of proposals, approvals, orders and fills. |
| F-E10-09 | S15 | Execution quotes | Quote source per subscription with a stale-quote guard. |
| F-E10-10 | S15 | Go-live checklist | Written criteria: length of paper period, clean reconciliation streak, zero safety-control breaches, investor sign-off. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E10-01 | C | F-E10-01 | The simulated broker passes the broker contract suite. The same suite runs against the paper account on manual trigger. |
| T-E10-02 | U | F-E10-05 | Every legal state transition works and every illegal one is rejected. |
| T-E10-03 | U | F-E10-05 | Submitting twice with the same client order id creates one order. |
| T-E10-04 | U | F-E10-04 | No approval means no order. An expired approval is rejected. An order changed after approval fails the hash check. |
| T-E10-05 | I | F-E10-02, F-E10-05 | Disconnect after submit and before acknowledgement: on reconnect the state is recovered and no duplicate is sent. |
| T-E10-06 | U | F-E10-06 | An engineered position break is detected and blocks new orders until cleared. |
| T-E10-07 | U | F-E10-07 | With the live flag off the live adapter refuses to connect. In paper mode a non-paper account id is refused. |
| T-E10-08 | U | F-E10-07 | Orders beyond the daily notional or count cap are blocked. The kill switch cancels working orders and blocks new ones. |
| T-E10-09 | U | F-E10-09, F-E10-05 | A stale quote blocks the order. A limit price outside the collar is blocked. |
| T-E10-10 | U | F-E10-08 | Altering any audit record breaks chain verification. |
| T-E10-11 | I | F-E10-03, F-E10-05, F-E10-06 | On the paper account: one small limit order is placed and filled; ledger, broker and audit log agree. |
| T-E10-12 | U | F-E10-03 | A ticker with several listings resolves to the primary exchange; an unknown ticker gives a typed error. |
| T-E10-13 | M | F-E10-04, F-E10-10 | Investor approves a paper order end to end and reviews the go-live checklist. |
| T-E10-14 | U | F-E10-10, F-E10-07 | The live flag cannot be switched on unless a signed go-live checklist record exists; without it startup fails closed. |

## Known limits

- Fractional-share order types available through the API are to be confirmed against IBKR documentation during the sprint.
- Live trading is not enabled by this epic. It is enabled only at M8.
