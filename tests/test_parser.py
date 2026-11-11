"""Parser description tests: sigils must survive when not cleaning.

With ``clean_description=False`` (the default) tags stay in the
description, so the final ``+``/``@`` cleanup must not run: it stripped
the sigils off kept tags and corrupted ordinary text (``C++`` became
``C``, ``user@x.com`` became ``userx.com``). With
``clean_description=True`` the cleanup still applies.
"""

from vitodo.parser import Parser


def parse(item, clean):
    return Parser("todo.txt", clean)._parse_item(item)


def test_no_clean_keeps_tag_sigils():
    result = parse("(A) Buy milk @store +groceries", False)
    assert result["description"] == "Buy milk @store +groceries"


def test_no_clean_keeps_plain_text_sigils():
    result = parse("(A) Fix C++ build, mail user@x.com", False)
    assert result["description"] == "Fix C++ build, mail user@x.com"


def test_clean_still_strips_sigils():
    result = parse("(A) Buy milk @store +groceries", True)
    assert result["description"] == "Buy milk"
    assert "@" not in result["description"]
    assert "+" not in result["description"]
