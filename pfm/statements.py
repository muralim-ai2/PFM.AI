"""Standardized statements: 3 audited fiscal years + unaudited interim quarters, with tie-out checks."""
from collections import defaultdict
from datetime import date

# item -> (kind, candidate us-gaap tags in priority order)
MAP = {
    "Revenue": ("flow", ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"]),
    "CostOfRevenue": ("flow", ["CostOfGoodsAndServicesSold", "CostOfRevenue"]),
    "GrossProfit": ("flow", ["GrossProfit"]),
    "OperatingIncome": ("flow", ["OperatingIncomeLoss"]),
    "InterestExpense": ("flow", ["InterestExpense", "InterestExpenseNonoperating"]),
    "NetIncome": ("flow", ["NetIncomeLoss"]),
    "CFO": ("flow", ["NetCashProvidedByUsedInOperatingActivities"]),
    "CFI": ("flow", ["NetCashProvidedByUsedInInvestingActivities"]),
    "CFF": ("flow", ["NetCashProvidedByUsedInFinancingActivities"]),
    "FXOnCash": ("flow", ["EffectOfExchangeRateOnCashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]),
    "Capex": ("flow", ["PaymentsToAcquirePropertyPlantAndEquipment"]),
    "NetChangeInCash": ("flow", ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsPeriodIncreaseDecreaseIncludingExchangeRateEffect",
                                 "CashAndCashEquivalentsPeriodIncreaseDecrease"]),
    "Assets": ("stock", ["Assets"]),
    "Liabilities": ("stock", ["Liabilities"]),
    "Equity": ("stock", ["StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest", "StockholdersEquity"]),
    "LiabilitiesAndEquity": ("stock", ["LiabilitiesAndStockholdersEquity"]),
    "Cash": ("stock", ["CashAndCashEquivalentsAtCarryingValue"]),
    "Debt": ("stock", ["LongTermDebt", "LongTermDebtNoncurrent"]),
}


def _days(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


def build(con, cik):
    """Rebuild statement_line. Latest filing wins per period; quarters missing from filings
    (Q4, and cash-flow Q2/Q3) are derived by differencing year-to-date figures and flagged."""
    con.execute("delete from statement_line where cik=?", (cik,))
    for item, (kind, tags) in MAP.items():
        rows = next((r for t in tags if (r := con.execute(
            "select start,end,value,form,accn from fact where cik=? and tag=? order by filed", (cik, t)).fetchall())), [])
        out = {}  # (end, type) -> (value, audited, derived, accn)
        if kind == "stock":
            annual = {r[1] for r in rows if r[3].startswith("10-K")}
            for _, e, v, _, accn in rows:
                out[(e, "FY" if e in annual else "Q")] = (v, int(e in annual), 0, accn)
        else:
            cum = defaultdict(dict)
            for s, e, v, _, accn in rows:
                cum[s][e] = (v, accn)
            for s, ends in cum.items():
                prev_e = prev_v = None
                for e in sorted(ends):
                    v, accn = ends[e]
                    d = _days(s, e)
                    if 350 <= d <= 380:
                        out[(e, "FY")] = (v, 1, 0, accn)
                    if prev_e is None and 80 <= d <= 100:
                        out[(e, "Q")] = (v, 0, 0, accn)
                    elif prev_e and 80 <= _days(prev_e, e) <= 100:
                        out.setdefault((e, "Q"), (v - prev_v, 0, 1, accn))
                    prev_e, prev_v = e, v
        con.executemany("insert or replace into statement_line values(?,?,?,?,?,?,?,?)",
                        [(cik, item, e, t, *vals) for (e, t), vals in out.items()])
    con.commit()


def _val(con, cik, item, end, ptype):
    r = con.execute("select value from statement_line where cik=? and item=? and period_end=? and period_type=?",
                    (cik, item, end, ptype)).fetchone()
    return r[0] if r else None


def checks(con, cik, tol=0.005):
    """Tie-outs: assets = liabilities + equity; operating + investing + financing (+ FX) = change in cash."""
    res = []
    for end, pt in con.execute("select period_end, period_type from statement_line where cik=? and item='Assets'", (cik,)):
        a = _val(con, cik, "Assets", end, pt)
        le = _val(con, cik, "LiabilitiesAndEquity", end, pt)
        if le is None:
            l, q = _val(con, cik, "Liabilities", end, pt), _val(con, cik, "Equity", end, pt)
            le = l + q if None not in (l, q) else None
        if le is not None:
            res.append({"period": end, "check": "balance", "ok": abs(a - le) <= tol * abs(a)})
    for (end,) in con.execute("select period_end from statement_line where cik=? and item='NetChangeInCash' and period_type='FY'", (cik,)):
        parts = [_val(con, cik, i, end, "FY") for i in ("CFO", "CFI", "CFF")]
        if None not in parts:
            total = sum(parts) + (_val(con, cik, "FXOnCash", end, "FY") or 0)
            chg = _val(con, cik, "NetChangeInCash", end, "FY")
            res.append({"period": end, "check": "cash", "ok": abs(total - chg) <= tol * max(abs(chg), 1)})
    return res


def view(con, cik, years=3):
    """Last `years` fiscal years plus every interim quarter after the latest year end."""
    fy = [r[0] for r in con.execute("select distinct period_end from statement_line where cik=? and period_type='FY' "
                                    "and item='Revenue' order by period_end desc limit ?", (cik, years))]
    out = {"annual_audited": {}, "interim_unaudited": {}}
    for item, end, pt, v, derived in con.execute(
            "select item, period_end, period_type, value, derived from statement_line where cik=?", (cik,)):
        if pt == "FY" and end in fy:
            out["annual_audited"].setdefault(end, {})[item] = v
        elif pt == "Q" and fy and end > fy[0]:
            out["interim_unaudited"].setdefault(end, {})[item] = v
    return out
