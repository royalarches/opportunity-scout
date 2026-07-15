import argparse
import json
from pathlib import Path

from opportunity_scout.pipeline import scout_page


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find and rank spare-part opportunity signals."
    )
    parser.add_argument("url", help="Public page to examine")
    parser.add_argument(
        "--source",
        default="web",
        help="Short source name, such as forum or marketplace",
    )
    parser.add_argument(
        "--output",
        default="data/opportunities.json",
        help="Where to save the results",
    )
    args = parser.parse_args()

    results = scout_page(args.url, args.source)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            [item.model_dump(mode="json") for item in results],
            indent=2,
        )
    )

    print(f"Found {len(results)} opportunity signals.")
    print(f"Saved results to {output_path}.")

    for item in results[:10]:
        print(f"{item.total_score:>4.1f}  {item.title}")


if __name__ == "__main__":
    main()
