"""Offline dry run: a synthetic company (TESTCO) and a scripted model. Proves the plumbing only.
Benchmark numbers from the mock are simulated and say nothing about real models."""
import copy
import json
from .eval.llm_judge import SYSTEM as JUDGE
from .agents.team import VERIFY, LEADSYS
from .memo import PARTS


def companyfacts():
    """Three fiscal years (2023-2025) and three interim quarters of 2026, internally consistent."""
    facts = {}

    def add(tag, start, end, val, form):
        facts.setdefault(tag, {"units": {"USD": []}})["units"]["USD"].append(
            {"start": start, "end": end, "val": val, "form": form, "fy": int(end[:4]), "fp": "FY" if form == "10-K" else "Q",
             "filed": end, "accn": f"0000000001-{end[2:4]}-{end[5:7]}"} | ({} if start else {"start": None}))
    T = {"rev": "Revenues", "op": "OperatingIncomeLoss", "ni": "NetIncomeLoss",
         "cfo": "NetCashProvidedByUsedInOperatingActivities", "cfi": "NetCashProvidedByUsedInInvestingActivities",
         "cff": "NetCashProvidedByUsedInFinancingActivities", "chg": "CashAndCashEquivalentsPeriodIncreaseDecrease",
         "a": "Assets", "l": "Liabilities", "e": "StockholdersEquity", "le": "LiabilitiesAndStockholdersEquity", "debt": "LongTermDebt"}
    annual = {2023: dict(rev=1000, op=150, ni=100, cfo=140, cfi=-60, cff=-50, chg=30, a=2000, l=900, e=1100, debt=400),
              2024: dict(rev=1100, op=170, ni=115, cfo=160, cfi=-65, cff=-55, chg=40, a=2150, l=950, e=1200, debt=400),
              2025: dict(rev=1210, op=190, ni=130, cfo=180, cfi=-70, cff=-60, chg=50, a=2300, l=1000, e=1300, debt=380)}
    for y, d in annual.items():
        for k, v in d.items():
            add(T[k], None if k in "ale debt" else f"{y}-01-01", f"{y}-12-31", v, "10-K")
        add(T["le"], None, f"{y}-12-31", d["a"], "10-K")
    qends = ["03-31", "06-30", "09-30"]
    quarters = {2025: dict(rev=[290, 300, 305], op=[45, 47, 48], ni=[31, 32, 33], cfo=[42, 44, 46]),
                2026: dict(rev=[320, 330, 340], op=[51, 53, 55], ni=[35, 36, 38], cfo=[48, 50, 52])}
    for y, d in quarters.items():
        for k, vals in d.items():
            for i, e in enumerate(qends):
                add(T[k], f"{y}-01-01", f"{y}-{e}", sum(vals[:i + 1]), "10-Q")       # year-to-date
                if i and k != "cfo":
                    add(T[k], f"{y}-{['04-01', '07-01'][i - 1]}", f"{y}-{e}", vals[i], "10-Q")
    for i, e in enumerate(qends):
        a, l = 2350 + 50 * i, 1010 + 10 * i
        for k, v in dict(a=a, l=l, e=a - l, le=a).items():
            add(T[k], None, f"2026-{e}", v, "10-Q")
    return {"cik": 1, "entityName": "Test Co (synthetic)", "facts": {"us-gaap": facts}}


def _sec(topic, a, b, why):
    return (f"{topic} moved from [{a}] in fiscal 2023 to [{b}] in fiscal 2025, driven by {why}. The change is steady across "
            "all three audited years and continues in the unaudited interim quarters, which suggests the trend is "
            "structural and not a single-period effect or an accounting artefact.")


def _fig(i, label, value, item=None, end=None, expr=None, pt="FY"):
    return {"id": f"F{i}", "label": label, "value": value, "item": item, "period_end": end,
            "period_type": pt if item else None, "audited": (pt == "FY") if item else None, "expr": expr}


GOLD = {
    "analysis": {
        "figures": [
            _fig(1, "Revenue 2023", 1000, "Revenue", "2023-12-31"), _fig(2, "Revenue 2025", 1210, "Revenue", "2025-12-31"),
            _fig(3, "Revenue CAGR", 0.1, expr="(F2 / F1) ** 0.5 - 1"),
            _fig(4, "Operating income 2023", 150, "OperatingIncome", "2023-12-31"),
            _fig(5, "Operating income 2025", 190, "OperatingIncome", "2025-12-31"),
            _fig(6, "Operating margin 2025", 190 / 1210, expr="F5 / F2"), _fig(7, "Operating margin 2023", 0.15, expr="F4 / F1"),
            _fig(8, "Net income 2025", 130, "NetIncome", "2025-12-31"), _fig(9, "Equity 2025", 1300, "Equity", "2025-12-31"),
            _fig(10, "ROE 2025", 0.1, expr="F8 / F9"), _fig(11, "Net income 2023", 100, "NetIncome", "2023-12-31"),
            _fig(12, "Equity 2023", 1100, "Equity", "2023-12-31"), _fig(13, "Debt 2025", 380, "Debt", "2025-12-31"),
            _fig(14, "Debt 2023", 400, "Debt", "2023-12-31"), _fig(15, "CFO 2025", 180, "CFO", "2025-12-31"),
            _fig(16, "CFO 2023", 140, "CFO", "2023-12-31"), _fig(17, "Cash conversion 2025", 180 / 130, expr="F15 / F8"),
            _fig(18, "Revenue Q3 2026", 340, "Revenue", "2026-09-30", pt="Q")],
        "claims": [
            {"id": "C1", "text": "Revenue compounded at 10% a year over 2023-2025.", "kind": "fact", "supports": ["F3"]},
            {"id": "C2", "text": "Operating margin widened from 15.0% to 15.7%.", "kind": "fact", "supports": ["F6", "F7"]},
            {"id": "C3", "text": "Growth has been profitable and cash-backed.", "kind": "inference", "supports": ["C1", "C2", "F17"]},
            {"id": "C4", "text": "The shares trade below a conservative base value.", "kind": "conclusion", "supports": ["C3"]}],
        "analysis": {
            "growth": _sec("Revenue", "F1", "F2", "volume gains in the core segment"),
            "margins": _sec("Operating income", "F4", "F5", "operating leverage on a largely fixed cost base"),
            "returns": _sec("Net income on equity", "F11", "F8", "higher margins on a slowly growing equity base [F12] [F9]"),
            "leverage": _sec("Long-term debt", "F14", "F13", "scheduled repayments funded from operating cash flow"),
            "cash_conversion": _sec("Operating cash flow", "F16", "F15", "disciplined working capital and low capital intensity"),
            "earnings_quality": _sec("Cash earnings against reported profit [F11]", "F16", "F15", "cash flow growing faster than accruals"),
        }},
    "peers": {"peers": [{"ticker": t, "reason": "Same industry code, similar revenue scale and comparable end-market mix."}
                        for t in ["PEERA", "PEERB", "PEERC", "PEERD", "PEERE", "PEERF"]]},
    "valuation": {
        "assumptions": [
            {"name": "revenue_growth", "value": 0.08, "basis": ["F3"],
             "rationale": "Set below the three-year compound rate to allow for a slower mature phase ahead."},
            {"name": "operating_margin", "value": 0.155, "basis": ["F6"],
             "rationale": "Held just under the latest audited margin so no further expansion is assumed in the base case."},
            {"name": "wacc", "value": 0.09, "basis": ["F13"],
             "rationale": "Reflects modest leverage and a mid-range equity risk premium over the current risk-free rate."},
            {"name": "terminal_growth", "value": 0.025, "basis": ["F3"],
             "rationale": "Kept in line with long-run nominal growth and well below the discount rate used."}],
        "scenarios": {"bear": {"value_per_share": 40, "prob": 0.25}, "base": {"value_per_share": 60, "prob": 0.5},
                      "bull": {"value_per_share": 80, "prob": 0.25}},
        "expected_value": 60, "methods": {"dcf": 60, "peer_multiples": 56}, "method_gap_note": ""},
    "risk": {
        "risks": [{"text": "Margin reverts to the 2023 level.", "downside_pct": 15},
                  {"text": "Revenue growth halves.", "downside_pct": 20},
                  {"text": "Refinancing at higher rates.", "downside_pct": 5}],
        "thesis_breakers": ["Operating margin below 14% for two consecutive quarters.", "Revenue growth under 4% for a fiscal year."],
        "change_my_mind": ["Cash conversion falling below net income.", "Debt rising while revenue slows."]},
}
HEAD = {"verdict": "buy", "position_pct": 10, "sector_pct": 20,
        "summary": ("Test Co has grown revenue at ten percent a year with widening margins. Cash flow exceeds reported profit "
                    "and debt is falling. At the current price the shares sit twenty percent below a conservative base value. "
                    "That clears the required margin of safety, so the verdict is buy at a ten percent position.")}

# Scripted flaws on a first draft: sub-dimension -> (part, how to break it)
DEFECTS = {
    "scenarios": ("valuation", lambda f: f.update(expected_value=75)),
    "peers_justified": ("peers", lambda f: f.update(peers=f["peers"][:3])),
    "thesis_breakers": ("risk", lambda f: f.update(thesis_breakers=["Things get worse."])),
    "downside_quantified": ("risk", lambda f: [r.update(downside_pct=None) for r in f["risks"]]),
}


class Mock:
    """Models with 'haiku' in the name start with four flaws and fix one per part per revision;
    others start with one and fix everything named. The judge is scripted as saturated (all 2s)."""

    def __init__(self):
        self.tokens = 0

    def complete(self, model, system, prompt, extra=None):
        self.tokens += (len(system) + len(prompt)) // 4
        if system == JUDGE:
            subs = json.loads(prompt.split("RUBRIC\n")[1].split("\n\nSTATEMENTS")[0])
            return json.dumps({d: {s: {"score": 2, "quote": "TESTCO", "reason": "looks fine"} for s in ss} for d, ss in subs.items()})
        if system == LEADSYS:
            return json.dumps(HEAD)
        if system == VERIFY:
            return json.dumps(json.loads(prompt.split("DRAFTS\n")[1])[0])
        part = prompt.split("PART: ")[1].split("\n")[0]
        small = "haiku" in model
        mine = [s for s, (p, _) in DEFECTS.items() if p == part and (small or s == "scenarios")]
        if "PREVIOUS\n" not in prompt:
            frag = copy.deepcopy(GOLD[part])
            for s in mine:
                DEFECTS[s][1](frag)
            return json.dumps(frag)
        frag = json.loads(prompt.split("PREVIOUS\n")[1].split("\nCRITIQUE")[0])
        named = [s for s in mine if s + ":" in prompt.split("CRITIQUE\n")[1]]
        for s in named[:1] if small else named:
            fixed = copy.deepcopy(GOLD[part])
            for other in named:
                if small and other != s:
                    DEFECTS[other][1](fixed)
            frag = fixed
        return json.dumps(frag)
