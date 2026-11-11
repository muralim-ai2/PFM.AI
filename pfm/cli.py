import argparse
import json
from pathlib import Path
import yaml
from . import db, edgar, statements, loop, bench, mock

ROOT = Path(__file__).resolve().parents[1]


def _cik(con, ticker):
    r = con.execute("select cik from company where ticker=?", (ticker.upper(),)).fetchone()
    if not r:
        raise SystemExit(f"{ticker} not ingested; run: pfm ingest {ticker}")
    return r[0]


def main():
    p = argparse.ArgumentParser(prog="pfm")
    p.add_argument("--db", default="pfm.db")
    p.add_argument("--mock", action="store_true", help="offline dry run on synthetic TESTCO with a scripted model")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ingest").add_argument("tickers", nargs="+")
    sub.add_parser("statements").add_argument("ticker")
    a = sub.add_parser("analyze")
    a.add_argument("ticker"); a.add_argument("--price", type=float, required=True); a.add_argument("--team", default="frontier")
    b = sub.add_parser("bench")
    b.add_argument("targets", nargs="+", help="TICKER:PRICE"); b.add_argument("--teams", nargs="+", default=["frontier", "swarm"])
    args = p.parse_args()

    con = db.connect(":memory:" if args.mock else args.db)
    cfg = yaml.safe_load((ROOT / "config/teams.yaml").read_text())
    if args.mock:
        statements.build(con, edgar.load(con, mock.companyfacts(), "TESTCO"))
        provider = mock.Mock()
    elif args.cmd in ("analyze", "bench"):
        from .agents.providers import Anthropic
        provider = Anthropic()

    if args.cmd == "ingest":
        for t in args.tickers:
            statements.build(con, cik := edgar.load(con, edgar.fetch(t), t))
            bad = [c for c in statements.checks(con, cik) if not c["ok"]]
            print(f"{t}: loaded, {len(bad)} tie-out failures {bad[:3]}")
    elif args.cmd == "statements":
        cik = _cik(con, args.ticker)
        print(json.dumps({"statements": statements.view(con, cik), "checks": statements.checks(con, cik)}, indent=1))
    elif args.cmd == "analyze":
        r = loop.run(con, _cik(con, args.ticker), args.ticker, args.price, args.team, cfg, provider)
        Path(f"{args.ticker}_memo.json").write_text(r.pop("memo").model_dump_json(indent=1))
        print(json.dumps(r, indent=1))
    elif args.cmd == "bench":
        targets = [(_cik(con, t), t, float(px)) for t, px in (x.split(":") for x in args.targets)]
        print(bench.table(bench.run(con, targets, args.teams, cfg, provider)))


if __name__ == "__main__":
    main()
