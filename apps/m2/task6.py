import sys
from pathlib import Path

from bs4 import BeautifulSoup, SoupReplacer


def main(path, output_path):
    # Rename <b> to <blockquote> while the parser builds the tree.
    b_to_blockquote = SoupReplacer("b", "blockquote")
    with open(path, "rb") as handle:
        soup = BeautifulSoup(handle, "html.parser", replacer=b_to_blockquote)
    Path(output_path).write_text(soup.prettify(), encoding="utf-8")


if __name__ == "__main__":
    source = sys.argv[1]
    destination = sys.argv[2] if len(sys.argv) > 2 else "output.html"
    main(source, destination)
