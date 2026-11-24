# Milestone 4

```
python3 ./apps/m4/task8.py ./doc.jp/index.html
python3 -m pytest bs4/tests/test_soup_iter.py
```

It prints every node of the document, one at a time.

## Iterate

`bs4/__init__.py` is a generator function. 
It takes the root and walk to the next one by one and yield each one.

## Tests

1. Tags test
2. Strings test
3. Tags and strings mixed together test
4. Empty soup gives no nodes test
5. Nodes are produced one at a time with next() test
