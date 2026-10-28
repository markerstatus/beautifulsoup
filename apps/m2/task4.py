import sys

from bs4 import BeautifulSoup, SoupStrainer


def main(path):
    # id=True keeps a tag only when that attribute is present.
    only_with_id = SoupStrainer(id=True)
    with open(path, "rb") as handle:
        soup = BeautifulSoup(handle, "html.parser", parse_only=only_with_id)
    for tag in soup.find_all(id=True):
        print(f"<{tag.name} id=\"{tag.get('id')}\">")


if __name__ == "__main__":
    main(sys.argv[1])
