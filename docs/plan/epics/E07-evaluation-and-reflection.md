# E7. Evaluation and reflection

**Goal:** no memo drives a decision unless a deterministic judge and a blind LLM judge both pass it; judges are themselves tested; revisions are targeted; team shapes are benchmarked on attempts needed to reach a score.
**Depends on:** E6 for memos; E2 to E5 for the data the deterministic judge checks against.
**Milestone:** M5.

## Rubric v1

Sub-dimensions score 0 (bad), 1 (partial) or 2 (fully met).
Dimension score = 1 + 4 x points earned / points possible, giving 1.0 to 5.0.
Overall = weighted mean of dimensions.

| Dimension | Sub-dimensions | Critical |
|---|---|---|
| Grounded decisions | Reasoning without jumps; facts corroborated by reputable sources; sub-agent reasoning vetted | none |
| Data integrity | Statements tie out; audited and unaudited labelled; every figure traceable | tie-out, traceable |
| Analytical depth | Fundamentals covered; peer set justified; trends explained | none |
| Valuation soundness | Assumptions explicit and defensible; scenarios and sensitivity; methods cross-checked | scenario arithmetic |
| Risk discipline | Fits the mandate; downside quantified; thesis-breakers stated | mandate fit |
| Clarity | Clear verdict; plain language; what would change the view | none |
| Backtest validity (strategies only) | No look-ahead; costs included; out-of-sample tested | no look-ahead |

Gate: per dimension the final score is the lower of the two judges. A memo passes when every
dimension is at least 4.0 and neither judge gives 0 on a critical sub-dimension. A gap above 1.0
between the judges on any dimension marks the memo disputed and sends it to human review.

## Features

| ID | Sprint | Feature | Acceptance checks |
|---|---|---|---|
| F-E7-01 | S10 | Rubric as versioned config | Dimensions, sub-dimensions, descriptors for scores 0, 1 and 2, weights, critical flags, pass mark. Scoring formula implemented once. Rubric version stored on every score. |
| F-E7-02 | S10 | Deterministic judge | One documented check per sub-dimension, returning score and evidence. A pure function of memo and data snapshot. A coverage statement lists what each check can and cannot detect. |
| F-E7-03 | S11 | LLM judge | Fresh context per call. No attempt number, prior scores, critiques or author identity in the prompt. A verbatim quote is required per score and verified. Three runs, median taken. Different model family from the author where available. |
| F-E7-04 | S10 | Concurrence gate | Implements the gate rules above, including the disputed state and the human review queue. |
| F-E7-05 | S10 | Defect library and judge mutation testing | At least 30 defect types with injectors (wrong figure, unsupported conclusion, single-source fact, unvetted part, probabilities not summing to one, mandate breach, vague thesis-breaker, and others). Sensitivity reported per judge per defect. |
| F-E7-06 | S11 | Human gold set and calibration | Investor grades 15 memos on the rubric. Agreement metrics computed. Descriptors and judge prompt tuned, then frozen as a judge version. |
| F-E7-07 | S11 | Judge drift monitoring | Anchor memos re-scored on every judge, prompt or model change and monthly. Shifts beyond tolerance raise an alert. |
| F-E7-08 | S11 | Targeted reflection loop | Critique routed to the part that owns the failed sub-dimension, with the previous draft. Sub-dimensions that passed may not regress. Attempt cap, then escalation with both judges' evidence. |
| F-E7-09 | S11 | Cross-run lessons | Recurring failures summarized into versioned guidance. Guidance is adopted only after an A/B run shows fewer attempts to pass. |
| F-E7-10 | S16 | Outcome reflection | Thesis-breakers monitored against new data with alerts. Quarterly review compares past verdicts with outcomes; lessons recorded for human review, not auto-applied. |
| F-E7-11 | S11 | Team benchmark harness | Tickers by team shapes by seeds. Reports attempts to pass, attempts to reach a chosen score, score by attempt, pass rate at each attempt, tokens, cost, wall time and judge inflation, with median and interquartile range. |
| F-E7-12 | S10 | Score store and scorecard data | All sub-scores from both judges with evidence, linked to memo, attempt, rubric version and judge version. |

## Tests

| ID | Type | Covers | Test |
|---|---|---|---|
| T-E7-01 | U | F-E7-01 | Scoring formula on enumerated cases: all zeros give 1.0, all twos give 5.0, mixed cases give the expected decimals; weights applied. |
| T-E7-02 | U | F-E7-02 | For each sub-dimension, three fixtures score 2, 1 and 0 respectively, with evidence populated. |
| T-E7-03 | P | F-E7-02 | The same memo and snapshot give identical scores and evidence over 100 runs. |
| T-E7-04 | EV | F-E7-02, F-E7-05 | Deterministic judge catches 100% of critical-defect injections and at least 90% of the non-critical defects its coverage statement claims. |
| T-E7-05 | EV | F-E7-03, F-E7-05 | LLM judge sensitivity on the defect library is at least 85%, on recorded responses in PRs and live nightly. |
| T-E7-06 | U | F-E7-03 | The rendered judge prompt contains no attempt number, prior score, critique text or team name. |
| T-E7-07 | U | F-E7-03 | A quote not present in the memo sets that sub-score to zero. |
| T-E7-08 | U | F-E7-04 | Truth table: LLM pass with deterministic fail fails; deterministic pass with LLM fail fails; both pass passes; a critical zero fails regardless of averages; a gap above 1.0 marks disputed. |
| T-E7-09 | EV | F-E7-03, F-E7-04 | Saturation: one flawed memo resubmitted five times with trivial rewording does not gain more than 0.25 from the LLM judge, and never passes the gate. |
| T-E7-10 | EV | F-E7-06 | Against the investor's grades: exact sub-score agreement at least 70%, within one point at least 95%, weighted kappa at least 0.6, and no memo the investor failed on a critical item passes the gate. |
| T-E7-11 | U | F-E7-08 | A revision that fixes one sub-dimension and lowers a previously passing one is flagged as a regression. |
| T-E7-12 | U | F-E7-08 | Reaching the attempt cap sets status escalated and attaches both judges' evidence. |
| T-E7-13 | I | F-E7-11 | With the fake provider the harness produces a report in the expected schema, and fixed seeds reproduce it. |
| T-E7-14 | EV | F-E7-11 | Live, cost-capped: at least 20 tickers, at least two team shapes, three seeds each. Report delivered with all listed metrics. |
| T-E7-15 | U | F-E7-07 | An anchor re-score beyond tolerance raises an alert naming the changed component. |
| T-E7-16 | U | F-E7-10 | Engineered data crossing a thesis-breaker threshold raises an alert linked to the memo. |
| T-E7-17 | EV | F-E7-09 | A/B run with and without guidance reports attempts to pass for both arms; adoption is recorded only if the guided arm is better. |
| T-E7-18 | U | F-E7-12 | Scores read back from the store equal those returned by the judges; each row has rubric and judge versions. |
| T-E7-19 | U | F-E7-03 | The median of three judge runs is used; a run that fails schema validation is repeated, not counted as zero. |
| T-E7-20 | M | F-E7-06, F-E7-11 | Investor grades the gold set, then reviews the calibration and benchmark reports. |

## Known limits

- The deterministic judge checks structure, arithmetic, provenance and rule compliance. It does not judge insight. Its coverage statement says so per sub-dimension.
- Calibration needs about 15 memos graded by the investor; plan several hours for it.
- Benchmark results apply to the models, prompts and tickers tested, not in general.
