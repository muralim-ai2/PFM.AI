import sqlite3

SCHEMA = """
create table if not exists company(cik integer primary key, ticker text, name text);
create table if not exists fact(cik int, tag text, unit text, start text, end text, value real,
  form text, fy int, fp text, filed text, accn text);
create index if not exists fact_ix on fact(cik, tag);
create table if not exists statement_line(cik int, item text, period_end text, period_type text,
  value real, audited int, derived int, accn text, primary key(cik, item, period_end, period_type));
create table if not exists run(id integer primary key, ticker text, team text, attempts int,
  passed int, tokens int, seconds real, created text default current_timestamp);
create table if not exists memo(id integer primary key, run_id int, attempt int, json text);
create table if not exists eval_score(memo_id int, judge text, dimension text, sub text,
  score real, evidence text);
"""


def connect(path="pfm.db"):
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    return con
