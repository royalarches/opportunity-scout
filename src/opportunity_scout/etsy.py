import html
import math
import os

import httpx
from dotenv import load_dotenv

from opportunity_scout.models import OpportunitySignal
from opportunity_scout.pipeline import add_initial_estimates
from opportunity_scout.scoring import rank_opportunities


SEARCH_URL = "https://openapi.etsy.com/v3/application/listings/active"


def format_price(price: dict) -> str:
    amount = price.get("amount", 0)
    divisor = price.get("divisor", 100) or 100
    currency = price.get("currency_code", "")
    return f"{amount / divisor:.2f} {currency}".strip()


def search_etsy(query: str) -> list[OpportunitySignal]:
    load_dotenv()

    api_key = os.getenv("ETSY_API_KEY", "")
    shared_secret = os.getenv("ETSY_SHARED_SECRET", "")

    if not api_key or not shared_secret:
        raise RuntimeError(
            "Add ETSY_API_KEY and ETSY_SHARED_SECRET to .env."
        )

    response = httpx.get(
        SEARCH_URL,
        params={
            "keywords": query,
            "limit": 25,
            "sort_on": "score",
            "sort_order": "desc",
        },
        headers={
            "x-api-key": f"{api_key}:{shared_secret}",
        },
        timeout=15,
        follow_redirects=True,
    )
    response.raise_for_status()
    payload = response.json()

    total_listings = payload.get("count", 0)
    competition = min(
        10,
        round(math.log10(total_listings + 1) * 2.5, 2),
    )
    signals: list[OpportunitySignal] = []

    for listing in payload.get("results", []):
        title = html.unescape(listing["title"])
        description = (
            f"Active listing; price "
            f"{format_price(listing.get('price', {}))}; "
            f"{total_listings} matching active listings."
        )
        signal = OpportunitySignal(
            source="etsy",
            title=title,
            url=listing["url"],
            description=description,
        )
        estimated = add_initial_estimates(signal)
        signals.append(
            estimated.model_copy(
                update={"competition_score": competition}
            )
        )

    return rank_opportunities(signals)
