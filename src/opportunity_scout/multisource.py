import json
import time
from pathlib import Path

from opportunity_scout.batch import run_batch
from opportunity_scout.models import OpportunitySignal
from opportunity_scout.scoring import rank_opportunities
from opportunity_scout.stackexchange import search_stackexchange


COMMUNITY_SEARCHES = (
    ("bicycles", "replacement reflector bracket"),
    ("diy", "discontinued appliance knob"),
    ("mechanics", "broken interior trim clip"),
    ("outdoors", "replacement tent pole clip"),
)


def run_multisource() -> list[OpportunitySignal]:
    unique: dict[str, OpportunitySignal] = {
        str(signal.url): signal for signal in run_batch()
    }

    for site, query in COMMUNITY_SEARCHES:
        print(f"Searching Stack Exchange {site}: {query}")
        for signal in search_stackexchange(query, site):
            unique[str(signal.url)] = signal
        time.sleep(1)

    return rank_opportunities(list(unique.values()))


def main() -> None:
    results = run_multisource()
    output_path = Path("data/multisource_opportunities.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            [item.model_dump(mode="json") for item in results],
            indent=2,
        )
    )

    print(f"Saved {len(results)} unique results to {output_path}.")
    print("Top opportunities:")

    for item in results[:25]:
        print(
            f"{item.total_score:>4.1f}  "
            f"[{item.source}]  {item.title}"
        )


if __name__ == "__main__":
    main()
