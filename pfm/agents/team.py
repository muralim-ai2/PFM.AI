"""Team orchestration. Same code path for both shapes; only config changes:
  frontier - 1-3 strong agents;  swarm - many small agents guided and assembled by a frontier lead.
Workers draft parts in parallel, a different agent vets each part, the lead writes the verdict."""
import json
from concurrent.futures import ThreadPoolExecutor
from ..memo import Memo, PARTS, LEAD, part_hash

WORKER = ("You write one part of an investment memo as JSON with exactly these top-level keys: {keys}. "
          "Use only numbers present in the statements. Cite figures as [F1]. Reply with JSON only.")
VERIFY = ("You are a verifier. Check the drafts against the statements, fix any error, and return the single "
          "best corrected draft as JSON only, same keys.")
LEADSYS = ("You are the lead analyst. Given the vetted parts, return JSON only with keys: "
           + ", ".join(LEAD) + ". Verdict is buy, hold or avoid and must follow the margin of safety.")


def parse(s):
    return json.loads(s[s.find("{"):s.rfind("}") + 1])


def _stub(ticker, price, **fields):
    return Memo.model_validate({"ticker": ticker, "price": price, "verdict": "hold", "summary": "", **fields})


def write(provider, team, ticker, price, evidence, schema, prev=None, critique=None, lessons=""):
    """prev: {part: fragment} from the last attempt. critique: {part: text}; only criticised parts are redone."""
    w, lead = team["workers"], team["lead"]
    k = max(1, w["count"] // len(PARTS))          # drafts per part
    todo = [p for p in PARTS if not prev or p in (critique or {})]
    ctx = f"TICKER: {ticker}\nPRICE: {price}\nSTATEMENTS\n{json.dumps(evidence)}\nSCHEMA\n{json.dumps(schema)}\n"

    def draft(job):
        part, i = job
        p = f"PART: {part}\n{ctx}"
        if lessons:
            p += f"COMMON FAILURES TO AVOID\n{lessons}\n"
        if prev and part in prev:
            p += f"PREVIOUS\n{json.dumps(prev[part])}\nCRITIQUE\n{critique[part]}\nRevise PREVIOUS; keep what was right.\n"
        return part, parse(provider.complete(w["model"], WORKER.format(keys=", ".join(PARTS[part])), p, w.get("extra")))

    def vet(part, drafts):
        # with a single worker the lead vets, so author and verifier always differ
        v = w if w["count"] > 1 else lead
        p = f"PART: {part}\n{ctx}DRAFTS\n{json.dumps(drafts)}"
        return part, parse(provider.complete(v["model"], VERIFY, p, v.get("extra")))

    with ThreadPoolExecutor(16) as ex:
        drafts = {}
        for part, d in ex.map(draft, [(p, i) for p in todo for i in range(k)]):
            drafts.setdefault(part, []).append(d)
        vetted = dict(ex.map(lambda kv: vet(*kv), drafts.items()))
    parts = {**(prev or {}), **vetted}

    head = parse(provider.complete(lead["model"], LEADSYS, f"{ctx}PARTS\n{json.dumps(parts)}\n"
                                   + (f"CRITIQUE\n{critique['lead']}" if critique and "lead" in critique else ""),
                                   lead.get("extra")))
    fields = {f: v for frag in parts.values() for f, v in frag.items()}
    fields.update({f: head[f] for f in LEAD if f in head})
    verifier = f"verifier:{(w if w['count'] > 1 else lead)['model']}"
    # vetted_hash is the hash of what the verifier returned; the code judge re-hashes the memo against it
    fields["work"] = [{"agent": f"worker:{w['model']}", "part": p, "vetted_by": verifier,
                       "output_hash": (h := part_hash(_stub(ticker, price, **parts[p]), p)), "vetted_hash": h}
                      for p in PARTS]
    return _stub(ticker, price, **fields), parts
