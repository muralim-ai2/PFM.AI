"""Code-only judge. Same memo in, same score out. Checks structure, arithmetic and provenance;
it cannot judge insight, which is the LLM judge's job."""
import ast
import re
from urllib.parse import urlparse
from .. import statements
from ..memo import PARTS, part_hash

SECTIONS = ["growth", "margins", "returns", "leverage", "cash_conversion", "earnings_quality"]
REQUIRED = ["revenue_growth", "operating_margin", "wacc", "terminal_growth"]
CAUSAL = re.compile(r"\b(because|due to|driven by|as a result|reflect)", re.I)
_OK = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Name, ast.Constant, ast.Load, ast.operator, ast.unaryop)


def _calc(expr, env):
    tree = ast.parse(expr, mode="eval")
    if not all(isinstance(n, _OK) for n in ast.walk(tree)):
        raise ValueError(expr)
    return eval(compile(tree, "", "eval"), {"__builtins__": {}}, env)


def _frac(ok, n):
    return 2 if n and ok == n else 1 if n and ok / n >= 0.8 else 0


def _close(a, b, tol=0.005):
    return a is not None and b is not None and abs(a - b) <= tol * max(abs(b), 1e-9)


def judge(memo, con, cik, rubric):
    figs = {f.id: f for f in memo.figures}
    claims = {c.id: c for c in memo.claims}
    cfg = rubric["mandate"]
    accns = {r[0] for r in con.execute("select distinct accn from fact where cik=?", (cik,))}

    # --- data integrity
    ties = statements.checks(con, cik)
    tie = 2 if ties and all(t["ok"] for t in ties) else 0
    reported = [f for f in figs.values() if f.item]
    db = {f.id: con.execute("select value, audited from statement_line where cik=? and item=? and period_end=? and period_type=?",
                            (cik, f.item, f.period_end, f.period_type)).fetchone() for f in reported}
    env = {f.id: f.value for f in reported if db[f.id] and _close(f.value, db[f.id][0])}
    ok = len(env)
    for f in figs.values():
        if f.expr:
            try:
                if _close(f.value, _calc(f.expr, env)):
                    env[f.id] = f.value
                    ok += 1
            except Exception:
                pass
    traceable = 2 if figs and ok == len(figs) else 0   # one wrong number fails the memo
    labelled = _frac(sum(bool(db[f.id]) and f.audited == bool(db[f.id][1]) for f in reported), len(reported))

    # --- grounded decisions
    def grounded(cid, seen=()):
        if cid in figs:
            return cid in env
        c = claims.get(cid)
        if not c or cid in seen:
            return False
        if c.kind == "fact":
            return True
        return bool(c.supports) and all(grounded(s, seen + (cid,)) for s in c.supports)
    derived = [c for c in claims.values() if c.kind != "fact"]
    has_conclusion = any(c.kind == "conclusion" for c in derived)
    no_jumps = _frac(sum(grounded(c.id) for c in derived), len(derived)) if has_conclusion else 0

    def corroborated(c):
        if any(s.ref in accns for s in c.sources) or any(s in env for s in c.supports):
            return True
        pubs = {s.publisher.lower() for s in c.sources
                if any(urlparse(s.ref).netloc.endswith(d) for d in rubric["reputable"])}
        return len(pubs) >= 2
    facts = [c for c in claims.values() if c.kind == "fact"]
    corr = _frac(sum(corroborated(c) for c in facts), len(facts))
    # a part counts only if a different agent vetted exactly the text that is in the memo
    by_part = {w.part: w for w in memo.work}
    vetted = _frac(sum(p in by_part and bool(by_part[p].vetted_by) and by_part[p].vetted_by != by_part[p].agent
                       and by_part[p].vetted_hash == part_hash(memo, p) for p in PARTS), len(PARTS))

    # --- analytical depth
    refs = {s: set(re.findall(r"\[(F\d+)\]", memo.analysis.get(s, ""))) & set(figs) for s in SECTIONS}
    coverage = _frac(sum(len(memo.analysis.get(s, "").split()) >= 40 and bool(refs[s]) for s in SECTIONS), len(SECTIONS))
    trends = _frac(sum(len({figs[r].period_end for r in refs[s] if figs[r].period_end}) >= 2
                       and bool(CAUSAL.search(memo.analysis.get(s, ""))) for s in SECTIONS), len(SECTIONS))
    tick = [p.get("ticker", "").upper() for p in memo.peers]
    good = sum(len(p.get("reason", "").split()) >= 8 for p in memo.peers)
    peers = 0 if not 5 <= len(set(tick) - {memo.ticker.upper()}) <= 10 or len(tick) != len(set(tick)) else _frac(good, len(tick))

    # --- valuation soundness
    a = {x.name: x for x in memo.assumptions}
    if not all(n in a for n in REQUIRED) or not (a["terminal_growth"].value < a["wacc"].value
                                                 and a["terminal_growth"].value <= 0.04 and 0.05 <= a["wacc"].value <= 0.15):
        assume = 0
    else:
        assume = 2 if all(len(a[n].rationale.split()) >= 10 and a[n].basis and all(b in env for b in a[n].basis)
                          for n in REQUIRED) else 1
    sc = memo.scenarios
    if set(sc) >= {"bear", "base", "bull"} and sc["bear"].value_per_share < sc["base"].value_per_share < sc["bull"].value_per_share \
            and abs(sum(s.prob for s in sc.values()) - 1) < 1e-6:
        ev = sum(s.value_per_share * s.prob for s in sc.values())
        scen = 2 if _close(memo.expected_value, ev, 0.01) else 1
    else:
        scen = 0
    base = sc["base"].value_per_share if "base" in sc else None
    vals = list(memo.methods.values())
    cross = 0 if len(vals) < 2 else 2 if (base and min(vals) * 0.8 <= base <= max(vals) * 1.2) or len(memo.method_gap_note.split()) >= 15 else 1

    # --- risk discipline
    mandate = 2 if (0 < memo.position_pct <= cfg["max_position_pct"] and memo.sector_pct <= cfg["max_sector_pct"]
                    and not memo.uses_margin) or memo.verdict != "buy" and not memo.uses_margin else 0
    down = 0 if len(memo.risks) < 3 else _frac(sum(r.downside_pct is not None for r in memo.risks), len(memo.risks))
    specific = sum(bool(re.search(r"\d", t)) for t in memo.thesis_breakers)
    breakers = 2 if specific >= 2 else 1 if specific == 1 else 0

    # --- clarity
    mos = (base - memo.price) / base if base else None
    want = None if mos is None else "buy" if mos >= cfg["margin_of_safety"] else "avoid" if mos < 0 else "hold"
    verdict = 2 if want == memo.verdict else 0
    sents = [s for s in re.split(r"[.!?]+\s*", memo.summary) if s.strip()]
    words = len(memo.summary.split())
    avg = words / len(sents) if sents else 99
    plain = 2 if avg <= 25 and 30 <= words <= 200 else 1 if avg <= 35 and words else 0
    change = min(len(memo.change_my_mind), 2)

    return {
        "grounded_decisions": {"no_jumps": no_jumps, "corroborated": corr, "subagents_vetted": vetted},
        "data_integrity": {"tie_out": tie, "audited_labelled": labelled, "traceable": traceable},
        "analytical_depth": {"coverage": coverage, "peers_justified": peers, "trends_explained": trends},
        "valuation_soundness": {"assumptions_explicit": assume, "scenarios": scen, "cross_checked": cross},
        "risk_discipline": {"mandate_fit": mandate, "downside_quantified": down, "thesis_breakers": breakers},
        "clarity": {"clear_verdict": verdict, "plain_language": plain, "change_my_mind": change},
    }
