"""Benchmark team shapes: attempts needed to pass both judges, score per attempt, tokens, time."""
from . import loop


def run(con, targets, team_names, cfg, provider):
    """targets: [(cik, ticker, price)]"""
    return [loop.run(con, cik, t, price, team, cfg, provider) for team in team_names for cik, t, price in targets]


def table(rows):
    out = ["| team | ticker | passed | attempts | final score by attempt | judge inflation | tokens | seconds |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        traj = " -> ".join(f"{t['overall']:.2f}" for t in r["trajectory"])
        out.append(f"| {r['team']} | {r['ticker']} | {'yes' if r['passed'] else 'no'} | {r['attempts']} | {traj} | "
                   f"{r['judge_inflation']:+.2f} | {r['tokens']:,} | {r['seconds']} |")
    return "\n".join(out)
