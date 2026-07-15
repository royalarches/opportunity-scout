from opportunity_scout.scraper import extract_opportunity_links


def test_extracts_only_opportunity_links():
    html = """
    <a href="/post/1">Broken blender knob</a>
    <a href="/post/2">Favorite recipes</a>
    <a href="/post/1">Broken blender knob</a>
    """

    results = extract_opportunity_links(
        html=html,
        page_url="https://example.com/forum/",
        source="test",
    )

    assert len(results) == 1
    assert results[0].title == "Broken blender knob"
    assert str(results[0].url) == "https://example.com/post/1"
