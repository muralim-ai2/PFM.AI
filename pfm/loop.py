"""Write -> two judges -> gate -> targeted revision. Stops on pass or max_attempts."""
import json
import time
from .agents import team as team_mod
from .eval import deterministic, llm_judge, rubric as rb
from .memo import Memo, PARTS
from . import statements

SUB_PART = {s: p for p, subs in {
    "analysis": ["no_jumps", "corroborated", "coverage", "trends_explained", "traceable", "audited_labelled"],
    "peers": ["peers_justified"],
    "valuation": ["assumptions_explicit", "scenarios", "cross_checked"],
    "risk": ["downside_quantified", "thesis_breakers", "change_my_mind"],
    "lead": ["clear_verdict", "plain_language", "mandate_fit"]}.items() for s in subs}


def lessons(con, n=5):
    """Cross-run reflection: the sub-dimensions that fail most often, fed to every worker."""
    rows = con.execute("select sub, count(*) c from eval_score where judge='final' and score<2 "
                       "group by sub order by c desc limit ?", (n,)).fetchall()
    return "\n".join(f"- {s} (failed {c}x)" for s, c in rows)


def run(con, cik, ticker, price, team_name, cfg, provider, rubric=None):
    rubric = rubric or rb.load()
    team, evidence = cfg["teams"][team_name], statements.view(con, cik)
    descs = {s: m["desc"] for spec in rubric["dimensions"].values() for s, m in spec["subs"].items()}
    schema = {p: {f: Memo.model_json_schema()["properties"][f] for f in fs} for p, fs in PARTS.items()}
    schema["$defs"] = Memo.model_json_schema().get("$defs", {})
    t0, tok0 = time.time(), provider.tokens
    run_id = con.execute("insert into run(ticker, team) values(?,?)", (ticker, team_name)).lastrowid
    prev = critique = None
    hint, trajectory = lessons(con), []
    for attempt in range(1, rubric["max_attempts"] + 1):
        memo, prev = team_mod.write(provider, team, ticker, price, evidence, schema, prev, critique, hint)
        det = deterministic.judge(memo, con, cik, rubric)
        llm, notes = llm_judge.judge(memo, evidence, rubric, provider, cfg["judge"])
        g = rb.gate(rubric, det, llm)
        memo_id = con.execute("insert into memo(run_id, attempt, json) values(?,?,?)",
                              (run_id, attempt, memo.model_dump_json())).lastrowid
        con.executemany("insert into eval_score values(?,?,?,?,?,?)", [
            (memo_id, j, d, s, v, notes[d][s] if j == "llm" else "")
            for j, sc in (("det", det), ("llm", llm), ("final", {d: {s: min(det[d][s], llm[d][s]) for s in det[d]} for d in det}))
            for d in sc for s, v in sc[d].items()])
        trajectory.append({"attempt": attempt, "overall": g["overall"], "det": rb.overall(rubric, g["deterministic"]),
                           "llm": rb.overall(rubric, g["llm"]), "weak": g["weak"]})
        if g["passed"]:
            break
        critique = {}
        for key in g["weak"]:
            d, s = key.split(".")
            critique.setdefault(SUB_PART.get(s, "lead"), []).append(
                f"{s}: {descs[s]} (code judge {det[d][s]}/2, reviewer {llm[d][s]}/2. {notes[d][s]})")
        critique = {p: "\n".join(v) for p, v in critique.items()}
    res = {"ticker": ticker, "team": team_name, "attempts": attempt, "passed": g["passed"], "final": g["final"],
           "overall": g["overall"], "judge_inflation": g["judge_inflation"], "tokens": provider.tokens - tok0,
           "seconds": round(time.time() - t0, 1), "trajectory": trajectory, "memo": memo}
    con.execute("update run set attempts=?, passed=?, tokens=?, seconds=? where id=?",
                (attempt, int(g["passed"]), res["tokens"], res["seconds"], run_id))
    con.commit()
    return res
