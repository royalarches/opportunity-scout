import httpx

from opportunity_scout.ifixit import search_ifixit


def test_ifixit_keeps_questions_and_prioritizes_unanswered(monkeypatch):
    payload = {
        "results": [
            {
                "dataType": "question",
                "title": "Where can I find a replacement battery cover?",
                "topic": "Example Keyboard",
                "url": "https://example.com/question",
                "answer_count": 0,
                "accepted_answerid": None,
                "raw_text": "The original cover is missing.",
            },
            {
                "dataType": "guide",
                "title": "Battery Cover Replacement",
                "topic": "Example Camera",
                "url": "https://example.com/guide",
            },
        ]
    }
    response = httpx.Response(
        200,
        json=payload,
        request=httpx.Request("GET", "https://example.com"),
    )
    monkeypatch.setattr(httpx, "get", lambda *args, **kwargs: response)

    results = search_ifixit("replacement battery cover")

    assert len(results) == 1
    assert results[0].title.startswith("Example Keyboard:")
    assert results[0].demand_score == 9
