from urllib.parse import quote

import httpx

from opportunity_scout.collector import USER_AGENT
from opportunity_scout.models import OpportunitySignal
from opportunity_scout.pipeline import add_initial_estimates
from opportunity_scout.scoring import rank_opportunities


API_BASE = "https://www.ifixit.com/api/2.0"


def search_ifixit(query: str) -> list[OpportunitySignal]:
    encoded_query = quote(query, safe="")
    response = httpx.get(
        f"{API_BASE}/suggest/{encoded_query}",
        params={"doctypes": "question,guide"},
        headers={"User-Agent": USER_AGENT},
        timeout=15,
        follow_redirects=True,
    )
    response.raise_for_status()

    signals: list[OpportunitySignal] = []

    for result in response.json().get("results", []):
        title = result.get("title") or result.get("display_title")
        url = result.get("url")

        if not title or not url:
            continue

        signal = OpportunitySignal(
            source="ifixit",
            title=title,
            url=url,
            description=result.get("summary", ""),
        )
        signals.append(add_initial_estimates(signal))

    return rank_opportunities(signals)
