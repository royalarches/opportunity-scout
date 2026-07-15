from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

import httpx


USER_AGENT = "OpportunityScout/0.1 (personal research project)"


def robots_url_for(url: str) -> str:
    parts = urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}/robots.txt"


def is_allowed(url: str) -> bool:
    robots_url = robots_url_for(url)

    try:
        response = httpx.get(
            robots_url,
            headers={"User-Agent": USER_AGENT},
            timeout=10,
            follow_redirects=True,
        )
        response.raise_for_status()
    except httpx.HTTPError:
        return False

    parser = RobotFileParser()
    parser.set_url(robots_url)
    parser.parse(response.text.splitlines())
    return parser.can_fetch(USER_AGENT, url)


def fetch_page(url: str) -> str:
    if not is_allowed(url):
        raise PermissionError(
            f"Collection is not allowed or robots.txt could not be verified: {url}"
        )

    response = httpx.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=15,
        follow_redirects=True,
    )
    response.raise_for_status()
    return response.text
