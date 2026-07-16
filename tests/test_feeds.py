from opportunity_scout.feeds import parse_feed


def test_parse_rss_keeps_repair_opportunities():
    xml_text = """
    <rss>
      <channel>
        <item>
          <title>Broken camper cabinet latch</title>
          <link>https://example.com/posts/latch</link>
          <description>&lt;p&gt;Cannot find a replacement.&lt;/p&gt;</description>
        </item>
        <item>
          <title>Favorite camping recipes</title>
          <link>https://example.com/posts/recipes</link>
          <description>Food discussion</description>
        </item>
      </channel>
    </rss>
    """

    results = parse_feed(xml_text, "test-feed")

    assert len(results) == 1
    assert results[0].title == "Broken camper cabinet latch"
    assert results[0].source == "test-feed"


def test_parse_atom_keeps_repair_opportunities():
    xml_text = """
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry>
        <title>Missing motorcycle side cover</title>
        <link href="https://example.com/posts/cover"/>
        <summary>Looking for a replacement part.</summary>
      </entry>
    </feed>
    """

    results = parse_feed(xml_text, "test-atom")

    assert len(results) == 1
    assert results[0].title == "Missing motorcycle side cover"
