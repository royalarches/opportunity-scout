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
        params={"doctypes": "question"},
        headers={"User-Agent": USER_AGENT},
        timeout=15,
        follow_redirects=True,
    )
    response.raise_for_status()

    signals: list[OpportunitySignal] = []

    for result in response.json().get("results", []):
        if result.get("dataType") != "question":
            continue

        title = result.get("title") or result.get("display_title")
        url = result.get("url")

        if not title or not url:
            continue

        topic = result.get("topic", "").strip()
        display_title = f"{topic}: {title}" if topic else title
        answer_count = result.get("answer_count", 0)
        accepted_answer = result.get("accepted_answerid")
        description = result.get("raw_text") or result.get("text", "")

        signal = OpportunitySignal(
            source="ifixit",
            title=display_title,
            url=url,
            description=description,
        )
        estimated = add_initial_estimates(signal)
        demand = estimated.demand_score
        if answer_count == 0:
            demand += 2
        elif not accepted_answer:
            demand += 1

        signals.append(
            estimated.model_copy(
                update={"demand_score": min(demand, 10)}
            )
        )

    return rank_opportunities(signals)
