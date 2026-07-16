import argparse
import json
from pathlib import Path

import httpx

from opportunity_scout.ebay import search_ebay
from opportunity_scout.etsy import search_etsy


SEARCHERS = {
    "ebay": search_ebay,
    "etsy": search_etsy,
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check marketplace competition for a part."
    )
    parser.add_argument(
        "source",
        choices=SEARCHERS,
        help="Marketplace to search",
    )
    parser.add_argument(
        "query",
        help='Search phrase, such as "replacement knob"',
    )
    parser.add_argument(
        "--output",
        help="Optional custom JSON output path",
    )
    args = parser.parse_args()

    try:
        results = SEARCHERS[args.source](args.query)
    except RuntimeError as error:
        parser.error(str(error))
    except httpx.HTTPStatusError as error:
        status = error.response.status_code
        parser.error(
            f"{args.source} returned HTTP {status}; "
            "the API credentials may still be pending approval."
        )

    output_path = Path(
        args.output
        or f"data/{args.source}_opportunities.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            [item.model_dump(mode="json") for item in results],
            indent=2,
        )
    )

    print(f"Found {len(results)} active listings.")
    print(f"Saved results to {output_path}.")

    for item in results:
        print(f"{item.total_score:>4.1f}  {item.title}")


if __name__ == "__main__":
    main()
