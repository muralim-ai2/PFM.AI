"""Structured investment memo. Agents must emit this shape so code can judge it."""
from typing import Literal
from pydantic import BaseModel


class Figure(BaseModel):
    id: str                       # F1, F2...
    label: str
    value: float
    item: str | None = None       # reported: statement item + period
    period_end: str | None = None
    period_type: Literal["FY", "Q"] | None = None
    audited: bool | None = None
    expr: str | None = None       # computed: arithmetic over figure ids, e.g. "F1 / F2"


class Source(BaseModel):
    ref: str                      # filing accession number or URL
    publisher: str = ""


class Claim(BaseModel):
    id: str                       # C1, C2...
    text: str
    kind: Literal["fact", "inference", "conclusion"]
    supports: list[str] = []      # claim or figure ids this rests on
    sources: list[Source] = []


class Assumption(BaseModel):
    name: str                     # revenue_growth, operating_margin, wacc, terminal_growth
    value: float
    rationale: str
    basis: list[str] = []         # figure ids


class Scenario(BaseModel):
    value_per_share: float
    prob: float


class Risk(BaseModel):
    text: str
    downside_pct: float | None = None


class Work(BaseModel):
    agent: str
    part: str
    output_hash: str
    vetted_by: str = ""
    vetted_hash: str = ""


# Which memo fields each worker part owns. The lead owns the rest.
PARTS = {
    "analysis": ["figures", "claims", "analysis"],
    "peers": ["peers"],
    "valuation": ["assumptions", "scenarios", "expected_value", "methods", "method_gap_note"],
    "risk": ["risks", "thesis_breakers", "change_my_mind"],
}
LEAD = ["verdict", "summary", "position_pct", "sector_pct"]


def part_hash(memo, part):
    """Hash of a part's content, so code can prove the vetted text is the text in the memo."""
    import hashlib
    import json
    d = memo.model_dump(include=set(PARTS[part]))
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()[:16]


class Memo(BaseModel):
    ticker: str
    price: float
    verdict: Literal["buy", "hold", "avoid"]
    summary: str
    figures: list[Figure] = []
    claims: list[Claim] = []
    analysis: dict[str, str] = {}             # section -> text citing figures as [F1]
    peers: list[dict] = []                    # {ticker, reason}
    assumptions: list[Assumption] = []
    scenarios: dict[str, Scenario] = {}       # bear, base, bull
    expected_value: float | None = None
    methods: dict[str, float] = {}            # method -> value per share
    method_gap_note: str = ""
    risks: list[Risk] = []
    thesis_breakers: list[str] = []
    change_my_mind: list[str] = []
    position_pct: float = 0
    sector_pct: float = 0
    uses_margin: bool = False
    work: list[Work] = []
