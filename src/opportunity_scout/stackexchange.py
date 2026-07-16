import html
import math

import httpx

from opportunity_scout.collector import USER_AGENT
from opportunity_scout.models import OpportunitySignal
from opportunity_scout.pipeline import add_initial_estimates
from opportunity_scout.scoring import rank_opportunities


API_URL = "https://api.stackexchange.com/2.3/search/advanced"


def search_stackexchange(
    query: str,
    site: str,
) -> list[OpportunitySignal]:
    response = httpx.get(
        API_URL,
        params={
            "q": query,
            "site": site,
            "pagesize": 30,
            "order": "desc",
            "sort": "relevance",
        },
        headers={"User-Agent": USER_AGENT},
        timeout=15,
        follow_redirects=True,
    )
    response.raise_for_status()

    signals: list[OpportunitySignal] = []

    for item in response.json().get("items", []):
        title = html.unescape(item["title"])
        signal = OpportunitySignal(
            source=f"stackexchange:{site}",
            title=title,
            url=item["link"],
            description="Tags: " + ", ".join(item.get("tags", [])),
        )
        estimated = add_initial_estimates(signal)

        views = item.get("view_count", 0)
        answers = item.get("answer_count", 0)
        demand = min(
            10,
            estimated.demand_score
            + math.log10(views + 1)
            + min(answers, 5) * 0.2,
        )
        signals.append(
            estimated.model_copy(
                update={"demand_score": round(demand, 2)}
            )
        )

    return rank_opportunities(signals)
