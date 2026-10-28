import sys

from bs4 import BeautifulSoup, SoupStrainer


def main(path):
    # only parse the a tag part
    only_tag = SoupStrainer("a")
    with open(path, "rb") as html_doc:
        soup = BeautifulSoup(html_doc, "html.parser", parse_only=only_tag)
    for anchor in soup.find_all("a"):
        href = anchor.get("href")
        if href is not None:
            print(href)


if __name__ == "__main__":
    main(sys.argv[1])
