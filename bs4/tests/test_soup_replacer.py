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


def b_to_blockquote(tag):
    return "blockquote" if tag.name == "b" else tag.name


class TestSoupReplacerTransformers:
    HTML = (
        '<div class="box" id="d">'
        "<b>content1<b>content2</b></b>after"
        '<p class="old" id="first">keep</p>'
        "<p>second</p>"
        "<i>also</i>"
        '<a href="/y">link</a>'
        '<span class="s">y</span>'
        "</div>"
        "<blockquote><b>inner</b>outer</blockquote>"
    )

    def test_name_xformer_renames_nested_tags(self):
        soup = BeautifulSoup(
            self.HTML, "html.parser", replacer=SoupReplacer(name_xformer=b_to_blockquote)
        )

        assert soup.find("b") is None
        outer = soup.div.blockquote
        assert outer.get_text() == "content1content2"
        assert outer.blockquote.get_text() == "content2"
        assert outer.next_sibling == "after"

    def test_name_xformer_leaves_other_tags_alone(self):
        soup = BeautifulSoup(
            self.HTML, "html.parser", replacer=SoupReplacer(name_xformer=b_to_blockquote)
        )

        assert soup.div["class"] == ["box"]
        assert soup.p["id"] == "first"
        assert soup.p.get_text() == "keep"
        assert soup.i.get_text() == "also"
        assert soup.a["href"] == "/y"

    def test_attrs_xformer_replaces_attributes(self):
        def set_test_class(tag):
            if tag.name == "p":
                return {"class": "test"}
            return tag.attrs

        soup = BeautifulSoup(
            self.HTML, "html.parser", replacer=SoupReplacer(attrs_xformer=set_test_class)
        )

        paragraphs = soup.find_all("p")
        assert len(paragraphs) == 2
        assert [p.attrs for p in paragraphs] == [{"class": "test"}, {"class": "test"}]

    def test_attrs_xformer_leaves_other_tags_unchanged(self):
        def drop_p_attrs(tag):
            return {} if tag.name == "p" else tag.attrs

        soup = BeautifulSoup(
            self.HTML, "html.parser", replacer=SoupReplacer(attrs_xformer=drop_p_attrs)
        )

        assert [p.attrs for p in soup.find_all("p")] == [{}, {}]
        assert soup.div["class"] == ["box"]
        assert soup.div["id"] == "d"
        assert soup.a["href"] == "/y"
        assert soup.span["class"] == ["s"]

    def test_xformer_changes_tag_in_place(self):
        def remove_class_attr(tag):
            if "class" in tag.attrs:
                del tag.attrs["class"]
            return "ignored"

        soup = BeautifulSoup(
            self.HTML, "html.parser", replacer=SoupReplacer(xformer=remove_class_attr)
        )

        assert soup.div.attrs == {"id": "d"}
        assert soup.p.attrs == {"id": "first"}
        assert soup.span.attrs == {}
        assert soup.span.get_text() == "y"

    def test_renamed_tag_closes_inside_tag_with_same_new_name(self):
        soup = BeautifulSoup(
            self.HTML, "html.parser", replacer=SoupReplacer(name_xformer=b_to_blockquote)
        )

        outer = soup.contents[1]
        assert outer.name == "blockquote"
        assert outer.contents[0].name == "blockquote"
        assert outer.contents[0].get_text() == "inner"
        assert outer.contents[1] == "outer"
        assert outer.parent is soup
