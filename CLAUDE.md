# PFM.AI
Personal fund manager for a risk-averse 30/70 equity/debenture mandate. Cash account, no margin, human approves trades.

- Numbers come from code, never from an LLM. LLMs read, map, judge and write.
- Every memo must pass two judges: `pfm/eval/deterministic.py` (code) and `pfm/eval/llm_judge.py` (blind). Final score is the lower of the two.
- Rubric and mandate limits: `config/rubric.yaml`. Team shapes and models: `config/teams.yaml`.
- Keep code brief. Run `pytest -q` before committing. `pfm --mock bench TESTCO:48` is the offline smoke test.
- SQLite is the system of record; all statement figures keep their filing accession number.
