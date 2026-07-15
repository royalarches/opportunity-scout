from urllib.parse import urljoin

from bs4 import BeautifulSoup

from opportunity_scout.models import OpportunitySignal


NEED_KEYWORDS = (
    "broken",
    "broke",
    "replacement",
    "can't find",
    "cannot find",
    "discontinued",
    "repair",
    "missing part",
)


def extract_opportunity_links(
    html: str,
    page_url: str,
    source: str,
) -> list[OpportunitySignal]:
    soup = BeautifulSoup(html, "html.parser")
    signals: list[OpportunitySignal] = []
    seen_urls: set[str] = set()

    for link in soup.find_all("a", href=True):
        title = link.get_text(" ", strip=True)
        title_lower = title.lower()

        if not title or not any(word in title_lower for word in NEED_KEYWORDS):
            continue

        url = urljoin(page_url, link["href"])
        if url in seen_urls:
            continue

        seen_urls.add(url)
        signals.append(
            OpportunitySignal(
                source=source,
                title=title,
                url=url,
            )
        )

    return signals
