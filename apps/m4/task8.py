import sys

from bs4 import BeautifulSoup

if __name__ == "__main__":
    with open(sys.argv[1], "rb") as fs:
        soup = BeautifulSoup(fs, "html.parser")
    for node in soup:
        print(node)
