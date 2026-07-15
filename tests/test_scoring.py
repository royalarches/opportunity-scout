from opportunity_scout.models import OpportunitySignal
from opportunity_scout.scoring import calculate_total


def test_calculate_total():
    signal = OpportunitySignal(
        source="test",
        title="Broken appliance knob",
        url="https://example.com",
        demand_score=8,
        competition_score=3,
        printability_score=9,
        legal_risk_score=2,
    )

    assert calculate_total(signal) == 8.1
