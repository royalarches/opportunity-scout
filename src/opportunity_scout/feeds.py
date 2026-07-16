import html
import xml.etree.ElementTree as ET

import httpx
from bs4 import BeautifulSoup

from opportunity_scout.collector import USER_AGENT
from opportunity_scout.models import OpportunitySignal
from opportunity_scout.pipeline import (
    FAILURE_PHRASES,
    HIGH_INTENT_PHRASES,
    PRINTABLE_PART_WORDS,
    add_initial_estimates,
    contains_term,
)
from opportunity_scout.scoring import rank_opportunities


OPPORTUNITY_TERMS = (
    HIGH_INTENT_PHRASES
    + FAILURE_PHRASES
    + PRINTABLE_PART_WORDS
)


def clean_text(value: str) -> str:
    return BeautifulSoup(
        html.unescape(value),
        "html.parser",
    ).get_text(" ", strip=True)


def parse_feed(
    xml_text: str,
    source: str,
) -> list[OpportunitySignal]:
    root = ET.fromstring(xml_text)
    signals: list[OpportunitySignal] = []

    for item in root.findall(".//item"):
        title = clean_text(item.findtext("title", ""))
        url = item.findtext("link", "").strip()
        description = clean_text(
            item.findtext("description", "")
        )

        if (
            title
            and url
            and contains_term(title.lower(), OPPORTUNITY_TERMS)
        ):
            signal = OpportunitySignal(
                source=source,
                title=title,
                url=url,
                description=description,
            )
            signals.append(add_initial_estimates(signal))

    for entry in root.findall(".//{*}entry"):
        title = clean_text(
            entry.findtext("{*}title", "")
        )
        link = entry.find("{*}link")
        url = link.get("href", "").strip() if link is not None else ""
        description = clean_text(
            entry.findtext("{*}summary", "")
        )

        if (
            title
            and url
            and contains_term(title.lower(), OPPORTUNITY_TERMS)
        ):
            signal = OpportunitySignal(
                source=source,
                title=title,
                url=url,
                description=description,
            )
            signals.append(add_initial_estimates(signal))

    return rank_opportunities(signals)


def search_feed(
    url: str,
    source: str,
) -> list[OpportunitySignal]:
    response = httpx.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=15,
        follow_redirects=True,
    )
    response.raise_for_status()
    content_type = response.headers.get("content-type", "").lower()
    if "xml" not in content_type and "rss" not in content_type:
        raise RuntimeError(
            "Feed unavailable: the site returned non-feed content."
        )
    return parse_feed(response.text, source)
