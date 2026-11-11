import sys
from pathlib import Path

from bs4 import BeautifulSoup, SoupReplacer


def p_with_test_class(tag):
    # Replace class attr with "test" on all <p> tags
    if tag.name == "p":
        attrs = dict(tag.attrs)
        attrs["class"] = "test"
        return attrs
    return tag.attrs


if __name__ == "__main__":
    source = sys.argv[1]
    # give it default value if not provided
    destination = sys.argv[2] if len(sys.argv) > 2 else "output.html"
    replacer = SoupReplacer(attrs_xformer=p_with_test_class)
    with open(source, "rb") as fs:
        soup = BeautifulSoup(fs, "html.parser", replacer=replacer)
    # write to file, default as "output.html"
    Path(destination).write_text(soup.prettify(), encoding="utf-8")
