from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def load(path=ROOT / "config/rubric.yaml"):
    return yaml.safe_load(Path(path).read_text())


def dim_scores(rubric, subs):
    """subs: {dimension: {sub: 0|1|2}} -> {dimension: 1.0-5.0}"""
    return {d: round(1 + 4 * sum(subs[d].get(s, 0) for s in spec["subs"]) / (2 * len(spec["subs"])), 2)
            for d, spec in rubric["dimensions"].items()}


def overall(rubric, dims):
    w = {d: s.get("weight", 1) for d, s in rubric["dimensions"].items()}
    return round(sum(dims[d] * w[d] for d in w) / sum(w.values()), 2)


def gate(rubric, det, llm):
    """Both judges must independently clear the pass mark. Final score is the lower of the two."""
    dd, dl = dim_scores(rubric, det), dim_scores(rubric, llm)
    final = {d: min(dd[d], dl[d]) for d in dd}
    crit = [f"{d}.{s}" for d, spec in rubric["dimensions"].items() for s, m in spec["subs"].items()
            if m.get("critical") and 0 in (det[d].get(s, 0), llm[d].get(s, 0))]
    weak = [f"{d}.{s}" for d in det for s in rubric["dimensions"][d]["subs"]
            if min(det[d].get(s, 0), llm[d].get(s, 0)) < 2]
    return {"passed": not crit and all(v >= rubric["pass_mark"] for v in final.values()),
            "final": final, "overall": overall(rubric, final), "deterministic": dd, "llm": dl,
            "judge_inflation": round(overall(rubric, dl) - overall(rubric, dd), 2),
            "critical_zero": crit, "weak": weak}
