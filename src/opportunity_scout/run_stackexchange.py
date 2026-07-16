import argparse
import json
from pathlib import Path

from opportunity_scout.stackexchange import search_stackexchange


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Search Stack Exchange for spare-part opportunities."
    )
    parser.add_argument(
        "query",
        help='Search phrase, such as "broken knob"',
    )
    parser.add_argument(
        "--site",
        default="bicycles",
        help="Stack Exchange site name, such as bicycles or diy",
    )
    parser.add_argument(
        "--output",
        default="data/stackexchange_opportunities.json",
        help="Where to save the ranked results",
    )
    args = parser.parse_args()

    results = search_stackexchange(args.query, args.site)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            [item.model_dump(mode="json") for item in results],
            indent=2,
        )
    )

    print(f"Found {len(results)} results.")
    print(f"Saved results to {output_path}.")

    for item in results:
        print(f"{item.total_score:>4.1f}  {item.title}")


if __name__ == "__main__":
    main()
