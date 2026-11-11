# E6. Agent teams

**Goal:** agent teams in selectable shapes that turn the services' outputs into a structured investment memo, with every call traced and budgeted.
**Depends on:** E2 to E5 for content. Model API access.
**Milestone:** M5.

## Team shapes

| Preset | Lead | Workers | Use |
|---|---|---|---|
| `frontier-1` | Frontier model | none (lead does all parts; a second call vets) | Baseline |
| `frontier-3` | Frontier model | 2 frontier | Few strong agents |
| `swarm-12` | Frontier model | 12 small models with high reasoning | Many small agents, guided |
| `swarm-30` | Frontier model | 30 small models with high reasoning | Scale test |
| `hybrid` | Frontier model | small models draft, frontier vets | Cost and quality trade-off |

Models are named in config. Any model reachable through a provider adapter can fill a role.

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E6-01 | S9 | Provider abstraction | One protocol for completion, structured output, tool use and usage reporting. Adapters: Anthropic, an OpenAI-compatible endpoint for other and open models, and a fake for tests. |
| F-E6-02 | S9 | Team configuration | Schema-validated config for lead, workers (model, count, reasoning settings) and judge. The presets above ship in the repo. |
| F-E6-03 | S9 | Read-only agent tools | Tools to fetch statements, metrics, peers, valuation and filing sections, and to compute an expression over figure ids. A number that did not come from a tool result is rejected before judging. |
| F-E6-04 | S9 | Memo schema | Versioned schema: figures (reported or computed), claims with support links and sources, analysis sections, peers, assumptions, scenarios, methods, risks, machine-checkable thesis-breakers, verdict. |
| F-E6-05 | S9 | Workflow | Lead plans; workers draft parts in parallel, several drafts per part in swarm shapes; a different agent vets each part; lead assembles. |
| F-E6-06 | S9 | Structured-output robustness | Schema validation, up to two repair attempts, then a typed failure. |
| F-E6-07 | S9 | Budgets and limits | Token and cost cap per run, timeout per call, concurrency cap, provider rate-limit handling. |
| F-E6-08 | S9 | Trace store | Every call stored with prompt hash, model, parameters, tokens, latency, cost and output, linked to run and memo. |
| F-E6-09 | S9 | Prompt management | Prompts as versioned files. The prompt version is recorded on every memo. |
| F-E6-10 | S10 | Untrusted-text handling | Filing and web text passed as delimited data. Instructions inside it have no effect on verdicts. |
| F-E6-11 | S10 | Response cache | Deterministic cache for development and test replay. Disabled in benchmarks. |
| F-E6-12 | S10 | Narrative rendering | Narrative text refers to figures by id; numbers are filled in from the figure table at render time. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E6-01 | C | F-E6-01 | Every adapter, including the fake, passes the shared provider contract suite on recorded responses. |
| T-E6-02 | C | F-E6-01 | Nightly, cost-capped: one live structured-output call per configured model succeeds. |
| T-E6-03 | U | F-E6-02 | Unknown model, zero worker count or missing judge fail config validation with a clear message. |
| T-E6-04 | U | F-E6-03 | A memo containing a number absent from all tool results and computed figures is rejected before judging. |
| T-E6-05 | U | F-E6-05 | With the fake provider: parts are drafted in parallel and vetted by a different agent id; in `frontier-1` the vetting call is separate from the drafting call. |
| T-E6-06 | U | F-E6-06 | Malformed output is repaired on retry; a third failure ends the run with the typed error. |
| T-E6-07 | U | F-E6-07 | A run that hits its cap stops, saves a partial trace, and reports status budget-exceeded. |
| T-E6-08 | U | F-E6-08 | Trace row count equals provider call count, and summed cost equals the run total. |
| T-E6-09 | EV | F-E6-10 | Filing text containing an embedded instruction to rate the company a buy leaves the verdict unchanged on recorded and live runs. |
| T-E6-10 | U | F-E6-12 | Every number in a rendered narrative maps to a figure id. |
| T-E6-11 | I | F-E6-04, F-E6-05 | End to end on recorded responses for one company yields a schema-valid memo with all parts. |
| T-E6-12 | U | F-E6-09 | Editing a prompt file produces a new prompt version on the next memo. |
| T-E6-13 | U | F-E6-11 | The cache returns the stored response for an identical key and is bypassed when the benchmark flag is set. |
| T-E6-14 | U | F-E6-04 | A thesis-breaker that cannot be parsed into a metric, comparison and threshold is rejected by the schema. |

## Known limits

- Reasoning-effort settings differ by provider; each adapter documents what it supports.
- Small open models may fail structured output more often. The benchmark in E7 measures this rather than assuming it.
