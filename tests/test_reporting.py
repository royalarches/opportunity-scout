import csv

from opportunity_scout.models import OpportunitySignal
from opportunity_scout.reporting import write_csv_report


def test_write_csv_report(tmp_path):
    signal = OpportunitySignal(
        source="test",
        title="Replacement camper latch",
        url="https://example.com/part",
        total_score=8.2,
    )
    output_path = write_csv_report([signal], tmp_path / "report.csv")

    with output_path.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["title"] == "Replacement camper latch"
    assert rows[0]["total_score"] == "8.2"
