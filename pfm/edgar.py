"""SEC EDGAR companyfacts -> fact table. SEC requires a descriptive User-Agent with contact email."""
import os
import httpx


def _get(url):
    ua = os.environ["SEC_USER_AGENT"]  # e.g. "PFM.AI you@example.com"
    return httpx.get(url, headers={"User-Agent": ua}, timeout=60).raise_for_status().json()


def cik_for(ticker):
    rows = _get("https://www.sec.gov/files/company_tickers.json").values()
    return next(r["cik_str"] for r in rows if r["ticker"] == ticker.upper())


def fetch(ticker):
    return _get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_for(ticker):010d}.json")


def load(con, data, ticker):
    cik = int(data["cik"])
    con.execute("insert or replace into company values(?,?,?)", (cik, ticker.upper(), data["entityName"]))
    con.execute("delete from fact where cik=?", (cik,))
    rows = [(cik, tag, unit, r.get("start"), r["end"], r["val"], r["form"], r.get("fy"), r.get("fp"), r["filed"], r["accn"])
            for tag, body in data["facts"].get("us-gaap", {}).items()
            for unit, rs in body["units"].items() for r in rs if r["form"][:4] in ("10-K", "10-Q")]
    con.executemany("insert into fact values(?,?,?,?,?,?,?,?,?,?,?)", rows)
    con.commit()
    return cik
