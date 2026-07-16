import math
import os

import httpx
from dotenv import load_dotenv

from opportunity_scout.models import OpportunitySignal
from opportunity_scout.pipeline import add_initial_estimates
from opportunity_scout.scoring import rank_opportunities


TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
SEARCH_URL = (
    "https://api.ebay.com/buy/browse/v1/item_summary/search"
)
SCOPE = "https://api.ebay.com/oauth/api_scope"


def get_application_token(
    client_id: str,
    client_secret: str,
) -> str:
    response = httpx.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "scope": SCOPE,
        },
        auth=(client_id, client_secret),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=15,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def search_ebay(query: str) -> list[OpportunitySignal]:
    load_dotenv()

    client_id = os.getenv("EBAY_CLIENT_ID", "")
    client_secret = os.getenv("EBAY_CLIENT_SECRET", "")
    marketplace = os.getenv("EBAY_MARKETPLACE_ID", "EBAY_US")

    if not client_id or not client_secret:
        raise RuntimeError(
            "Add EBAY_CLIENT_ID and EBAY_CLIENT_SECRET to .env."
        )

    token = get_application_token(client_id, client_secret)
    response = httpx.get(
        SEARCH_URL,
        params={"q": query, "limit": 25},
        headers={
            "Authorization": f"Bearer {token}",
            "X-EBAY-C-MARKETPLACE-ID": marketplace,
        },
        timeout=15,
        follow_redirects=True,
    )
    response.raise_for_status()
    payload = response.json()

    total_listings = payload.get("total", 0)
    competition = min(
        10,
        round(math.log10(total_listings + 1) * 2.5, 2),
    )
    signals: list[OpportunitySignal] = []

    for item in payload.get("itemSummaries", []):
        price = item.get("price", {})
        description = (
            f"Active listing; price "
            f"{price.get('value', 'unknown')} "
            f"{price.get('currency', '')}; "
            f"{total_listings} matching active listings."
        )
        signal = OpportunitySignal(
            source="ebay",
            title=item["title"],
            url=item["itemWebUrl"],
            description=description,
        )
        estimated = add_initial_estimates(signal)
        signals.append(
            estimated.model_copy(
                update={"competition_score": competition}
            )
        )

    return rank_opportunities(signals)
