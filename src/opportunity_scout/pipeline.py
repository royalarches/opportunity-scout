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


def add_initial_estimates(
    signal: OpportunitySignal,
) -> OpportunitySignal:
    title = signal.title.lower()
    demand = 5

    for phrase in HIGH_INTENT_PHRASES:
        if phrase in title:
            demand += 1

    return signal.model_copy(
        update={
            "demand_score": min(demand, 10),
            "competition_score": 5,
            "printability_score": 5,
            "legal_risk_score": 5,
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
