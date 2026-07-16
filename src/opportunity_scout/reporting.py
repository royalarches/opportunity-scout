import csv
from pathlib import Path

from opportunity_scout.models import OpportunitySignal


REPORT_COLUMNS = (
    "total_score",
    "source",
    "title",
    "url",
    "demand_score",
    "competition_score",
    "printability_score",
    "safety_risk_score",
    "legal_risk_score",
    "description",
    "observed_at",
)


def write_csv_report(
    signals: list[OpportunitySignal],
    output: str | Path,
) -> Path:
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=REPORT_COLUMNS)
        writer.writeheader()

        for signal in signals:
            writer.writerow(
                {
                    "total_score": signal.total_score,
                    "source": signal.source,
                    "title": signal.title,
                    "url": str(signal.url),
                    "demand_score": signal.demand_score,
                    "competition_score": signal.competition_score,
                    "printability_score": signal.printability_score,
                    "safety_risk_score": signal.safety_risk_score,
                    "legal_risk_score": signal.legal_risk_score,
                    "description": signal.description,
                    "observed_at": signal.observed_at.isoformat(),
                }
            )

    return output_path
