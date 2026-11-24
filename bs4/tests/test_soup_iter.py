"""Tests for iterating over every node of a BeautifulSoup object."""

from bs4 import BeautifulSoup

# NavigableString is the string content part of a tag. make type check easier.
# e.g. <p>hi</> would make "hi" a NavigableString. Found it in element.
from bs4.element import NavigableString


class TestSoupIteration:
    def test_iterates_over_tags(self):
        soup = BeautifulSoup("<div><p><b></b></p></div>", "html.parser")
        names = [node.name for node in soup]
        assert names == ["div", "p", "b"]

    def test_iterates_over_strings(self):
        soup = BeautifulSoup("<p>hello<b>world</b></p>", "html.parser")
        strings = [node for node in soup if isinstance(node, NavigableString)]
        assert strings == ["hello", "world"]

    def test_iterates_over_tags_and_strings_together(self):
        soup = BeautifulSoup("<ul><li>one</li><li>two</li></ul>", "html.parser")
        nodes = [str(node) for node in soup]
        assert nodes == [
            "<ul><li>one</li><li>two</li></ul>",
            "<li>one</li>",
            "one",
            "<li>two</li>",
            "two",
        ]

    def test_empty_soup(self):
        soup = BeautifulSoup("", "html.parser")
        assert list(soup) == []

    def test_one_node_at_a_time(self):
        soup = BeautifulSoup("<p>a</p>", "html.parser")
        itr = iter(soup)
        assert next(itr) is soup.p
        assert next(itr) == "a"
