"""Tests for parse-time tag replacement."""

from bs4 import BeautifulSoup, SoupReplacer


class TestSoupReplacer:
    def test_nested_tags_are_renamed_during_parsing(self):
        html = '<div><b class="someclassname">content1<b>content2</b></b></div>'
        soup = BeautifulSoup(
            html, "html.parser", replacer=SoupReplacer("b", "blockquote")
        )

        assert soup.find("b") is None
        quotes = soup.find_all("blockquote")
        assert len(quotes) == 2
        assert quotes[0]["class"] == ["someclassname"]
        assert quotes[0].find("blockquote").get_text() == "content2"
        assert quotes[0].get_text() == "content1content2"

    def test_other_tags_and_default_parse_stay_unchanged(self):
        html = "<div><p>keep</p><b>change</b></div>"

        plain = BeautifulSoup(html, "html.parser")
        assert plain.b.get_text() == "change"
        assert plain.find("blockquote") is None
        assert plain.p.get_text() == "keep"

        soup = BeautifulSoup(
            html, "html.parser", replacer=SoupReplacer("b", "blockquote")
        )
        assert soup.find("b") is None
        assert soup.blockquote.get_text() == "change"
        assert soup.p.get_text() == "keep"
        assert soup.div is not None
