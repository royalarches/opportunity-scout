from opportunity_scout.models import OpportunitySignal


def calculate_total(signal: OpportunitySignal) -> float:
    demand = min(max(signal.demand_score, 0), 10)
    competition = min(max(signal.competition_score, 0), 10)
    printability = min(max(signal.printability_score, 0), 10)
    legal_risk = min(max(signal.legal_risk_score, 0), 10)   
    safety_risk = min(max(signal.safety_risk_score, 0), 10)

    total = (
        demand * 0.35
        + (10 - competition) * 0.15
        + printability * 0.25
        + (10 - legal_risk) * 0.10
        + (10 - safety_risk) * 0.15
    )
    return round(total, 2)


def rank_opportunities(
    signals: list[OpportunitySignal],
) -> list[OpportunitySignal]:
    scored = [
        signal.model_copy(
            update={"total_score": calculate_total(signal)}
        )
        for signal in signals
    ]
    return sorted(scored, key=lambda item: item.total_score, reverse=True)
