from __future__ import unicode_literals

import fnmatch
import inspect
import json
import re

if False:  # pylint: disable=using-constant-test
    from typing import (  # pylint: disable=unused-import
        Any, Callable, Iterable, List, Optional, Pattern, Text, TypeVar)
    T = TypeVar("T")
    U = TypeVar("U")


def is_string(text):
    # type: (Any) -> bool
    try:
        return isinstance(text, (unicode, str))
    except NameError:
        return isinstance(text, str)


def quote(text):
    # type: (Optional[Text]) -> Text
    """Returns a quoted representation of the given string, to be used
    as a C(++) string literal."""
    text = text or ""
    if not is_string(text):
        raise TypeError("expected string")
    return json.dumps(text)


def compile_globs(patterns):
    # type: (Iterable[Text]) -> Pattern
    patterns = [fnmatch.translate(pattern) for pattern in patterns]
    regex = re.compile(r"\A({})\Z".format("|".join(patterns)))
    return regex


def flatten(iterable):
    # type: (Iterable[Any]) -> List[Any]
    result = []
    stack = [list(iterable)]
    while stack:
        if not stack[-1]:
            stack.pop()
            continue

        elem = stack[-1].pop()
        if isinstance(elem, list) or inspect.isgenerator(elem):
            stack.append(list(elem))
            continue
        result.append(elem)
    result.reverse()
    return result


def join_arguments(*arguments):
    # type: (*Any) -> Text
    return ", ".join([arg for arg in flatten(arguments) if arg is not None])


def strip_prefix(text, *prefixes):
    # type: (Text, *Text) -> Text
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text
