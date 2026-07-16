from opportunity_scout.models import OpportunitySignal
from opportunity_scout.pipeline import add_initial_estimates


def make_signal(title: str, suffix: str) -> OpportunitySignal:
    return OpportunitySignal(
        source="test",
        title=title,
        url=f"https://example.com/{suffix}",
    )


def test_printable_terms_match_whole_words_only():
    cap = add_initial_estimates(make_signal("Missing cap", "cap"))
    capacitors = add_initial_estimates(
        make_signal("Missing capacitors", "capacitors")
    )

    assert cap.printability_score == 9
    assert capacitors.printability_score == 5


def test_complex_context_overrides_printable_part_word():
    signal = add_initial_estimates(
        make_signal("Broken clip on motherboard", "motherboard")
    )

    assert signal.printability_score == 3


def test_safety_critical_parts_are_penalized():
    signal = add_initial_estimates(
        make_signal("Broken bottom bracket", "bottom-bracket")
    )

    assert signal.printability_score == 1
    assert signal.safety_risk_score == 9
