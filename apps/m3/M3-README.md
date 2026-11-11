# Milestone 3

Run from the repository root:

```
python3 ./apps/m3/task7.py ./doc.jp/index.html output.html
```

It sets class="test" on all  tags

## SoupReplacer: Milestone 2 vs Milestone 3

**Milestone 2:** `SoupReplacer("b", "blockquote")` : used to be one feature. replacing a tag with another one.

**Milestone 3:** beside the method overload. It is better if we extend the functionality of the method by giving it optional params:

- `name_xformer`    : replace names.
- `attrs_xformer`  : replace attributes.
- `xformer`              : custom transformer to make transformation in-place, no returns.

Instead of straight replace feature. These new params offer powerful approach to change attributes, names, and any other stuff user feel like to. The only cost is to pass a function in.

The new attributes offers a more powerful transformation options.  

However The functions run at the start tag, do not have access to its content / children

## Recommendation

- keep the previous approach untouched, to pass the previous test cases. However, we can make attrs optional so that we can write our new feature without affecting the deprecated version. name_xformer and attrs_xformer are straight forward. And go for xformer for more complex usage.
