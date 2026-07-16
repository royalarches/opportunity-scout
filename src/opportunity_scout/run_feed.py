import argparse
import json
from pathlib import Path

import httpx

from opportunity_scout.feeds import search_feed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search an RSS or Atom feed for part opportunities."
    )
    parser.add_argument("url", help="Public RSS or Atom feed URL")
    parser.add_argument(
        "--source",
        required=True,
        help="Short source name, such as camper-forum",
    )
    parser.add_argument(
        "--output",
        default="data/feed_opportunities.json",
        help="Where to save the ranked results",
    )
    args = parser.parse_args()

    try:
        results = search_feed(args.url, args.source)
    except httpx.HTTPStatusError as error:
        parser.error(
            f"feed returned HTTP {error.response.status_code}"
        )
    except RuntimeError as error:
        parser.error(str(error))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            [item.model_dump(mode="json") for item in results],
            indent=2,
        )
    )

    print(f"Found {len(results)} opportunities.")
    print(f"Saved results to {output_path}.")

    for item in results:
        print(f"{item.total_score:>4.1f}  {item.title}")


if __name__ == "__main__":
    main()
