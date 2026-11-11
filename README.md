# PFM.AI

Personal fund manager: builds financial statements from SEC filings, has an agent team write an investment memo, and only accepts the memo when two independent judges agree.

## Setup
```
pip install -e ".[llm,dev]"
export SEC_USER_AGENT="PFM.AI you@example.com"   # SEC requires a contact
export ANTHROPIC_API_KEY=...
```

## Commands
| Command | Does |
|---|---|
| `pfm ingest AAPL MSFT` | Pulls EDGAR filings, builds statements, runs tie-out checks |
| `pfm statements AAPL` | 3 audited fiscal years + unaudited interim quarters |
| `pfm analyze AAPL --price 230 --team swarm` | Writes a memo, loops until both judges pass or 5 attempts |
| `pfm bench AAPL:230 MSFT:410 --teams frontier swarm` | Attempts-to-pass, score per attempt, tokens, time per team |
| `pfm --mock bench TESTCO:48` | Offline dry run on a synthetic company with a scripted model |

## Evaluation
- 6 dimensions x 3 sub-dimensions, each scored 0/1/2. Dimension = 1 + 4 x earned / possible.
- Code judge: recomputes every figure against the database, checks the reasoning chain, scenario arithmetic, mandate limits, and that vetted text is the text in the memo.
- LLM judge: fresh context each attempt, never sees attempt number or past scores, must quote the memo for each score.
- Gate: final = lower of the two per dimension; all dimensions >= 4.0; no 0 on a critical sub-dimension.
- Reflection: failed sub-dimensions go back only to the part that owns them; the most frequent failures across runs are fed to every worker.

## Teams (`config/teams.yaml`)
- `frontier`: one or a few strong agents.
- `swarm`: many small agents drafting in parallel, vetted, assembled by a frontier lead.

## Not built yet
Peer selection from real data, DCF engine, price feed, IBKR execution, backtest, trailing-twelve-month view, quarterly outcome reflection.
