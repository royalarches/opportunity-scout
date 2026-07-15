import re

from opportunity_scout.collector import fetch_page
from opportunity_scout.models import OpportunitySignal
from opportunity_scout.scoring import rank_opportunities
from opportunity_scout.scraper import extract_opportunity_links


HIGH_INTENT_PHRASES = (
    "can't find",
    "cannot find",
    "discontinued",
    "replacement",
    "missing part",
)

FAILURE_PHRASES = (
    "broken",
    "broke",
    "cracked",
    "snapped",
)

PRINTABLE_PART_WORDS = (
    "knob",
    "clip",
    "bracket",
    "cap",
    "cover",
    "holder",
    "hinge",
    "latch",
    "handle",
    "button",
    "adapter",
)

COMPLEX_CONTEXT_WORDS = (
    "battery",
    "screen",
    "display",
    "circuit",
    "board",
    "motherboard",
    "capacitor",
    "flex cable",
    "hard drive",
    "motor",
    "sensor",
    "camera",
    "antenna",
    "laptop",
    "smartphone",
)


def contains_term(text: str, terms: tuple[str, ...]) -> bool:
    return any(
        re.search(rf"\b{re.escape(term)}\b", text)
        for term in terms
    )


def add_initial_estimates(
    signal: OpportunitySignal,
) -> OpportunitySignal:
    title = signal.title.lower()
    demand = 5

    if contains_term(title, HIGH_INTENT_PHRASES):
        demand += 2
    elif contains_term(title, FAILURE_PHRASES):
        demand += 1

    printability = 5
    if contains_term(title, COMPLEX_CONTEXT_WORDS):
        printability = 3
    elif contains_term(title, PRINTABLE_PART_WORDS):
        printability = 9

    return signal.model_copy(
        update={
            "demand_score": min(demand, 10),
            "competition_score": 5,
            "printability_score": printability,
            "legal_risk_score": 3,
        }
    )


def scout_page(
    url: str,
    source: str,
) -> list[OpportunitySignal]:
    html = fetch_page(url)
    signals = extract_opportunity_links(
        html=html,
        page_url=url,
        source=source,
    )
    estimated = [add_initial_estimates(signal) for signal in signals]
    return rank_opportunities(estimated)
