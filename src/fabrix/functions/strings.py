"""
Implements common string manipulation functions for Fabric expressions.
"""

import uuid
from typing import Any

from fabrix.registry import registry
from fabrix.utils import as_int, as_string


@registry.register("concat")
def concat(*args: Any) -> str:
    """
    Combine two or more strings, and return the combined string.

    Parameters
    ----------
    *args : Any
        Strings to concatenate.

    Returns
    -------
    str
        The concatenated string.
    """
    return "".join(as_string(arg) for arg in args)


@registry.register("endsWith")
def ends_with(
    string: str,
    suffix: str,
) -> bool:
    """
    Check whether a string ends with the specified substring.

    Parameters
    ----------
    string : str
        The string to check.
    suffix : str
        The suffix to check for.

    Returns
    -------
    bool
        True if string ends with suffix, else False.
    """
    return str(string).endswith(str(suffix))


@registry.register("guid")
def guid() -> str:
    """
    Generate a globally unique identifier (GUID) as a string.

    Parameters
    ----------

    Returns
    -------
    str
        A GUID string.
    """
    return as_string(uuid.uuid4())


@registry.register("indexOf")
def index_of(string: str, substring: str) -> int:
    """
    Return the starting position for a substring.

    Parameters
    ----------
    string : str
        The string to search.
    substring : str
        The substring to find.

    Returns
    -------
    int
        The index of the first occurrence of substring, or -1 if not found.
    """
    index = as_string(string).find(as_string(substring))
    return index if index >= 0 else 0


@registry.register("lastIndexOf")
def last_index_of(string: str, substring: str) -> int:
    """
    Return the starting position for the last occurrence of a substring.

    Parameters
    ----------
    string : str
        The string to search.
    substring : str
        The substring to find.

    Returns
    -------
    int
        The index of the last occurrence of substring, or -1 if not found.
    """
    index = as_string(string).rfind(as_string(substring))
    return index if index >= 0 else 0


@registry.register("replace")
def replace(string: str, old: str, new: str) -> str:
    """
    Replace a substring with the specified string, and return the updated string.

    Parameters
    ----------
    string : str
        The original string.
    old : str
        The substring to replace.
    new : str
        The replacement string.

    Returns
    -------
    str
        The updated string.
    """
    return as_string(string).replace(as_string(old), as_string(new))


@registry.register("split")
def split(
    string: str,
    delimiter: str | None = ",",
) -> list[str]:
    """
    Return an array that contains substrings, separated by commas or a specified delimiter.

    Parameters
    ----------
    string : str
        The original string.
    delimiter : str, optional
        The delimiter to split on. Defaults to ','.

    Returns
    -------
    list[str]
        List of substrings.
    """
    return as_string(string).split(delimiter if delimiter is not None else ",")


@registry.register("startsWith")
def starts_with(string: str, prefix: str) -> bool:
    """
    Check whether a string starts with a specific substring.

    Parameters
    ----------
    string : str
        The string to check.
    prefix : str
        The prefix to check for.

    Returns
    -------
    bool
        True if string starts with prefix, else False.
    """
    return as_string(string).startswith(as_string(prefix))


@registry.register("substring")
def substring(
    string: str,
    start: int,
    length: int,
) -> str:
    """
    Return characters from a string, starting from the specified position.

    Parameters
    ----------
    string : str
        The string to take a substring from.
    start : int
        The start index.
    length : int, optional
        Number of characters to return. If omitted, returns to the end.

    Returns
    -------
    str
        The substring.
    """
    s = as_string(string)
    start = as_int(start)
    length = as_int(length)

    if any(value < 0 for value in (start, length)):
        raise ValueError("Parameters 'start' and 'length' should be greater equal 0")

    if start + length > len(s):
        raise ValueError("Sum of parameters 'start' and 'length' should be equal to to length of the string.")

    return s[start : start + length]


@registry.register("toLower")
def to_lower(string: str) -> str:
    """
    Return a string in lowercase format.

    Parameters
    ----------
    string : str
        The string to convert.

    Returns
    -------
    str
        The lowercase string.
    """
    return as_string(string).lower()


@registry.register("toUpper")
def to_upper(string: str) -> str:
    """
    Return a string in uppercase format.

    Parameters
    ----------
    string : str
        The string to convert.

    Returns
    -------
    str
        The uppercase string.
    """
    return as_string(string).upper()


@registry.register("trim")
def trim(string: str) -> str:
    """
    Remove leading and trailing whitespace from a string, and return the updated string.

    Parameters
    ----------
    string : str
        The string to trim.

    Returns
    -------
    str
        The trimmed string.
    """
    return as_string(string).strip()
