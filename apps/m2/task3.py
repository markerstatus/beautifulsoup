import sys

from bs4 import BeautifulSoup, SoupStrainer


def main(path):
    # SoupStrainer(True) matches every tag name. Parsing still builds
    # the whole tree, because "all tags" leaves nothing to skip.
    # Tasks 2 and 4 can drop unmatched nodes. This one cannot.
    every_tag = SoupStrainer(True)
    with open(path, "rb") as handle:
        soup = BeautifulSoup(handle, "html.parser", parse_only=every_tag)
    for tag in soup.find_all(True):
        print(tag.name)


if __name__ == "__main__":
    main(sys.argv[1])
