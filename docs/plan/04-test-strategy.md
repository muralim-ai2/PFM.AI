# 4. Test strategy

## 4.1 Test types used in the epic files

| Code | Type | What it proves | Runs |
|---|---|---|---|
| U | Unit | One function or class behaves as specified | Every PR |
| P | Property | An invariant holds for generated inputs | Every PR |
| C | Contract | An adapter parses a recorded vendor response, or passes the shared adapter suite | Every PR (recorded), nightly (live) |
| I | Integration | Several components work together against a real local database | Every PR |
| G | Golden | Output equals hand-verified reference values from primary sources | Every PR |
| DQ | Data quality | Real ingested data meets coverage and consistency thresholds | Nightly and at milestones |
| EV | Evaluation | Judges, rubric and benchmark behave as required | PR (recorded), nightly (live) |
| E2E | End to end | A user-visible flow works through the interface | Milestone |
| CI | Pipeline | The build pipeline enforces a gate | Once per gate, then continuously |
| M | Manual acceptance | The investor checks evidence and signs off | Milestone |

## 4.2 Reference datasets

| Dataset | Content | Built in | Used by |
|---|---|---|---|
| `pilot-25` | 25 non-financial US companies across sectors and fiscal year-ends | S1 | DQ thresholds, milestone demos |
| `golden-statements` | 10 companies, 20 key lines, 3 fiscal years plus 3 quarters, hand-keyed from filings | S3-S4 | E2 golden tests |
| `golden-metrics` | 3 companies, every registered metric hand-calculated in a spreadsheet | S5 | E3 golden tests |
| `known-peers` | Pairs that must rank as peers | S6 | E4 |
| `valuation-examples` | Worked DCF, WACC and reverse-DCF examples with published answers | S7 | E5 |
| `defect-library` | 30 or more defect types with injectors applied to passing memos | S10 | E7 judge sensitivity |
| `gold-grades` | 15 memos graded by the investor on the rubric | S11 | E7 calibration |
| `anchor-memos` | Fixed memos re-scored on every judge change | S11 | E7 drift |
| `reference-returns` | Return series with metrics from a reference library | S12 | E8 |

Each dataset records its source, date, and who verified it. Golden values are entered from the
filing by hand, not copied from system output.

## 4.3 Checks that guard the known failure modes

| Failure mode | Guard |
|---|---|
| A number is wrong or invented | Lineage on every figure; deterministic judge recomputes all figures; narrative numbers rendered from figure ids |
| Look-ahead in models or backtests | `as_of` property test; perturbation test on signals; look-ahead canary strategy |
| Survivorship bias | Point-in-time universe membership; survivorship coverage report; flagged in every tearsheet |
| LLM judge drifts upward across attempts | Blind judge; saturation test; deterministic judge must concur |
| Judges miss defects | Mutation testing with the defect library; sensitivity thresholds |
| Judge disagrees with the investor | Gold-grade calibration with agreement thresholds |
| Statement mapping silently wrong | Golden statements; integrity checks; unmapped-material-tag report; reconciliation pack |
| Order sent in error | Approval hash check; live flag; account-id guard; notional caps; reconciliation halt |
| Results not reproducible | Snapshot ids; run manifests; byte-identical rerun tests |
| Costs run away | Per-run budget cap; cost ledger; budget alerts |

## 4.4 Evaluation of the evaluators

The two judges are tested like any other component.

- Deterministic judge: three fixtures per sub-dimension (scores 2, 1 and 0), a determinism test, and mutation tests.
- LLM judge: blindness asserted on the rendered prompt, quote verification, sensitivity on the defect library, a saturation test, and agreement with the investor's grades.
- Gate: truth table covering every combination of pass and fail from each judge, plus the critical-zero rule.

Thresholds are listed with the tests in `epics/E07-evaluation-and-reflection.md`.

## 4.5 Milestone evidence pack

At each milestone the following is delivered for review:

1. Test report: every test id in scope, with status.
2. Data-quality or evaluation report for that milestone.
3. A demo script the investor can run.
4. List of known limits and deferred items.
5. Decision log entries made during the milestone.
