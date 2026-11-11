# 2. Target architecture

## 2.1 Layers

```
                 +--------------------------------------------------+
  interfaces     |  CLI  |  dashboard  |  webhook receiver  | jobs  |
                 +--------------------------------------------------+
  services       | ingest | statements | fundamentals | peers       |
                 | models | agents | evaluation | backtest          |
                 | portfolio | execution | reporting                |
                 +--------------------------------------------------+
  domain         | entities, value objects, metric and model        |
                 | registries, rubric, mandate rules (pure Python)  |
                 +--------------------------------------------------+
  adapters       | EDGAR | FRED | price providers | LLM providers   |
                 | IBKR | embeddings | storage | notifications      |
                 +--------------------------------------------------+
  storage        | SQLite (records) | Parquet + DuckDB (series)     |
                 | raw archive (immutable payloads) | snapshots     |
                 +--------------------------------------------------+
```

Rules, enforced by import contracts in CI:

- `domain` imports nothing from `services`, `adapters` or `interfaces`.
- `services` depend on adapter protocols, never on a vendor SDK.
- `interfaces` call services only.

## 2.2 Data flow

1. Ingest jobs pull raw payloads, archive them unchanged with a hash, and load typed rows that carry a knowledge time.
2. Data-quality checks run. A critical failure blocks that company downstream.
3. Statements service maps facts to the standard chart of accounts, derives periods, runs integrity checks, records lineage.
4. Fundamentals and peer services compute from statements through the metric registry.
5. Models service screens, values and produces medium-term signals. Outputs are stored with model version and data snapshot id.
6. Agent teams read those outputs through read-only tools and write a structured memo.
7. Evaluation scores the memo with both judges. Failures go back for targeted revision. Passing memos become eligible for portfolio use.
8. Portfolio service builds order proposals inside the mandate limits.
9. The investor approves. Execution sends approved orders to IBKR and reconciles.
10. Reporting renders statements, memos, scorecards and portfolio reports.

## 2.3 Time model

| Field | Meaning |
|---|---|
| `period_end` / `period_type` | What the number describes |
| `knowledge_time` | When it became public (filing acceptance time, price date) |
| `ingested_at` | When this system stored it |
| `superseded_by` | Link to a later restated value, if any |

`as_of(t)` returns only rows with `knowledge_time <= t`. Backtests, historical peer sets and
historical valuations all read through it. A data snapshot id freezes a consistent view for
reproducible runs.

## 2.4 Core entities

| Area | Tables |
|---|---|
| Reference | company, ticker_history, universe, universe_member |
| Filings | filing, filing_document, filing_section, raw_payload |
| Facts | xbrl_fact, mapping_rule, mapping_override, mapping_proposal |
| Statements | statement_line, statement_check, restatement |
| Market | price_daily (Parquet), corporate_action, macro_series, benchmark_series |
| Analysis | metric_def, metric_value, peer_set, peer_member, peer_override |
| Models | model_def, screen_result, valuation, scenario, signal |
| Agents | team_config, llm_call, memo, memo_part |
| Evaluation | rubric_version, eval_score, gold_grade, defect_case, benchmark_run |
| Portfolio | mandate, target_weight, order_proposal, approval, ledger_lot, cash_movement |
| Execution | broker_order, fill, reconciliation, audit_log |
| Operations | job_run, dq_result, snapshot, cost_entry, alert |

## 2.5 Cross-cutting rules

- Idempotent jobs: running twice changes nothing.
- Every stored number can be traced to a source payload or a registered formula.
- Every model, metric, mapping, prompt and rubric has a version recorded on its outputs.
- Live trading is off by default and guarded by a config flag, an account-id check and a go-live checklist.
- Filing text and any web text are passed to models as data, never as instructions.
