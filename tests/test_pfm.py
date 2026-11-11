import copy
import yaml
import pytest
from pfm import db, edgar, statements, mock, loop, bench
from pfm.agents import team
from pfm.eval import deterministic, rubric as rb
from pfm.cli import ROOT

CFG = yaml.safe_load((ROOT / "config/teams.yaml").read_text())


@pytest.fixture
def con():
    c = db.connect(":memory:")
    statements.build(c, edgar.load(c, mock.companyfacts(), "TESTCO"))
    return c


def gold(**override):
    parts = copy.deepcopy(mock.GOLD)
    for part, fields in override.items():
        parts[part].update(fields)

    class P(mock.Mock):
        def complete(self, model, system, prompt, extra=None):
            if system in (team.LEADSYS, team.VERIFY):
                return super().complete(model, system, prompt)
            import json
            return json.dumps(parts[prompt.split("PART: ")[1].split("\n")[0]])
    return team.write(P(), CFG["teams"]["frontier"], "TESTCO", 48, {}, {})[0]


def test_statements_derive_and_tie(con):
    v = lambda item, end, pt: statements._val(con, 1, item, end, pt)
    assert v("Revenue", "2025-12-31", "Q") == 1210 - 895          # Q4 = FY - 9M
    assert v("CFO", "2026-06-30", "Q") == 50                       # cash-flow Q2 from YTD
    assert con.execute("select audited, derived from statement_line where item='Revenue' and period_end='2025-12-31' "
                       "and period_type='Q'").fetchone() == (0, 1)
    assert all(c["ok"] for c in statements.checks(con, 1)) and len(statements.checks(con, 1)) >= 9
    view = statements.view(con, 1)
    assert sorted(view["annual_audited"]) == ["2023-12-31", "2024-12-31", "2025-12-31"]
    assert sorted(view["interim_unaudited"]) == ["2026-03-31", "2026-06-30", "2026-09-30"]


def test_code_judge_gold_is_perfect(con):
    r = rb.load()
    det = deterministic.judge(gold(), con, 1, r)
    assert all(v == 2 for d in det.values() for v in d.values()), det
    assert set(rb.dim_scores(r, det).values()) == {5.0}


@pytest.mark.parametrize("part,fields,dim,sub", [
    ("valuation", {"expected_value": 75}, "valuation_soundness", "scenarios"),
    ("valuation", {"methods": {"dcf": 60}}, "valuation_soundness", "cross_checked"),
    ("peers", {"peers": []}, "analytical_depth", "peers_justified"),
    ("risk", {"thesis_breakers": ["It goes badly."]}, "risk_discipline", "thesis_breakers"),
])
def test_code_judge_catches_defects(con, part, fields, dim, sub):
    assert deterministic.judge(gold(**{part: fields}), con, 1, rb.load())[dim][sub] < 2


def test_wrong_number_and_tampering_fail(con):
    r = rb.load()
    m = gold()
    m.figures[1].value = 1300                                      # misquoted revenue
    det = deterministic.judge(m, con, 1, r)
    assert det["data_integrity"]["traceable"] == 0
    assert det["grounded_decisions"]["subagents_vetted"] < 2       # memo no longer matches vetted hash
    assert not rb.gate(r, det, {d: {s: 2 for s in v} for d, v in det.items()})["passed"]


def test_saturated_llm_judge_cannot_pass_alone(con):
    r = rb.load()
    perfect = {d: {s: 2 for s in spec["subs"]} for d, spec in r["dimensions"].items()}
    det = copy.deepcopy(perfect)
    det["risk_discipline"].update(downside_quantified=0, thesis_breakers=0)
    g = rb.gate(r, det, perfect)
    assert not g["passed"] and g["final"]["risk_discipline"] == pytest.approx(2.33) and g["judge_inflation"] > 0


def test_benchmark_mock(con):
    rows = bench.run(con, [(1, "TESTCO", 48)], ["frontier", "swarm"], CFG, mock.Mock())
    by = {r["team"]: r for r in rows}
    assert by["frontier"]["passed"] and by["swarm"]["passed"]
    assert by["frontier"]["attempts"] < by["swarm"]["attempts"]
    assert con.execute("select count(*) from eval_score").fetchone()[0] > 0
    print("\n" + bench.table(rows))
