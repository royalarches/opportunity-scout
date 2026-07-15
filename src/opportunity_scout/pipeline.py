from opportunity_scout.collector import fetch_page
from opportunity_scout.models import OpportunitySignal
from opportunity_scout.scoring import rank_opportunities
from opportunity_scout.scraper import extract_opportunity_links


DEMAND_PHRASES = (
    "can't find",
    "cannot find",
    "discontinued",
    "replacement",
    "missing part",
    "broken",
    "broke",
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

COMPLEX_PART_WORDS = (
    "battery",
    "screen",
    "display",
    "circuit",
    "motor",
    "sensor",
    "camera",
    "antenna",
)


def add_initial_estimates(
    signal: OpportunitySignal,
) -> OpportunitySignal:
    title = signal.title.lower()
    demand = 5

    for phrase in DEMAND_PHRASES:
        if phrase in title:
            demand += 1

    printability = 5
    if any(word in title for word in PRINTABLE_PART_WORDS):
        printability = 9
    elif any(word in title for word in COMPLEX_PART_WORDS):
        printability = 3

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
