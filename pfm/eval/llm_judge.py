"""Blind LLM judge. Fresh context every call: it never sees the attempt number, earlier scores,
or earlier critiques, so it cannot drift upward across attempts. Every score needs a verbatim
quote from the memo; a quote that isn't in the memo scores 0."""
import json

SYSTEM = ("You are a sceptical investment-committee reviewer. Score each sub-dimension 0 (bad), 1 (partial) "
          "or 2 (fully met). Default to 1 unless the memo gives clear evidence for 2. For each score give a "
          "verbatim quote from the memo as evidence. Reply with JSON only: "
          '{"<dimension>": {"<sub>": {"score": 0, "quote": "...", "reason": "..."}}}')


def judge(memo, evidence, rubric, provider, cfg):
    text = memo.model_dump_json()
    crit = {d: {s: m["desc"] for s, m in spec["subs"].items()} for d, spec in rubric["dimensions"].items()}
    prompt = f"RUBRIC\n{json.dumps(crit)}\n\nSTATEMENTS\n{json.dumps(evidence)}\n\nMEMO\n{text}"
    out = provider.complete(cfg["model"], SYSTEM, prompt, cfg.get("extra"))
    raw = json.loads(out[out.find("{"):out.rfind("}") + 1])
    scores, notes = {}, {}
    for d, subs in crit.items():
        scores[d], notes[d] = {}, {}
        for s in subs:
            r = raw.get(d, {}).get(s, {})
            quoted = bool(r.get("quote")) and json.dumps(r["quote"], ensure_ascii=False)[1:-1] in text
            scores[d][s] = int(r.get("score", 0)) if quoted else 0
            notes[d][s] = r.get("reason", "") if quoted else "quote not found in memo"
    return scores, notes
