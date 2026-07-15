import json
import time
from pathlib import Path

from opportunity_scout.ifixit import search_ifixit
from opportunity_scout.models import OpportunitySignal
from opportunity_scout.scoring import rank_opportunities


SEARCH_QUERIES = (
    "broken knob",
    "broken clip",
    "broken hinge",
    "replacement bracket",
    "discontinued handle",
    "missing cap",
)


def run_batch() -> list[OpportunitySignal]:
    unique: dict[str, OpportunitySignal] = {}

    for query in SEARCH_QUERIES:
        print(f"Searching: {query}")
        for signal in search_ifixit(query):
            unique[str(signal.url)] = signal
        time.sleep(1)

    return rank_opportunities(list(unique.values()))


def main() -> None:
    results = run_batch()
    output_path = Path("data/batch_opportunities.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            [item.model_dump(mode="json") for item in results],
            indent=2,
        )
    )

    print(f"Saved {len(results)} unique results to {output_path}.")
    print("Top opportunities:")

    for item in results[:20]:
        print(f"{item.total_score:>4.1f}  {item.title}")


if __name__ == "__main__":
    main()
